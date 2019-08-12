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
  <img width="1142" height="220" src="https://github.com/hafizas101/Real-time-human-pose-estimation-and-classification/blob/master/images/body%2025.png">
</p>
3. Based on coordinates of key points and geometrical structure of human being, we recognize the pose as either 'hello', 'stop', 'sitting' and 'standing' using the proposed rule based approach.<br/>
4. The same process is repeated for the next frame.
