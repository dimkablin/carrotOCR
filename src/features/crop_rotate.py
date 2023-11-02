# import numpy as np
# import cv2
# from skimage.color import rgb2gray
# from skimage.transform import rotate
# from skimage.transform import (hough_line, hough_line_peaks)
# from scipy.stats import mode
# from skimage import io
# from skimage.filters import threshold_otsu, sobel

# def binarizeImage(RGB_image:np.array) -> np.array:
#     image = rgb2gray(RGB_image)
#     threshold = threshold_otsu(image)
#     bina_image = image < threshold
#     return bina_image


# def findEdges(bina_image:np.array) -> np.array:
#     image_edges = sobel(bina_image)
#     return image_edges


# def findTiltAngle(image_edges:np.array) -> int:
#     h, theta, d = hough_line(image_edges)
#     accum, angles, dists = hough_line_peaks(h, theta, d)
#     angle = np.rad2deg(mode(angles)[0][0])
  
#     if (angle < 0):
#         r_angle = angle + 90
#     else:
#         r_angle = - 90 + 180
#     origin = np.array((0, image_edges.shape[1]))

#     for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
#         y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)

#     return r_angle

  
# def rotateImage(RGB_image:np.array, angle:int):
#     fixed_image = rotate(RGB_image, angle)
#     return fixed_image


# def cropped(img_path:str) -> np.array:
#     img = cv2.imdecode(np.fromfile(img_path, dtype=np.int32), 1)
#     h, w = img.shape[:2]
#     if w >= h:
#         img = img[0:h,0:int(w/(1.1*(w/h)))]
#     else:
#         img = img[0:int(h/(1.1*(h/w))), 0:w]

#     return img


# def generalPipeline(img_path:str) -> np.array:
#     image = cropped(img_path)
#     bina_image = binarizeImage(image)
#     image_edges = findEdges(bina_image)
#     angle = findTiltAngle(image_edges)
#     return rotateImage(cropped(img_path), angle)