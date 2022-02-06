from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os


def showing_image(image_name, spline=False, tck=None):
    """

    :param image_name: the name of the image that user uploaded
    :param spline: default is False. If True, it will use the _spline function
    opens the image in PIL and give it axis in matplotlib so the user can insert tck easier
    also calls function _splines
    """
    cwd = os.getcwd()
    file_dir = os.path.join(cwd, 'static', image_name)

    try:
        image = Image.open(file_dir, 'r')
    except:
        return "couldn't open image file"

    width, height = image.size
    image = np.flipud(image)
    plt.xlim([0, width])
    plt.ylim([0, height])

    if spline:
        image_name_png = image_name.split('.')[0] + '_result.png'
        file_dir = os.path.join(cwd, 'static', image_name_png)

        return _splines(tck, image, file_dir, image_name_png)

    else:
        image_name_png = image_name.split('.')[0] + '.png'
        file_dir = os.path.join(cwd, 'static', image_name_png)

        plt.imshow(image, aspect='auto')

        xticks = np.linspace(0, width, 10, dtype=int)
        yticks = np.linspace(0, height, 10, dtype=int)

        plt.xticks(xticks)
        plt.yticks(yticks)

        plt.grid(color="black", alpha=0.5)

        plt.savefig(file_dir, bbox_inches='tight', pad_inches=0, dpi=300)

        return image_name_png, image_name


def _splines(tck, image, file_dir, image_name):
    """
    calculates the splines with any degree
    then plots the result on the image
    """
    from scipy import interpolate
    tck = [np.array(tck[0]), [np.array(tck[1][0]), np.array(tck[1][1])], np.array(tck[2])]

    height = image.shape[0]
    width = image.shape[1]
    if any(height < tck[1][1]) or any(width < tck[1][0]):
        return 1, True

    l = len(tck[1][1])
    array_of_points = np.linspace(0, 1, (max(l * 2, 100)), endpoint=True)

    x = tck[1][0]
    y = tck[1][1]

    plt.plot(x, y, 'r:', marker='o', markerfacecolor='green')

    out = interpolate.splev(array_of_points, tck)

    plt.fill(x, y, c='green', alpha=0.2)

    plt.plot(out[0], out[1], 'r')

    fig = plt.imshow(image, aspect='auto')

    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    plt.savefig(file_dir, bbox_inches='tight', pad_inches=0, dpi=300)
    return image_name, False
