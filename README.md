# Automated Attendance System using Face Recognition

Daily attendance at workplaces or institutions tend to be time consuming because people
resort to traditional roll call or fingerprint/RFID scanners. This, although functions well,

is very tedious. While the biometric scanners are automatic, it involves a lot of machine-
human interface. This project focuses on using the human face as a biometric to record

the attendance of a person using face recognition with zero machine-human interface. If
this project were implemented, it would increase the productivity of the individual.
Despite significant advances in the field of face recognition, implementing face
recognition and verification in large scale and in real time has presented serious
challenges. Therefore, multiple Deep Convolutional Neural Networks in cascade are used
for face detection and recognition with a state-of-the-art classification algorithm.

### Prerequisites

[x] Ubuntu 16.04.x <br/>
[] MacOS <br/>
[x] Python 3.x <br/>
[x] OpenCV <br/>
[x] TensorFlow <br/>
[] Keras <br/>

## Running Face Recognition

1. Navigate to ```/face``` folder
2. Right click and open terminal from that folder
3. Type this to start the program::
``` 
python real_time.py
```
4. To stop the program, just click on the output window and click Q
5. For image testing
```
python real_time.py -- mode image
```

### To add people to the dataset

1. Make sure ```/face``` folder has the desired video of the person
2. In the ```face_recognition.py``` file, navigate to the ```add_faces()``` function
3. In the ```cv2.VideoCapture()``` function, enter the name of the video file as parameter
4. Navigate to the ```/face``` folder
5. Right click and open terminal from here
6. Start the training process by typing this in the terminal:
```
python real_time.py --mode input
```
7. The training will automatically stop and the person will be added to the dataset


## Authors

* **Raman Mohan** - [ramanmohan](https://github.com/ramanmohan)
* **Rajesh Kumar R**


## Acknowledgments

* Hat tip to anyone whose code was used

