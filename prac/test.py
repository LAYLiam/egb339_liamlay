import machinevisiontoolbox as mvt
from matplotlib import pyplot as plt
import numpy as np
from typing import Tuple
import cv2
import os
import sys


WSP_MARKERS = np.array([
    [117.7, 154.8],
    [297.7, 154.8],
    [297.7, -165.2],
    [117.7, -165.2],
])

def GetBlobsFromImg(
        img: mvt.Image, 
        sigma: int = 1, 
        h: int = 1, 
        thresh: float = 0.4,
        kernel: Tuple[int, int] = np.ones((3, 3)),
        filter: int = 200,
    ) -> Tuple[int, int, int]:
    img_temp = img.copy()

    img = np.power(img, np.ones(img.shape)*0.45)
    K_gauss = mvt.Kernel.Gauss(sigma, h)
    img = img.convolve(K_gauss)

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    Y = R + G + B

    r = np.divide(np.asarray(R), np.asarray(Y))
    g = np.divide(np.asarray(G), np.asarray(Y))
    b = np.divide(np.asarray(B), np.asarray(Y))

    def OpenClose(img: mvt.Image) -> mvt.Image:
        opened = img.open(kernel)
        closed = opened.close(kernel)
        return closed 

    red = OpenClose(r >= thresh)
    green = OpenClose(g >= thresh) 
    blue = OpenClose(b >= thresh) 

    # red.disp()
    # green.disp()
    # blue.disp(block=True)

    red_blobs = red.blobs().filter(area=filter)
    green_blobs = green.blobs().filter(area=filter)
    blue_blobs = blue.blobs().filter(area=filter)

    img_temp.disp()
    red_blobs.plot_box(color="r", linewidth=2)
    green_blobs.plot_box(color="g", linewidth=2)
    blue_blobs.plot_box(color="b", linewidth=2)

    # print(red_blobs)
    # print(green_blobs)
    # print(blue_blobs)

    return red_blobs, green_blobs, blue_blobs


def GetMarkersAndPositions(blobs):
    red_blobs, green_blobs, blue_blobs = blobs

    shapes = {}
    markers = []

    # assign colour and shape to each blob
    for colour, blobs in [
            ("red", red_blobs), 
            ("green", green_blobs), 
            ("blue", blue_blobs)
        ]:
        for blob in blobs:
            if blob.circularity > 0.925:
                if colour == "red":
                    markers.append(blob)
                else:
                    shapes[f"{colour} circle"] = blob.centroid
            elif blob.circularity > 0.75:
                shapes[f"{colour} square"] = blob.centroid
            else:
                shapes[f"{colour} triangle"] = blob.centroid

    return OrderMarkers(markers), shapes


def OrderMarkers(markers):
    points = [m.centroid for m in markers]
    biggest_marker_index = np.argmax([m.area for m in markers])
    A = points[biggest_marker_index]

    x1, y1 = A
    x2, y2 = np.array(points)[:, 0], np.array(points)[:, 1]
    euclid_dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    C = points[np.argmax(euclid_dist)]

    midx, midy = ((C[0] - x1)/2) + x1, ((C[1] - y1)/2) + y1
    point_angle_relative_to_mid = [np.arctan2((p[1]-midy),(p[0]-midx)) for p in points]
    index_map = list(np.argsort(point_angle_relative_to_mid))
    index_A = index_map.index(biggest_marker_index)
    index_map = np.array(index_map[index_A:] + index_map[:index_A])

    return np.array(points)[index_map]


if __name__ == "__main__":
    path = r"""C:\Users\liaml\Git\egb339_liamlay\assignment_2_3_vision\VisionExampleImages-2024"""
    files = os.listdir(path)

    if len(sys.argv) > 1:
        files = [files[int(sys.argv[1]) if len(sys.argv) > 1 else 0]]

    for i, filename in enumerate(files):
        print(f"id: {sys.argv[1] if len(sys.argv) > 1 else i}, {filename}", end=' ')
        img = mvt.Image.Read(path + "\\" + filename)

        im_markers, im_poisitions = GetMarkersAndPositions(GetBlobsFromImg(img))
        # print(im_markers)
        # print(im_poisitions)
        print(f"{len(im_poisitions)} shapes")

        for shape, position in im_poisitions.items():
            plt.text(round(position[0]), round(position[1]), shape)

        for i, marker in enumerate(im_markers):
            plt.text(round(marker[0]), round(marker[1]), f"Marker {i}")

        plt.show(block=True)


