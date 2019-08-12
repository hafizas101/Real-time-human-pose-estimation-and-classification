# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
from math import sqrt, acos, degrees, atan, degrees
import numpy as np

# ----------------------------------------- Arslan Part ----------------------------------------------------------------------------------
def get_angle(a,b):
    #print(a)
    #print(b)
    del_y = a[1]-b[1]
    del_x = b[0]-a[0]
    if del_x == 0:
        del_x = 0.1
    #print("Del_X : "+str(del_x)+"-----Del_Y: "+str(del_y))
    angle = 0

    if del_x > 0 and del_y > 0:
        angle = degrees(atan(del_y / del_x))
    elif del_x < 0 and del_y > 0:
        angle = degrees(atan(del_y / del_x)) + 180

    return angle

# ------------------------------------------------------------------------------------------------------------------------------------------	

# ----------------------------------------- Maksim Part ----------------------------------------------------------------------------------

def angle_gor(a,b,c,d):
    ab=[a[0]-b[0],a[1]-b[1]]
    ab1=[c[0]-d[0],c[1]-d[1]]
    cos=abs(ab[0]*ab1[0]+ab[1]*ab1[1])/(sqrt(ab[0]**2+ab[1]**2)*sqrt(ab1[0]**2+ab1[1]**2))
    ang = acos(cos)
    return ang*180/np.pi


def sit_ang(a,b,c,d):
	ang=angle_gor(a,b,c,d)
	s1=0
	if ang != None:
		#print("Angle",ang)
		if ang < 120 and ang>40:
			s1=1
	return s1

def sit_rec(a,b,c,d):
	ab = [a[0] - b[0], a[1] - b[1]]
	ab1 = [c[0] - d[0], c[1] - d[1]]
	l1=sqrt(ab[0]**2+ab[1]**2)
	l2=sqrt(ab1[0]**2+ab1[1]**2)
	s=0
	if l1!=0 and l2!=0:
		#print(l1,l2, "---------->>>")
		if l2/l1>=1.5:
			s=1
	return s
	
# ------------------------------------------------------------------------------------------------------------------------------------------	

# ----------------------------------------------------------- OpenPose Example Code ----------------------------------------------------------
	
# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.) 
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.) 
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/home/nvidia/openpose/models/"

# Add others in path?
for i in range(0, len(args[1])):
    curr_item = args[1][i]
    if i != len(args[1])-1: next_item = args[1][i+1]
    else: next_item = "1"
    if "--" in curr_item and "--" in next_item:
        key = curr_item.replace('-','')
        if key not in params:  params[key] = "1"
    elif "--" in curr_item and "--" not in next_item:
        key = curr_item.replace('-','')
        if key not in params: params[key] = next_item

# Construct it from system arguments
# op.init_argv(args[1])
# oppython = op.OpenposePython()

c=0
# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# ------------------------------------------------------- OUR CONTRIBUTIONS ----------------------------------------------------------------

cam = cv2.VideoCapture(1)
for i in range(1000):
	# Process Image
	datum = op.Datum()
	s, im = cam.read() # captures image
	#cv2.imshow("Test Picture", im) # displays captured image
	#im=cv2.resize(im,(480,270), interpolation = cv2.INTER_AREA)
	image1 = im
	#imageToProcess = cv2.imread(args[0].image_path)
	c+=1
	if c==8:
		c=0
		datum.cvInputData = image1
		opWrapper.emplaceAndPop([datum])     # OpenPose being applied to the frame image.
		# Display Image
		#print("Body keypoints: \n" + str(datum.poseKeypoints))
		#print(datum.poseKeypoints.shape)
		if len(datum.poseKeypoints.shape)>=2:
			x1=0
			x2=0

			for j in range(len(datum.poseKeypoints)):
				x1=0
				x2=0
				s=0
				s1=0
				ang1 = get_angle(datum.poseKeypoints[j][3], datum.poseKeypoints[j][4])
				ang2 = get_angle(datum.poseKeypoints[j][6], datum.poseKeypoints[j][7])
				if (30 < ang1 < 150):
				    x1 = 1
				if (30 < ang2 < 150):
				    x2 = 1
				x3 = x1+x2
				if (x3 == 1):
				    print("The {} person says: HELLO !".format(j+1))
				    #cv2.putText(datum.cvOutputData,'OpenPose using Python-OpenCV',(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1,cv2.LINE_AA)
				elif (x3 == 2):
				    print("The {} person says: STOP PLEASE !".format(j+1))
				s += sit_rec(datum.poseKeypoints[j][9], datum.poseKeypoints[j][10],datum.poseKeypoints[j][10],datum.poseKeypoints[j][11])
				s += sit_rec(datum.poseKeypoints[j][12], datum.poseKeypoints[j][13],datum.poseKeypoints[j][13],datum.poseKeypoints[j][14])
				s1+=sit_ang(datum.poseKeypoints[j][9], datum.poseKeypoints[j][10],datum.poseKeypoints[j][10],datum.poseKeypoints[j][11])
				s1+=sit_ang(datum.poseKeypoints[j][12], datum.poseKeypoints[j][13],datum.poseKeypoints[j][13],datum.poseKeypoints[j][14])
				if s > 0 or s1>0:
				    print("The {} person is sitting".format(j+1))
				if s == 0 and s1 == 0:
				    print("The {} person is standing".format(j+1))
			print("___________________________")
			print("      ")
			im=cv2.resize(datum.cvOutputData,(960,540), interpolation = cv2.INTER_AREA)
			cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", im)
			cv2.waitKey(1)
			
			
# ------------------------------------------------------------------------------------------------------------------------------------------