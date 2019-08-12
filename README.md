# Real-time-human-pose-estimation-and-classification using OpenPose
This repository explains how OpenPose can be used for human pose estimation and activity classification. Availability of the two state of the art datasets namely MPII Human Pose dataset in 2015 and COCO keypoint dataset in 2016 gave a real boost to develop this field and pushed researchers to develop state of the art libraries for pose estimation of multiple people in a video using camera. One such state of the art library is [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) which is a real-time multi person system to detect keypoints. Using BODY_25 model, we get 25 body part key-points. We install this library on NVidia Jetson TX2 controller for mobile robotics task and develop a code that recognizes four poses of human (Standing, sitting, saying hello and stop) on the video being captured by Full HD USB video camera.
### Why OpenPose ?
OpenPose is a very efficient library in terms of running time and accuracy because other algorithms fail when number of people in the image is increased. The below figure  shows comparative performance of OpenPose with two other state of the art pose estimation libraries which are [AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) and [Mask R-CNN](https://github.com/matterport/Mask_RCNN). AlphaPose performs good when there are less than 5 people in the image but as the number of people increase, it becomes computationally expensive.
<p align="center">
  <img width="400" height="300" src="https://github.com/hafizas101/Real-time-human-pose-estimation-and-classification/blob/master/images/openpose_vs_competition.png">
</p>

### Methodology

<p align="center">
  <img width="1142" height="220" src="https://github.com/hafizas101/Real-time-human-pose-estimation-and-classification/blob/master/images/block%20dia.png">
</p>
1. Video from the USB camera is processed frame by frame. Some preprocessing steps are done on each frame which include: resizing image in term of reducing calculation complexity, blurring by gaussian kernel for reducing the noise. <br/>
2. We are using BODY_25 model of OpenPose and hence the frame processed by the pretrained OpenPose deep neural network stored in caffe format and this algorithm returns 25 possible key points (if finds) for each person in the order shown in the following figure.
<p align="center">
  <img width="550" height="900" src="https://github.com/hafizas101/Real-time-human-pose-estimation-and-classification/blob/master/images/body%2025.png">
</p>
3. Based on coordinates of key points and geometrical structure of human being, we recognize the pose as either 'hello', 'stop', 'sitting' and 'standing' using the proposed rule based approach.<br/>
4. The same process is repeated for the next frame.<br/>

### Installation of OpenPose
Installation of OpenPose on jetson tx2 is a challenging task as well. The official installation instructions to install OpenPose can fe found in (https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md). This blog (https://medium.com/pixel-wise/real-time-pose-estimation-in-webcam-using-openpose-python-2-3-opencv-91af0372c31c) explains the step by step instructions to install OpenPose on ubuntu and discusses all errors and issues as well.

### Pose classification
The script main.py is able to classify four human poses:<br/>
- Hello gesture
- Stop gesture
- Sitting pose
- Standing pose
For the recognition of first two poses (Say hello and stop), we pass right and left elbow and right and left wrist keypoints to the get_angle function. This function uses x,y coordinates of these keypoints and calculates angle of the forearm (line connecting elbow and wrist joints) for both arms. If one of the two angles is in the range of 30 to 150 degrees we classify it as Hello pose and if both angles  are in the range of 30 to 150 degrees, we classify it as Stop pose. The following figure illustrates this methodology. <br/>
<p align="center">
  <img width="654" height="657" src="https://github.com/hafizas101/Real-time-human-pose-estimation-and-classification/blob/master/images/hello-stop.png">
</p>
For the recognition of other two poses we use hip, knee and ankle keyoints for both the legs. The distance between hip and knee (l1) and distance between knee and ankle (l2) are calculated. If the ratio (l2/l1) is greater than a particular threshold, it is classified as a Sitting pose otherwise it is classified as Standing pose. The following figure illustrates this strategy.
<p align="center">
  <img width="678" height="505" src="https://github.com/hafizas101/Real-time-human-pose-estimation-and-classification/blob/master/images/sit-stand.png">
</p>

