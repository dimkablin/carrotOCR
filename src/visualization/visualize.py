""" Visualization functions """
import numpy as np
import matplotlib.pyplot as plt


def show(image: np.ndarray, figsize: tuple[int, int] =(15, 7)) -> None:
    """Show the np.ndarray object """

    plt.figure(figsize=figsize)
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()
