# import the necessary packages
import cv2

#reference point for area of interest
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
	global refPt, cropping
 
	if cropping == True:
		# if crooping is enabled draw a rectangle around the region of interest
		image = clone.copy()
		cv2.rectangle(image, refPt[0], (x,y), (0, 0, 255), 1)
		cv2.imshow("image", image)
	
	# if left mouse click start drawing the cropping area
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
	
	# if right mosue click stop drawing the area 	
	if event == cv2.EVENT_RBUTTONDOWN:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		cropping = False
		refPt.append((x,y))
		cv2.rectangle(image, refPt[0], (x,y), (0, 0, 255), 1)
		cv2.imshow("image1", image)
		
image = cv2.imread("result1.jpg")
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break
 
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	cv2.imshow("ROI", roi)
	cv2.imwrite("cropped.jpg", roi)
	cv2.waitKey(0)
 
# close all open windows
cv2.destroyAllWindows()