from tools import generate_detections as gdet
from deep_sort.tracker import Tracker
from deep_sort.detection import Detection
from deep_sort import preprocessing, nn_matching
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1 import ConfigProto
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
from core.config import cfg
from tensorflow.python.saved_model import tag_constants
from core.functions import *
from core.yolov4 import filter_boxes
import core.utils as utils
from absl.flags import FLAGS
from absl import app, flags, logging
import tensorflow as tf
import time
import os
import json

# comment out below line to enable tensorflow logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
# deep sort imports
flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', './data/video/test.mp4',
                    'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID',
                    'codec used in VideoWriter when saving video to file')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('dont_show', False, 'dont show video output')
flags.DEFINE_boolean('info', False, 'show detailed info of tracked objects')
flags.DEFINE_boolean('count', False, 'count objects being tracked on screen')
# Creates the flag for each new function. Defines the data type, the name, the default value and a basic description
flags.DEFINE_boolean('trail', False, 'draw object tracking trail')
flags.DEFINE_integer('trail_radius', 4, 'radius of trail points')
flags.DEFINE_integer('min_hits', 5, 'minimum hits to save object')
flags.DEFINE_boolean('total_class', False, 'print class count on completion')
flags.DEFINE_boolean('total_dir', False, 'print direction count on completion')
flags.DEFINE_boolean('total_dir_class', False,
                     'print direction count on completion per class')
flags.DEFINE_string('tracked_objects_names', 'trackedObjects',
                    'path to output trackedObject data')


# Translates an angular value to a physical direction of travel value
def angle_to_direction(cur_angle):
    if cur_angle < 45 and cur_angle > -45:
        cur_dir = 'right'
    elif cur_angle <= -45 and cur_angle > -135:
        cur_dir = 'down'
    elif cur_angle >= 45 and cur_angle < 135:
        cur_dir = 'up'
    else:
        cur_dir = 'left'
    return cur_dir


# Confirms detected objects are valid detections comparing with the minimum hits value
def all_valid_track(historic_tracks, min_hits):
    all_valid_tracks = {k: v for k, v in historic_tracks.items() if (
        v["hits"] >= min_hits) and v["state"] != 1}
    return all_valid_tracks


# Updates the number of objects travelling in each direction per class
def seen_classes_direction(current_class, seen_classes_dir, current_dir):
    if current_class in seen_classes_dir:
        if current_dir in seen_classes_dir[current_class]:
            seen_classes_dir[current_class][current_dir] += 1
        else:
            seen_classes_dir[current_class][current_dir] = 1
    else:
        seen_classes_dir[current_class] = {current_dir: 1}
    return seen_classes_dir

# Updates the number of objects travelling in each direction
def seen_direction(current_dir, seen_dirs):
    if current_dir in seen_dirs:
        seen_dirs[current_dir] += 1
    else:
        seen_dirs[current_dir] = 1
    return seen_dirs


def main(_argv):
    # Definition of the parameters
    max_cosine_distance = 0.4
    nn_budget = None
    nms_max_overlap = 1.0

    # initialize deep sort
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    # calculate cosine distance metric
    metric = nn_matching.NearestNeighborDistanceMetric(
        "cosine", max_cosine_distance, nn_budget)
    # initialize tracker
    tracker = Tracker(metric)

    # load configuration for object detector
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = FLAGS.video

    # load tflite model if flag is set
    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print(input_details)
        print(output_details)
    # otherwise load standard tensorflow saved model
    else:
        saved_model_loaded = tf.saved_model.load(
            FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    out = None

    # get video ready to save locally if flag is set
    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))

    frame_num = 0
    # while video is running
    while True:
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break
        frame_num += 1
        print('Frame #: ', frame_num)
        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()

        # run detections on tflite if flag is set
        if FLAGS.framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(
                output_details[i]['index']) for i in range(len(output_details))]
            # run detections using yolov3 if flag is set
            if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
        else:
            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )

        # convert data to numpy arrays and slice out unused elements
        num_objects = valid_detections.numpy()[0]
        bboxes = boxes.numpy()[0]
        bboxes = bboxes[0:int(num_objects)]
        scores = scores.numpy()[0]
        scores = scores[0:int(num_objects)]
        classes = classes.numpy()[0]
        classes = classes[0:int(num_objects)]

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, width, height
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(bboxes, original_h, original_w)

        # store all predictions in one parameter for simplicity when calling functions
        pred_bbox = [bboxes, scores, classes, num_objects]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        #allowed_classes = list(class_names.values())

        # custom allowed classes (uncomment line below to customize tracker for only people)
        allowed_classes = ['person', 'bicycle',
                           'car', 'motorbike', 'bus', 'truck']

        # loop through objects and use class index to get class name, allow only classes in allowed_classes list
        names = []
        deleted_indx = []
        for i in range(num_objects):
            class_indx = int(classes[i])
            class_name = class_names[class_indx]
            if class_name not in allowed_classes:
                deleted_indx.append(i)
            else:
                names.append(class_name)
        names = np.array(names)
        count = len(names)
        if FLAGS.count:
            # count objects found
            counted_classes = count_objects(
                pred_bbox, by_class=True, allowed_classes=allowed_classes)
            # loop through dict and print
            for key, value in counted_classes.items():
                print("Number of {}s: {}".format(key, value))
            image = utils.draw_bbox(frame, pred_bbox, FLAGS.info, counted_classes,
                                    allowed_classes=allowed_classes, show_label=False)
        else:
            image = utils.draw_bbox(
                frame, pred_bbox, FLAGS.info, allowed_classes=allowed_classes, show_label=False)

        # encode yolo detections and feed to tracker
        features = encoder(frame, bboxes)
        detections = [Detection(bbox, score, class_name, feature) for bbox,
                      score, class_name, feature in zip(bboxes, scores, names, features)]

        # initialize color map
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

        # run non-maxima supression
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(
            boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]

        # Call the tracker
        tracker.predict()
        tracker.update(detections)

        # update tracks
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            class_name = track.get_class()

        # draw bbox on screen
            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]
            #cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(
                len(class_name)+len(str(track.track_id)))*17, int(bbox[1])), color, -1)
            cv2.putText(frame, class_name + "-" + str(track.track_id),
                        (int(bbox[0]), int(bbox[1]-10)), 0, 0.75, (255, 255, 255), 2)
            if FLAGS.trail:
                for point in track.locations:
                    cv2.circle(frame, point, FLAGS.trail_radius, color, -1)

        # if enable info flag then print details about each track
            if FLAGS.info:
                print("Tracker ID: {}, Class: {},  BBox Coords (xmin, ymin, xmax, ymax): {}".format(
                    str(track.track_id), class_name, (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))))

        # calculate frames per second of running detections
        fps = 1.0 / (time.time() - start_time)
        print("FPS: %.2f" % fps)
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if not FLAGS.dont_show:
            cv2.imshow("Output Video", result)

        # if output flag is set, save video file
        if FLAGS.output:
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    # Checks if tracked objects are valid
    all_valid_tracks = all_valid_track(tracker.historic_tracks, FLAGS.min_hits)

    # Saves records of valid tracks to defined location
    with open(FLAGS.tracked_objects_names + '.json', 'w') as object_store:
        json.dump(all_valid_tracks, object_store)

    seen_classes_dir = {}
    seen_dirs = {}
    for track_id in all_valid_tracks:
        current_class = all_valid_tracks[track_id]['class']
        current_angle = all_valid_tracks[track_id]['direction']

        current_dir = angle_to_direction(current_angle)
        seen_classes_dir = seen_classes_direction(current_class, seen_classes_dir, current_dir)
        seen_dirs = seen_direction(current_dir, seen_dirs)

    open(FLAGS.tracked_objects_names + '.txt', 'w').close()
    # If total direction per class flag is true, saves data to specified location
    if FLAGS.total_dir_class:
        print("\nCounts of each class in each direction: \n   ")
        print(seen_classes_dir)
        with open(FLAGS.tracked_objects_names + '.txt', 'a') as dir_class_store:
            dir_class_store.write('Counts of each class in each direction: ')
            json.dump(seen_classes_dir, dir_class_store)
    # If total count per class flag is true, saves data to specified location
    if FLAGS.total_class:
        print("\nCounts of each class:")
        with open(FLAGS.tracked_objects_names + '.txt', 'a') as count_class_store:
            count_class_store.write('\n\nCounts of each class: ')
            for current_class in seen_classes_dir:
                print(current_class + ': ' +
                      str(sum(seen_classes_dir[current_class].values())))
                count_class_store.write(
                    "\n"+current_class + ': ' + str(sum(seen_classes_dir[current_class].values())))
    # If total count per direction flag is true, saves data to specified location
    if FLAGS.total_dir:
        print("\nCounts of each direction:")
        with open(FLAGS.tracked_objects_names + '.txt', 'a') as dir_store:
            dir_store.write('\n\nCounts in each direction: ')
            for dir_name, count in seen_dirs.items():
                print(dir_name + ': ' + str(count))
                dir_store.write("\n" + dir_name + ': ' + str(count))


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        print("ignoring exit")
    finally:
        menu.open_result_window()
