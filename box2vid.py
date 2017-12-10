import cv2
import imageio
import math

coordinates = []

'''
Reads the box coordinates for each frame from the .box file.
Populates the list 'coordinates' with coordinates of all the boxes,
indexed by the number of frame.
The coordinates i.e., x1, y1, x2, y2 of ith box in nth frame are given by:
coordinates[n][i*4: i*4+4]
'''
def readCoordinates(file):
	lines = file.readlines()
	for i in lines:
		# convert to a list of floats
		coor = list(map(float, i.strip().split()))
		coor = [math.floor(x) for x in coor]
		coordinates.append(coor[2:]) # ignore frame no. & box count
		
'''
Check to see if coordinates are mismatching i.e., not in proper point pairs
'''
def checkCoordinates():
	n = len(coordinates)
	for i in range(n):
		if len(coordinates[i]) % 4 is not 0:
			print("Frame #",i,"is faulty")
			exit(1)
	
'''
Annotates a given frame by drawing bounding boxes. The coordinates of two opposite points of
boxes are given as a list.
RETURNS: labelled frame as numpy.array
'''
def annotateFrame(img, coor):
	for i in range(0, len(coor), 4):
		cv2.rectangle(img, (coor[i], coor[i+1]), (coor[i+2], coor[i+3]), (0,0,255), 2)
	return img

'''
Extracts frames from the given video file.
USES annotateFrame() to draw boxes on each frame. Then,
it combines the frames to form a new video file and saves it on disk.
'''
def iterVideo(file):
	# input video
	inVideo = cv2.VideoCapture(file)
	print("Input ready: ", inVideo.isOpened())

	# output settings
	fps = 30.0
	# make sure width and height match the source
	width = 1920
	height = 1080
	outVideo = cv2.VideoWriter(file[:-4]+"_annotated.avi", cv2.VideoWriter_fourcc(*'DIVX'), fps, (width,height))
	print("Output ready: ", outVideo.isOpened())

	# reading and writing
	success, image = inVideo.read()
	num = 0 # frame number

	while success:
		img = annotateFrame(image, coordinates[num])
		# show frame number
		#cv2.putText(img, str(num), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
		outVideo.write(img)
		# save frame as image
		#cv2.imwrite(str(num)+".jpg", img)
		success, image = inVideo.read()
		num += 1
	
	# close the video
	inVideo.release()
	outVideo.release()

		
if __name__ == '__main__':
	identifier = input("Enter the name OR relative path of the video along with extension: ")
	box = open(identifier+".box", "r")

	readCoordinates(box)
#	checkCoordinates()
	
	iterVideo(identifier)