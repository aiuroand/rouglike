""" Filtering function """
import numpy as np

def apply_filter(image: np.array, kernel: np.array) -> np.array:
    """ Apply given filter on image """
    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    # A given filter has to be 2 dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]
    if kernel.shape[0]%2 == 0:
        z = np.zeros((3,3), np.int8)
        z[0][0] = kernel[0][0]
        z[0][1] = kernel[0][1]
        z[1][0] = kernel[1][0]
        z[1][1] = kernel[1][1]
        kernel=z
    newimage = image.copy()
    if image.ndim == 3:
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                for c in range(image.ndim):
                    s = 0
                    for k1 in range(-(kernel.shape[0]//2), kernel.shape[1]//2 + 1):
                        for k2 in range(-(kernel.shape[0]//2), kernel.shape[1]//2 + 1):
                            # print(k1, k2)
                            if ((i+k1 < 0) or (j+k2 < 0) or (i+k1 >= image.shape[0]) or (j+k2 >= image.shape[1])):
                                s = s + 0
                            else:
                                s = s + (kernel[kernel.shape[0]//2+k1][kernel.shape[0]//2+k2] * image[i+k1][j+k2][c])
                    # print(s)
                    if s > 255:
                        newimage[i][j][c] = 255
                    elif s < 0:
                        newimage[i][j][c] = 0
                    else:
                        newimage[i][j][c] = s
    else:
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
                # print(s)
                if s > 255:
                    newimage[i][j] = 255
                elif s < 0:
                    newimage[i][j] = 0
                else:
                    newimage[i][j] = s
    return newimage
