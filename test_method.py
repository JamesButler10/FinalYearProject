import unittest
from deep_sort.track import Track 
import sys
import os

from object_tracker import angle_to_direction
from object_tracker import all_valid_track
from object_tracker import seen_classes_direction
from object_tracker import seen_direction
import pytest

# Unit tests for calculating angular direction of travel
def test_direction_x_y_ne():
    x_array = [0,1]
    y_array = [0,1]
    expected = -45

    actual = Track.direction( y_array, x_array)

    assert actual == expected

def test_direction_x_y_nw():
    x_array = [0,-1]
    y_array = [0,1]
    expected = -135

    actual = Track.direction(y_array, x_array)

    assert actual == expected

def test_direction_x_y_sw():
    x_array = [0,-1]
    y_array = [0,-1]
    expected = 135

    actual = Track.direction(y_array, x_array)

    assert actual == expected     

def test_direction_x_y_se():
    x_array = [0,1]
    y_array = [0,-1]
    expected = 45

    actual = Track.direction(y_array, x_array)

    assert actual == expected

def test_direction_x_y_n():
    x_array = [0,0]
    y_array = [0,1]
    expected = -90

    actual = Track.direction(y_array, x_array)

    assert actual == expected

def test_direction_x_y_s():
    x_array = [0,0]
    y_array = [0,-1]
    expected = 90

    actual = Track.direction(y_array, x_array)

    assert actual == expected
def test_direction_x_y_e():
    x_array = [0,1]
    y_array = [0,0]
    expected = 0

    actual = Track.direction(y_array, x_array)

    assert actual == expected

def test_direction_x_y_w():
    x_array = [0,-1]
    y_array = [0,0]
    expected = 180

    actual = Track.direction(y_array, x_array)

    assert actual == expected

# Unit tests for translating angular direction to physical direction
def test_angle_to_name_up():
    angle = 90
    expected = "up"

    actual = angle_to_direction(angle)

    assert actual == expected

def test_angle_to_name_down():
    angle = -90
    expected = "down"

    actual = angle_to_direction(angle)

    assert actual == expected

def test_angle_to_name_right():
    angle = 0
    expected = "right"

    actual = angle_to_direction(angle)

    assert actual == expected

def test_angle_to_name_left():
    angle = 180
    expected = "left"

    actual = angle_to_direction(angle)

    assert actual == expected

def test_angle_to_name_left_negative():
    angle = -180
    expected = "left"

    actual = angle_to_direction(angle)

    assert actual == expected

# Unit tests for calculating the velocity of a detected object
def test_velocity_4_4_5():
    hyp_changes=[5,5,5]
    x_changes=[4,4,4]
    expected = 5
    actual = Track.velocity(hyp_changes,x_changes)
    assert actual == expected

def test_velocity_1_3_5():
    hyp_changes=[1,3,5]
    x_changes=[1,4,5]
    expected = 3
    actual = Track.velocity(hyp_changes,x_changes)
    assert actual == expected

def test_velocity_empty():
    hyp_changes=[]
    x_changes=[]
    expected = 0 
    actual = Track.velocity(hyp_changes,x_changes)
    assert actual == expected

# Unit tests for calculating which detected objects are valid
def test_all_valid_tracks_0():
    tracks = {"1": {"class": "person", "state": 3, "hits": 47, "age": 108, "direction": -156.6951094607969, "velocity": 6.4792709854662265}, "2": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 25.443377201972872, "velocity": 2.440185844902603}, "3": {"class": "person", "state": 3, "hits": 68, "age": 129, "direction": -76.79207153722089, "velocity": 3.2648541499419523}, "4": {"class": "person", "state": 2, "hits": 192, "age": 302, "direction": 25.0284241238516, "velocity": 2.6832040000582524}, "5": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 27.247619385504933, "velocity": 2.219224588985763}, "6": {"class": "person", "state": 3, "hits": 187, "age": 248, "direction": -146.64057221391175, "velocity": 6.339396967455296}, "7": {"class": "person", "state": 3, "hits": 171, "age": 251, "direction": 70.96195998269746, "velocity": 1.1828542578621577}, "8": {"class": "bicycle", "state": 3, "hits": 34, "age": 96, "direction": 32.05737573420543, "velocity": 3.698400117773726}, "9": {"class": "bicycle", "state": 2, "hits": 164, "age": 302, "direction": -0.2833596062736018, "velocity": 10.589558200896596}, "10": {"class": "person", "state": 3, "hits": 62, "age": 128, "direction": 40.601294645004465, "velocity": 1.5125267828237856}, "11": {"class": "person", "state": 3, "hits": 11, "age": 72, "direction": -75.46554491945989, "velocity": 3.215232560644508}, "12": {"class": "person", "state": 3, "hits": 70, "age": 182, "direction": -103.89572681644471, "velocity": 12.369715109749631}, "13": {"class": "person", "state": 2, "hits": 222, "age": 302, "direction": 149.74356283647074, "velocity": 2.251890776749808}, "15": {"class": "person", "state": 2, "hits": 280, "age": 302, "direction": -159.5565642649657, "velocity": 2.5495927789962702}, "16": {"class": "bicycle", "state": 3, "hits": 134, "age": 204, "direction": -142.43140797117252, "velocity": 6.275088634532456}, "19": {"class": "person", "state": 2, "hits": 297, "age": 297, "direction": 45.95052149970131, "velocity": 3.472399634430497}, "23": {"class": "person", "state": 3, "hits": 47, "age": 109, "direction": 17.417970792202837, "velocity": 1.4272036127660592}, "24": {"class": "person", "state": 2, "hits": 229, "age": 295, "direction": -18.012109418251512, "velocity": 6.900899950304319}, "27": {"class": "person", "state": 3, "hits": 52, "age": 115, "direction": -157.02945118574078, "velocity": 6.099741182962275}, "28": {"class": "person", "state": 3, "hits": 54, "age": 121, "direction": 29.357753542791272, "velocity": 0.6282611429109403}, "31": {"class": "person", "state": 3, "hits": 26, "age": 105, "direction": -126.62574097240096, "velocity": 6.141147351147824}, "39": {"class": "person", "state": 2, "hits": 190, "age": 216, "direction": -113.33042594484222, "velocity": 3.570083704496993}, "42": {"class": "person", "state": 3, "hits": 6, "age": 67, "direction": -95.1944289077348, "velocity": 2.282842712474619}, "44": {"class": "bicycle", "state": 3, "hits": 9, "age": 70, "direction": -170.21759296819272, "velocity": 8.137451211826939}, "45": {"class": "person", "state": 2, "hits": 64, "age": 152, "direction": 21.618239459754502, "velocity": 5.088266065023704}, "48": {"class": "person", "state": 3, "hits": 5, "age": 66, "direction": 90.0, "velocity": 0.25}, "49": {"class": "person", "state": 3, "hits": 16, "age": 78, "direction": 180.0, "velocity": 0.3333333333333333}, "51": {"class": "person", "state": 3, "hits": 12, "age": 73, "direction": 129.8055710922652, "velocity": 1.134428060419916}, "52": {"class": "person", "state": 3, "hits": 7, "age": 70, "direction": -72.34987578006988, "velocity": 3.925863654765692}, "54": {"class": "person", "state": 2, "hits": 96, "age": 96, "direction": 52.69605172201658, "velocity": 3.187147937244006}, "59": {"class": "person", "state": 2, "hits": 74, "age": 76, "direction": 23.834262901043378, "velocity": 4.936086483064871}, "60": {"class": "person", "state": 2, "hits": 13, "age": 13, "direction": 26.241349652157766, "velocity": 7.733833178709807}, "61": {"class": "person", "state": 2, "hits": 10, "age": 10, "direction": 31.42956561483852, "velocity": 5.825574167960355}}
    min_hits = 0
    expected = {"1": {"class": "person", "state": 3, "hits": 47, "age": 108, "direction": -156.6951094607969, "velocity": 6.4792709854662265}, "2": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 25.443377201972872, "velocity": 2.440185844902603}, "3": {"class": "person", "state": 3, "hits": 68, "age": 129, "direction": -76.79207153722089, "velocity": 3.2648541499419523}, "4": {"class": "person", "state": 2, "hits": 192, "age": 302, "direction": 25.0284241238516, "velocity": 2.6832040000582524}, "5": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 27.247619385504933, "velocity": 2.219224588985763}, "6": {"class": "person", "state": 3, "hits": 187, "age": 248, "direction": -146.64057221391175, "velocity": 6.339396967455296}, "7": {"class": "person", "state": 3, "hits": 171, "age": 251, "direction": 70.96195998269746, "velocity": 1.1828542578621577}, "8": {"class": "bicycle", "state": 3, "hits": 34, "age": 96, "direction": 32.05737573420543, "velocity": 3.698400117773726}, "9": {"class": "bicycle", "state": 2, "hits": 164, "age": 302, "direction": -0.2833596062736018, "velocity": 10.589558200896596}, "10": {"class": "person", "state": 3, "hits": 62, "age": 128, "direction": 40.601294645004465, "velocity": 1.5125267828237856}, "11": {"class": "person", "state": 3, "hits": 11, "age": 72, "direction": -75.46554491945989, "velocity": 3.215232560644508}, "12": {"class": "person", "state": 3, "hits": 70, "age": 182, "direction": -103.89572681644471, "velocity": 12.369715109749631}, "13": {"class": "person", "state": 2, "hits": 222, "age": 302, "direction": 149.74356283647074, "velocity": 2.251890776749808}, "15": {"class": "person", "state": 2, "hits": 280, "age": 302, "direction": -159.5565642649657, "velocity": 2.5495927789962702}, "16": {"class": "bicycle", "state": 3, "hits": 134, "age": 204, "direction": -142.43140797117252, "velocity": 6.275088634532456}, "19": {"class": "person", "state": 2, "hits": 297, "age": 297, "direction": 45.95052149970131, "velocity": 3.472399634430497}, "23": {"class": "person", "state": 3, "hits": 47, "age": 109, "direction": 17.417970792202837, "velocity": 1.4272036127660592}, "24": {"class": "person", "state": 2, "hits": 229, "age": 295, "direction": -18.012109418251512, "velocity": 6.900899950304319}, "27": {"class": "person", "state": 3, "hits": 52, "age": 115, "direction": -157.02945118574078, "velocity": 6.099741182962275}, "28": {"class": "person", "state": 3, "hits": 54, "age": 121, "direction": 29.357753542791272, "velocity": 0.6282611429109403}, "31": {"class": "person", "state": 3, "hits": 26, "age": 105, "direction": -126.62574097240096, "velocity": 6.141147351147824}, "39": {"class": "person", "state": 2, "hits": 190, "age": 216, "direction": -113.33042594484222, "velocity": 3.570083704496993}, "42": {"class": "person", "state": 3, "hits": 6, "age": 67, "direction": -95.1944289077348, "velocity": 2.282842712474619}, "44": {"class": "bicycle", "state": 3, "hits": 9, "age": 70, "direction": -170.21759296819272, "velocity": 8.137451211826939}, "45": {"class": "person", "state": 2, "hits": 64, "age": 152, "direction": 21.618239459754502, "velocity": 5.088266065023704}, "48": {"class": "person", "state": 3, "hits": 5, "age": 66, "direction": 90.0, "velocity": 0.25}, "49": {"class": "person", "state": 3, "hits": 16, "age": 78, "direction": 180.0, "velocity": 0.3333333333333333}, "51": {"class": "person", "state": 3, "hits": 12, "age": 73, "direction": 129.8055710922652, "velocity": 1.134428060419916}, "52": {"class": "person", "state": 3, "hits": 7, "age": 70, "direction": -72.34987578006988, "velocity": 3.925863654765692}, "54": {"class": "person", "state": 2, "hits": 96, "age": 96, "direction": 52.69605172201658, "velocity": 3.187147937244006}, "59": {"class": "person", "state": 2, "hits": 74, "age": 76, "direction": 23.834262901043378, "velocity": 4.936086483064871}, "60": {"class": "person", "state": 2, "hits": 13, "age": 13, "direction": 26.241349652157766, "velocity": 7.733833178709807}, "61": {"class": "person", "state": 2, "hits": 10, "age": 10, "direction": 31.42956561483852, "velocity": 5.825574167960355}}
    actual = all_valid_track(tracks,min_hits)
    assert actual == expected

def test_all_valid_tracks_15():
    tracks = {"1": {"class": "person", "state": 3, "hits": 47, "age": 108, "direction": -156.6951094607969, "velocity": 6.4792709854662265}, "2": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 25.443377201972872, "velocity": 2.440185844902603}, "3": {"class": "person", "state": 3, "hits": 68, "age": 129, "direction": -76.79207153722089, "velocity": 3.2648541499419523}, "4": {"class": "person", "state": 2, "hits": 192, "age": 302, "direction": 25.0284241238516, "velocity": 2.6832040000582524}, "5": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 27.247619385504933, "velocity": 2.219224588985763}, "6": {"class": "person", "state": 3, "hits": 187, "age": 248, "direction": -146.64057221391175, "velocity": 6.339396967455296}, "7": {"class": "person", "state": 3, "hits": 171, "age": 251, "direction": 70.96195998269746, "velocity": 1.1828542578621577}, "8": {"class": "bicycle", "state": 3, "hits": 34, "age": 96, "direction": 32.05737573420543, "velocity": 3.698400117773726}, "9": {"class": "bicycle", "state": 2, "hits": 164, "age": 302, "direction": -0.2833596062736018, "velocity": 10.589558200896596}, "10": {"class": "person", "state": 3, "hits": 62, "age": 128, "direction": 40.601294645004465, "velocity": 1.5125267828237856}, "11": {"class": "person", "state": 3, "hits": 11, "age": 72, "direction": -75.46554491945989, "velocity": 3.215232560644508}, "12": {"class": "person", "state": 3, "hits": 70, "age": 182, "direction": -103.89572681644471, "velocity": 12.369715109749631}, "13": {"class": "person", "state": 2, "hits": 222, "age": 302, "direction": 149.74356283647074, "velocity": 2.251890776749808}, "15": {"class": "person", "state": 2, "hits": 280, "age": 302, "direction": -159.5565642649657, "velocity": 2.5495927789962702}, "16": {"class": "bicycle", "state": 3, "hits": 134, "age": 204, "direction": -142.43140797117252, "velocity": 6.275088634532456}, "19": {"class": "person", "state": 2, "hits": 297, "age": 297, "direction": 45.95052149970131, "velocity": 3.472399634430497}, "23": {"class": "person", "state": 3, "hits": 47, "age": 109, "direction": 17.417970792202837, "velocity": 1.4272036127660592}, "24": {"class": "person", "state": 2, "hits": 229, "age": 295, "direction": -18.012109418251512, "velocity": 6.900899950304319}, "27": {"class": "person", "state": 3, "hits": 52, "age": 115, "direction": -157.02945118574078, "velocity": 6.099741182962275}, "28": {"class": "person", "state": 3, "hits": 54, "age": 121, "direction": 29.357753542791272, "velocity": 0.6282611429109403}, "31": {"class": "person", "state": 3, "hits": 26, "age": 105, "direction": -126.62574097240096, "velocity": 6.141147351147824}, "39": {"class": "person", "state": 2, "hits": 190, "age": 216, "direction": -113.33042594484222, "velocity": 3.570083704496993}, "42": {"class": "person", "state": 3, "hits": 6, "age": 67, "direction": -95.1944289077348, "velocity": 2.282842712474619}, "44": {"class": "bicycle", "state": 3, "hits": 9, "age": 70, "direction": -170.21759296819272, "velocity": 8.137451211826939}, "45": {"class": "person", "state": 2, "hits": 64, "age": 152, "direction": 21.618239459754502, "velocity": 5.088266065023704}, "48": {"class": "person", "state": 3, "hits": 5, "age": 66, "direction": 90.0, "velocity": 0.25}, "49": {"class": "person", "state": 3, "hits": 16, "age": 78, "direction": 180.0, "velocity": 0.3333333333333333}, "51": {"class": "person", "state": 3, "hits": 12, "age": 73, "direction": 129.8055710922652, "velocity": 1.134428060419916}, "52": {"class": "person", "state": 3, "hits": 7, "age": 70, "direction": -72.34987578006988, "velocity": 3.925863654765692}, "54": {"class": "person", "state": 2, "hits": 96, "age": 96, "direction": 52.69605172201658, "velocity": 3.187147937244006}, "59": {"class": "person", "state": 2, "hits": 74, "age": 76, "direction": 23.834262901043378, "velocity": 4.936086483064871}, "60": {"class": "person", "state": 2, "hits": 13, "age": 13, "direction": 26.241349652157766, "velocity": 7.733833178709807}, "61": {"class": "person", "state": 2, "hits": 10, "age": 10, "direction": 31.42956561483852, "velocity": 5.825574167960355}}
    min_hits = 15
    expected = {"1": {"class": "person", "state": 3, "hits": 47, "age": 108, "direction": -156.6951094607969, "velocity": 6.4792709854662265}, "2": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 25.443377201972872, "velocity": 2.440185844902603}, "3": {"class": "person", "state": 3, "hits": 68, "age": 129, "direction": -76.79207153722089, "velocity": 3.2648541499419523}, "4": {"class": "person", "state": 2, "hits": 192, "age": 302, "direction": 25.0284241238516, "velocity": 2.6832040000582524}, "5": {"class": "person", "state": 2, "hits": 302, "age": 302, "direction": 27.247619385504933, "velocity": 2.219224588985763}, "6": {"class": "person", "state": 3, "hits": 187, "age": 248, "direction": -146.64057221391175, "velocity": 6.339396967455296}, "7": {"class": "person", "state": 3, "hits": 171, "age": 251, "direction": 70.96195998269746, "velocity": 1.1828542578621577}, "8": {"class": "bicycle", "state": 3, "hits": 34, "age": 96, "direction": 32.05737573420543, "velocity": 3.698400117773726}, "9": {"class": "bicycle", "state": 2, "hits": 164, "age": 302, "direction": -0.2833596062736018, "velocity": 10.589558200896596}, "10": {"class": "person", "state": 3, "hits": 62, "age": 128, "direction": 40.601294645004465, "velocity": 1.5125267828237856}, "12": {"class": "person", "state": 3, "hits": 70, "age": 182, "direction": -103.89572681644471, "velocity": 12.369715109749631}, "13": {"class": "person", "state": 2, "hits": 222, "age": 302, "direction": 149.74356283647074, "velocity": 2.251890776749808}, "15": {"class": "person", "state": 2, "hits": 280, "age": 302, "direction": -159.5565642649657, "velocity": 2.5495927789962702}, "16": {"class": "bicycle", "state": 3, "hits": 134, "age": 204, "direction": -142.43140797117252, "velocity": 6.275088634532456}, "19": {"class": "person", "state": 2, "hits": 297, "age": 297, "direction": 45.95052149970131, "velocity": 3.472399634430497}, "23": {"class": "person", "state": 3, "hits": 47, "age": 109, "direction": 17.417970792202837, "velocity": 1.4272036127660592}, "24": {"class": "person", "state": 2, "hits": 229, "age": 295, "direction": -18.012109418251512, "velocity": 6.900899950304319}, "27": {"class": "person", "state": 3, "hits": 52, "age": 115, "direction": -157.02945118574078, "velocity": 6.099741182962275}, "28": {"class": "person", "state": 3, "hits": 54, "age": 121, "direction": 29.357753542791272, "velocity": 0.6282611429109403}, "31": {"class": "person", "state": 3, "hits": 26, "age": 105, "direction": -126.62574097240096, "velocity": 6.141147351147824}, "39": {"class": "person", "state": 2, "hits": 190, "age": 216, "direction": -113.33042594484222, "velocity": 3.570083704496993},"45": {"class": "person", "state": 2, "hits": 64, "age": 152, "direction": 21.618239459754502, "velocity": 5.088266065023704}, "49": {"class": "person", "state": 3, "hits": 16, "age": 78, "direction": 180.0, "velocity": 0.3333333333333333}, "54": {"class": "person", "state": 2, "hits": 96, "age": 96, "direction": 52.69605172201658, "velocity": 3.187147937244006}, "59": {"class": "person", "state": 2, "hits": 74, "age": 76, "direction": 23.834262901043378, "velocity": 4.936086483064871}}
    actual = all_valid_track(tracks,min_hits)
    assert actual == expected

def test_all_valid_tracks_empty():
    tracks = {}
    min_hits = 15
    expected ={}
    actual = all_valid_track(tracks,min_hits)
    assert actual == expected

def test_all_valid_tracks_all_fail():
    tracks = {"1": {"class": "person", "state": 3, "hits": 47, "age": 108, "direction": -156.6951094607969, "velocity": 6.4792709854662265}}
    min_hits = 50
    expected ={}
    actual = all_valid_track(tracks,min_hits)
    assert actual == expected

# Unit tests for calculating the count of each direction per class
def test_seen_classes_direction_empty():
    current_class = "person"
    current_dir = "left"
    seen_classes_dir = {}
    expected = {'person': {'left': 1}}
    actual = seen_classes_direction(current_class, seen_classes_dir, current_dir)
    assert actual == expected

def test_seen_classes_direction_empty_dir():
    current_class = "person"
    current_dir = "left"
    seen_classes_dir = {'person': {'right': 1}}
    expected = {'person': {'right': 1,'left': 1}}
    actual = seen_classes_direction(current_class, seen_classes_dir, current_dir)
    assert actual == expected

def test_seen_classes_direction_wrong_dir():
    current_class = "car"
    current_dir = "right"
    seen_classes_dir = {'person': {'right': 1}}
    expected = {'person': {'right': 1},'car': {'right': 1}}
    actual = seen_classes_direction(current_class, seen_classes_dir, current_dir)
    assert actual == expected

def test_seen_direction_empty():
    current_dir = "left"
    seen_dirs = {}
    expected = {'left':1}
    actual = seen_direction(current_dir, seen_dirs)
    assert actual == expected

def test_seen_direction_existing_dir():
    current_dir = "left"
    seen_dirs = {'left':1}
    expected = {'left':2}
    actual = seen_direction(current_dir, seen_dirs)
    assert actual == expected

def test_seen_direction_wrong_dir():
    current_dir = "left"
    seen_dirs = {'right':1}
    expected = {'right':1,'left':1}
    actual = seen_direction(current_dir, seen_dirs)
    assert actual == expected