#%%
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import h5py
import numpy as np
import matplotlib.pyplot as plt


h5f = h5py.File('TomoRec3D_13551.h5', 'r')
TomoRec3D_13551 = h5f['data'][:]
h5f.close()
#%%
image = TomoRec3D_13551[135,:,:]
image = image/np.max(image)
shapeX, shapeY = np.shape(image)

plt.figure()
plt.imshow(image, vmin=0.0, vmax=0.8, cmap="gray")
plt.title('Iterative FISTA-TV reconstruction')
plt.show()
#%%
# initialise curve for active countours
points_num = shapeX
index_crop = 1
x = np.linspace(index_crop, shapeX-index_crop, points_num)
y = np.linspace(index_crop, index_crop, points_num)
x = np.concatenate((x, np.linspace(index_crop, index_crop, points_num)))
y = np.concatenate((y, np.linspace(index_crop, shapeY-index_crop, points_num)))
x = np.concatenate((x, np.linspace(shapeX-index_crop, shapeX-index_crop, points_num)))
y = np.concatenate((y, np.linspace(shapeY-index_crop, index_crop, points_num)))
#s = np.linspace(0, 2*np.pi, 600)
#x = 300 + 200*np.cos(s)
#y = 270 + 260*np.sin(s)
init = np.array([x, y]).T
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(image, cmap=plt.cm.gray)
ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
plt.show()
#%%
snake = active_contour(gaussian(image, 3),
                       init, alpha=0.005, beta=0.5, gamma=0.001)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(image, cmap=plt.cm.gray)
ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, image.shape[1], image.shape[0], 0])
plt.show()
#%%
snake2 = snake.copy()
#snake2[:,0] = snake2[:,0] - 33*np.cos(s)
#snake2[:,1] = snake2[:,1] - 33*np.sin(s)
s = np.linspace(0, 2*np.pi, np.size(x,0))
snake2[:,0] = 45 + snake2[:,0] - 0.15*snake2[:,0]
snake2[:,1] = 35 + snake2[:,1] - 0.15*snake2[:,1]

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(image, cmap=plt.cm.gray)
ax.plot(snake[:, 0], snake[:, 1], '--r', lw=3)
ax.plot(snake2[:, 0], snake2[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, image.shape[1], image.shape[0], 0])
plt.show()
#%%
snake3 = active_contour(gaussian(image, 3),
                       snake2, alpha=0.05, beta=0.5, gamma=0.001)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(image, cmap=plt.cm.gray)
ax.plot(snake2[:, 0], snake2[:, 1], '--r', lw=3)
ax.plot(snake3[:, 0], snake3[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, image.shape[1], image.shape[0], 0])
plt.show()

#%%
snake4 = snake3.copy()
#snake2[:,0] = snake2[:,0] - 33*np.cos(s)
#snake2[:,1] = snake2[:,1] - 33*np.sin(s)
snake4[:,0] = 150 + snake4[:,0] - 0.4*snake4[:,0]
snake4[:,1] = 120 + snake4[:,1] - 0.4*snake4[:,1]

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(image, cmap=plt.cm.gray)
ax.plot(snake3[:, 0], snake3[:, 1], '--r', lw=3)
ax.plot(snake4[:, 0], snake4[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, image.shape[1], image.shape[0], 0])
plt.show()
#%%
#%%
snake5 = active_contour(gaussian(image, 3),
                       snake4, alpha=0.0001, beta=0.5, gamma=0.001)

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(image, cmap=plt.cm.gray)
ax.plot(snake4[:, 0], snake4[:, 1], '--r', lw=3)
ax.plot(snake5[:, 0], snake5[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, image.shape[1], image.shape[0], 0])
plt.show()
#%%
image2 = image.copy()

cordY = np.uint16(snake3[:, 0])
cordX = np.uint16(snake3[:, 1])

image2[cordX, cordY] = 0.0

import scipy.ndimage as ndimage    

# Create an empty image to store the masked array
r_mask = np.zeros_like(r, dtype='bool')

# Create a contour image by using the contour coordinates rounded to their nearest integer value
r_mask[np.round(contour[:, 0]).astype('int'), np.round(contour[:, 1]).astype('int')] = 1

# Fill in the hole created by the contour boundary
r_mask = ndimage.binary_fill_holes(r_mask)

# Invert the mask since you want pixels outside of the region
r_mask = ~r_mask

#%%
####################################################################
# using Morphological snakes from
# https://github.com/pmneila/morphsnakes
from morphsnakes import (morphological_chan_vese,
                         morphological_geodesic_active_contour,
                         inverse_gaussian_gradient, circle_level_set, checkerboard_level_set)

#image = TomoRec3D_13551[80:120,:,:]
#image = image/np.max(image)
#ls1 = circle_level_set(image.shape, (40, 300, 300), 70)

image = TomoRec3D_13551[85,:,:]
ls1 = circle_level_set(image.shape, (300, 300), 80)

# get outer liquer shape
#acwe_ls1 = morphological_chan_vese(image, iterations=250, smoothing=3, lambda1=1.0, lambda2=1.0, init_level_set=ls1)
# get the crystal 
acwe_ls2 = morphological_chan_vese(image, iterations=350, smoothing=3, lambda1=1.0, lambda2=0.025, init_level_set=ls1)

#gac_ls = morphological_geodesic_active_contour(image, iterations=60,init_level_set=acwe_ls1)
plt.figure()
plt.imshow(acwe_ls2[10,:,:], vmin=0.0, vmax=1, cmap="gray")
plt.title('Segmentation')
plt.show()
#%%
# performing morphological closing on segmeted images
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk


#segm = acwe_ls2[5,:,:]
segm_close = acwe_ls2.copy()
selem = disk(2)

#for i in range(0,100):
#    segm_close = binary_closing(segm_close).astype(np.int)

#eroded = erosion(segm_close, selem)
selem = disk(25)
#segm_dil = dilation(segm_close, selem)
segm_dil = closing(segm_close, selem)

plt.figure()
plt.imshow(segm_dil, vmin=0.0, vmax=1, cmap="gray")
plt.title('Closed Segmentation')
plt.show()
####################################################################
#%%
# using CV2 with Hough detection of lines
import cv2

image = TomoRec3D_13551[130,:,:]
image /= np.max(image)
kernel_size = 5
blur_gray = cv2.GaussianBlur(image,(kernel_size, kernel_size),0)
blur_gray /= np.max(blur_gray)

gray = (blur_gray*255).astype(np.uint8)
edges = cv2.Canny(gray, 1, 15, apertureSize = 3)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 70, maxLineGap=100)
for line in lines:
   x1, y1, x2, y2 = line[0]
   cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 128), 1)
cv2.imshow("linesEdges", edges)
cv2.imshow("linesDetected", gray)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#%%
image_crop = image[150:470,200:430]
(dx, dy)= np.gradient(image_crop)
magn = np.sqrt(dx**2 + dy**2)

magn[magn < 0.0085] = 0.0
magn[magn > 0.0085] = 1.0

plt.figure()
plt.imshow(magn, vmin=0.0, vmax=0.01, cmap="gray")
plt.show()

skel = morphology.skeletonize(magn)
out = morphology.binary_dilation(skel, morphology.selem.disk(1))
#%%
plt.figure()
plt.plot(image_crop[130,:])
plt.show()
#%%



