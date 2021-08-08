import numpy as np
import matplotlib.pyplot as plt
import skimage.segmentation as seg
import skimage.color as color
from PIL import Image

def image_show(image, nrows=1, ncols=1):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 14))
    ax.imshow(image)
    ax.axis('off')
    return fig, ax

def circle_points(resolution, center, radius):
    radians = np.linspace(0, 2 * np.pi, resolution)
    c = center[1] + radius * np.cos(radians)  # polar co-ordinates
    r = center[0] + radius * np.sin(radians)
    return np.array([c, r]).T

def örnek():
    path = 'puppy.jpg'
    image = np.asarray(Image.open(path))
    image_gray = color.rgb2gray(image)
    points = circle_points(200, [465, 965],400)[:-1]
    snake = seg.active_contour(image_gray, points)

    fig, ax = image_show(image)
    ax.plot(points[:, 0], points[:, 1], '--r', lw=3)
    ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
    plt.show()