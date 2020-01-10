import numpy as np
import cv2


image=cv2.IMREAD_GRAYSCALE(file_path)

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        # find the black pixels
        if image[i,j,0]==0 and image[i,j,1]==0 and image[i,j,2]==0: 
            image[i,]

# cv2.imwrite('result.png',image)