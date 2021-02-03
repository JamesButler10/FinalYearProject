# FinalYearProject

The dataset used in training the system was the AU-AIR dataset. This dataset can be found at https://bozcani.github.io/auairdataset
The vggToYolo.py file was used to translate the original annotation into the format recognised by YOLOv4. Each image requires a unique annotation file. Thes annotations files can be seen at https://1drv.ms/u/s!AsCWK5G5eCgrgvAfd0ic6kbFgWBwsA?e=oMpXh9
train.ps1 is the powershell command used to train the weights file for the system. train.ps1 and videoTest.ps1 are used to test the system using a specified image or video
