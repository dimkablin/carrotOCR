import PIL.Image as Image
import cv2
import numpy as np


def cut_image(image: Image.Image, k=1.4142) -> Image.Image:
    """ Changing size of the image from (w, h) to (new_w, k * new_w) where new_w equals to min(w, h)

    :param image: An Image.Image object representing input image
    :param k: A coefficient that shows how much longer the length is than the width
    :return: An Image.Image object
    """

    assert len(image.size) == 2, f"image dim has to be equal to 2, but image.shape has {len(image.size)} dim."

    width, height = image.size
    height = int(min(k * width, height))
    image = image.crop((0, 0, width, height))

    return image


def check_exif(image: Image.Image) -> Image.Image:
    """ Checking exif attribute

    :param image: An Image.Image object
    :return: An Image.Image rotated object according to the attribute
    """
    if hasattr(image, '_getexif') and image._getexif() is not None:
        exif = dict(image._getexif().items())

        if exif.get(274) == 3:
            image = image.rotate(180, expand=True)
        elif exif.get(274) == 6:
            image = image.rotate(270, expand=True)
        elif exif.get(274) == 8:
            image = image.rotate(90, expand=True)

    return image


def open_image(url: str) -> Image.Image:
    """ Open an image

    :param url: A string object representing the path to the image file
    :return: An Image.Image object representing the output image.
    """

    image = Image.open(url)
    image = check_exif(image)

    return image


def PILtoNumpy(image: Image.Image) -> np.ndarray:
    """ Convert a PIL image to a NumPy array.

    :param image: An Image.Image object representing the input image.
    :return: A NumPy array representing the image.
    """

    return np.array(image)


def grayscale(image: Image.Image) -> Image.Image:
    """ Converting image from _ to GRAY

    :param image: image (Image.Image): The input image.
    :return: A grayscale version of the input image.
    """

    image = image.convert('L')
    return image


def blur(image: np.ndarray,
         kernel: tuple[int, int] = (3, 3),
         sigma: int = 3) -> np.ndarray:
    """ Apply Gaussian blur to the input image.

    :param image: The input image as a NumPy array.
    :param kernel: A tuple specifying the size of the Gaussian blur kernel (width, height).
    :param sigma: The standard deviation of the Gaussian blur. Higher values result in stronger blur.
    :return: The blurred image as a NumPy array.
    """

    image = cv2.GaussianBlur(image, kernel, sigma)
    return image


def denoising(image: np.ndarray,
              kernel: np.ndarray = np.ones((3, 3), np.uint8),
              iterations: int = 1) -> np.ndarray:
    """ Apply denoising to the input image.

    :param image: A NumPy array representing the input image.
    :param kernel: A NumPy array representing the kernel for erosion and dilation operations.
                   By default, it's a 2x2 matrix with data type np.uint8.
    :param iterations: The number of times the erosion and dilation operations are applied.
    :return: A NumPy array representing the denoised image.
    """

    image = cv2.erode(image, kernel, iterations=iterations)
    image = cv2.dilate(image, kernel, iterations=iterations)
    return image


def clahe(image: np.ndarray,
          clipLimit: int = 2,
          tileGridSize: tuple[int, int] = (8, 8)) -> np.ndarray:
    """ Apply clahe histogram equalization

    :param image: The input image (grayscale).
    :param clipLimit: The contrast limit for CLAHE.
    :param tileGridSize: The size of the grid for histogram equalization. Default is (8, 8).
    :return: The contrast-enhanced image.
    """

    clahe_ = cv2.createCLAHE(clipLimit, tileGridSize)
    image = clahe_.apply(image)

    return image


def threshold(image: np.ndarray,
              thresh: int = 220,
              maxval: int = 255) -> np.ndarray:
    """ Apply thresholding to the input image.

    :param image: A NumPy array representing the input image.
    :param thresh: The threshold value used for binarization. Pixels below this value become 0.
    :param maxval: The maximum value assigned to pixels that exceed the threshold.
    :return: A NumPy array representing the thresholded image.
    """

    _, image = cv2.threshold(image, thresh, maxval, cv2.THRESH_BINARY)
    return image


def contrast_enhancement(image: np.ndarray) -> np.ndarray:
    """ Enhance the contrast of the input image.

    :param image: A NumPy array representing the input image.
    :return: A NumPy array representing the contrast-enhanced image.
    """

    min_val, max_val, _, _ = cv2.minMaxLoc(image)
    image = cv2.convertScaleAbs(image,
                                alpha=255.0 / (max_val - min_val),
                                beta=-min_val * (255.0 / (max_val - min_val))
                                )

    return image


def sobel_filter(image: np.ndarray,
                 ksize: int = 3) -> np.ndarray:
    """ Apply Sobel filter to the input image

    :param image: A NumPy array representing the input image
    :param ksize: The kernel size of sobel filter
    :return: A NumPy array representing edge-enhanced image
    """

    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize)
    image = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

    return image


def invert(image: np.ndarray) -> np.ndarray:
    """ Invert thr colors of the input image

    :param image: A NumPy array representing the input image.
    :return: A NumPy array representing the inverted image.
    """

    image = cv2.bitwise_not(image)
    return image
