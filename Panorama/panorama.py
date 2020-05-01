# import the necessary libraries
import numpy as np
import imutils
import cv2

class ImageStitcher:
	# stich two images without using any blending algorithm
	# save the warped image that will be used by the pyramid blending script
	def stitch(self, imageA, imageB, ratio=0.75, reprojThresh=4.0):
	
		# convert the image to grayscale
		grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
		grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

		# detect and extract features from the images
		descriptorA = cv2.xfeatures2d.SIFT_create()
		kpsA, featuresA = descriptorA.detectAndCompute(imageA, None)
		descriptorB = cv2.xfeatures2d.SIFT_create()
		kpsB, featuresB = descriptorB.detectAndCompute(imageB, None)

		# convert the keypoints from KeyPoint objects to NumPy arrays
		kpsA = np.float32([kpA.pt for kpA in kpsA])
		kpsB = np.float32([kpB.pt for kpB in kpsB])
		
		# find mathes
		matcher = cv2.DescriptorMatcher_create("BruteForce")
		rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
		
		# list for good matches
		matches = []
		
		# go over the raw matches
		for m in rawMatches:
			# ensure the distance between matches is within a certain ratio of each
			# other (i.e. Lowe's ratio test)
			if len(m) == 2 and m[0].distance < m[1].distance * ratio:
				matches.append((m[0].trainIdx, m[0].queryIdx))

		# homography needs 4 matches
		if len(matches) > 4:
			# construct the two sets of points
			ptsA = np.float32([kpsA[i] for (_, i) in matches])
			ptsB = np.float32([kpsB[i] for (i, _) in matches])

			# compute the homography between the two sets of points, use RANSAC
			# reprojThres is used as the distance treshold by the RANSAC algorithm
			H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

		result = cv2.warpPerspective(imageA, H, (imageA.shape[1] + imageB.shape[1], imageB.shape[0]))
		cv2.imwrite('r2.jpg', result)
		
		result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

		# check to see if the keypoint matches should be visualized
		return result
		
# load the two images
imageA = cv2.imread("r1.jpg")
imageB = cv2.imread("l1.jpg")

# stitch the images together to create a panorama
s = ImageStitcher()
result = s.stitch(imageA, imageB)

cv2.imshow("Panorama", result)
cv2.waitKey(0)