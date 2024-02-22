""" Visualization functions """
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.pyplot import colormaps


def show(image: np.ndarray, figsize: tuple[int, int] = (15, 7)) -> None:
    """Show the np.ndarray object """

    plt.figure(figsize=figsize)
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()


def result2show(image, result, cmap=colormaps['summer']) -> None:
    """
    Plot the original image and an empty white image for overlaying boxes and text
    A dictionary with the following keys and value types:
        - 'rec_texts': List of strings
        - 'rec_scores': List of floats
        - 'det_polygons': List of tuples [x1 y1 x2 y2 x3 y3 x4 y4] with four floats each
        - 'det_scores': List of floats

    """

    # plot image
    _, axis = plt.subplots(1, 2, figsize=(16, 16))
    axis[0].imshow(image, cmap='gray')
    axis[0].axis('off')

    # plot white image nearby
    white_img = np.ones_like(image, dtype=np.uint8)
    white_img.fill(255)
    axis[1].imshow(white_img, cmap='gray', vmin=0, vmax=255)
    axis[1].axis('off')

    # Iterate through the result dictionary
    for i in range(len(result['rec_texts'])):
        rec_texts = result['rec_texts'][i]
        rec_scores = result['rec_scores'][i]
        det_polygons = result['det_polygons'][i]
        det_scores = result['det_scores'][i]

        x_coord = [int(coord) for coord in det_polygons[0::2]]
        y_coord = [int(coord) for coord in det_polygons[1::2]]

        rect0 = patches.Polygon(
            xy=list(zip(x_coord, y_coord)),
            closed=True,
            fill=False,
            edgecolor=cmap(1 - det_scores),
            lw=1)

        rect1 = patches.Polygon(
            xy=list(zip(x_coord, y_coord)),
            closed=True,
            fill=True,
            facecolor=cmap(1 - rec_scores / 2.),
            edgecolor='green',
            lw=1)

        axis[0].add_patch(rect0)
        axis[1].add_patch(rect1)
        axis[1].text(x_coord[0],
                     np.mean(y_coord),
                     rec_texts.replace('$', r'\$'),
                     color='black',
                     fontsize=12,
                     va='center')

    plt.tight_layout()
