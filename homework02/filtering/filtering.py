""" Filtering function """
import numpy as np

def help_rgb(image: np.array, kernel: np.array, i: int, j: int, c: int) -> int:
    """ Help function for apply_rgb """
    s = 0
    for k1 in range(-(kernel.shape[0]//2), kernel.shape[1]//2 + 1):
        for k2 in range(-(kernel.shape[0]//2), kernel.shape[1]//2 + 1):
            if ((i+k1 < 0) or (j+k2 < 0) or (i+k1 >= image.shape[0]) or (j+k2 >= image.shape[1])):
                s = s + 0
            else:
                s = s + (kernel[kernel.shape[0]//2+k1][kernel.shape[0]//2+k2] * image[i+k1][j+k2][c])
    return s

def apply_rgb(image: np.array, kernel: np.array, newimage: np.array) -> np.array:
    """ Apply given filter on RGB image """
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for c in range(image.ndim):
                s = help_rgb(image, kernel, i, j, c)
                if s > 255:
                    newimage[i][j][c] = 255
                elif s < 0:
                    newimage[i][j][c] = 0
                else:
                    newimage[i][j][c] = s
    return newimage

def apply_bw(image: np.array, kernel: np.array, newimage: np.array) -> np.array:
    """ Apply given filter on balck-white image """
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            s = 0
            for k1 in range(-(kernel.shape[0]//2), kernel.shape[1]//2 + 1):
                for k2 in range(-(kernel.shape[0]//2), kernel.shape[1]//2 + 1):
                    # print(k1, k2)
                    if ((i+k1 < 0) or (j+k2 < 0) or (i+k1 >= image.shape[0]) or (j+k2 >= image.shape[1])):
                        s = s + 0
                    else:
                        s = s + (kernel[kernel.shape[0]//2+k1][kernel.shape[0]//2+k2] * image[i+k1][j+k2])
            if s > 255:
                newimage[i][j] = 255
            elif s < 0:
                newimage[i][j] = 0
            else:
                newimage[i][j] = s
    return newimage

def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """ Apply given filter on image """
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2 dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]
    if kernel.shape[0]%2 == 0:
        z = np.zeros((kernel.shape[0]+1,kernel.shape[1]+1), np.int8)
        for i in range(kernel.shape[0]):
            for j in range(kernel.shape[1]):
                z[i][j] = kernel[i][j]
        kernel=z
    newimage = image.copy()
    if image.ndim == 3:
        newimage = apply_rgb(image, kernel, newimage)
    else:
        newimage = apply_bw(image, kernel, newimage)
    return newimage
