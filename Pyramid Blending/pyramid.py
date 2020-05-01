#Import the necessary libraries
import numpy as np
import cv2
import sys

class PyramidBlender():
	#preprocssing the images, creating masks subA, subB, final image mask
	def preprocess(self, img1, img2, overlap_w):
		w1 = img1.shape[1]
		w2 = img2.shape[1]
		
		#creata subA
		shape = np.array(img1.shape)
		shape[1] = w1 + w2 - overlap_w
		subA = np.zeros(shape)
		subA[:, :w1] = img1
		
		#create subB
		subB = np.zeros(shape)
		subB[:, w1 - overlap_w:] = img2
		
		#create mask for the final image
		mask = np.zeros(shape)    
		mask[:, :w1 - overlap_w / 2] = 1
		
		return subA, subB, mask

	# creates gaussian pyramid of a image given
	def GaussianPyramid(self, img, leveln):
		GA = img.copy()
		gpA = [GA]
		for i in xrange(leveln):
			GA = cv2.pyrDown(GA)
			gpA.append(np.float32(GA))
		return gpA
	
	# creates laplacian pyramid of a image given
	def LaplacianPyramid(self, img, leveln):
		g = self.GaussianPyramid(img, leveln)
		lp = [g[leveln-1]]
		for i in xrange(leveln-1,0,-1):
			L = np.subtract(g[i-1], cv2.pyrUp(g[i], dstsize=(g[i-1].shape[1::-1])))
			lp.append(L)
		return lp

	# blends LPA, LPB, MP on eanch level
	def blend_pyramid(self, LPA, LPB, MP, leveln):
		blended = []
		for i in range(0, leveln):
			blended.append(LPA[(leveln-1)-i] * MP[i] + LPB[(leveln-1)-i] * (1.0 - MP[i]))
		return blended

	# reconstructs the LS to create the blended large image
	def reconstruct(self, LS):
		img = LS[-1]
		for lev_img in LS[-2::-1]:
			img = cv2.pyrUp(img, dstsize=(lev_img.shape[1::-1]))
			img = img + lev_img
		return img

	# pyramid blending method
	def pyramid_blending(self, img1, img2, overlap_w):
		subA, subB, mask = self.preprocess(img1, img2, overlap_w)
		
		max_leveln = int(np.floor(np.log2(min(img1.shape[0], img1.shape[1], img2.shape[0], img2.shape[1]))))
		leveln = max_leveln
		
		# Get Gaussian pyramid and Laplacian pyramid
		MP = self.GaussianPyramid(mask, leveln)
		
		# Get Laplacian pyramid of subA and sunB
		LPA = self.LaplacianPyramid(subA, leveln)
		LPB = self.LaplacianPyramid(subB, leveln)
		
		# Blend two Laplacian pyramidspass
		blended = self.blend_pyramid(LPA, LPB, MP, leveln)
		
		# Reconstruction process
		result = self.reconstruct(blended)
		result[result > 255] = 255
		result[result < 0] = 0
		cv2.waitKey(0)
		return result

#load images
img1 = cv2.imread('l1.jpg')
img2 = cv2.imread('r1.jpg')
		
# define the overlapping area
overlap_w = 150

# main funtions
pb = PyramidBlender()		
result = pb.pyramid_blending(img1, img2, overlap_w)
cv2.imwrite('result1.jpg', result)
result = cv2.imread('result1.jpg')
cv2.imshow("Result", result)
cv2.waitKey(0)