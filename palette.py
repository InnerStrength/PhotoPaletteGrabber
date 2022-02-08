# --- Applet to import a photo image then analyze the pixels to document the colors
import os
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rd
import pandas as pd


class Palette:

    def __init__(self, img, size, sense):
        self.filename = img
        im = Image.open(f"static/img/{self.filename}")
        im = im.resize((100, int(((im.size[1] / im.size[0]) * 100))))
        self.rgb_im = im.convert('RGB')
        self.img_height = im.size[0]
        self.img_width = im.size[1]
        self.pixel_list = []
        self.color_list = {}
        self.size = int(size)
        self.sensitivity = int(sense)

    def make_palette(self):
        # --- Gather a list of each pixel
        for width in range(self.img_width):
            for height in range(self.img_height):
                r, g, b = self.rgb_im.getpixel((height, width))
                pixel = int('{:08b}{:08b}{:08b}'.format(r, g, b), 2)
                self.pixel_list.append(pixel)
        # --- Counts and removes pixel from the list
        while len(self.pixel_list) > 0:
            color_count = self.pixel_list.count(self.pixel_list[0])
            self.color_list[self.pixel_list[0]] = color_count
            self.pixel_list = list(filter((self.pixel_list[0]).__ne__, self.pixel_list))

        colors = pd.DataFrame(self.color_list.items(), columns=["Hex Number", "Counts"]) \
            .sort_values("Hex Number", ascending=False)
        colors = colors[colors.Counts > 1]
        colors = colors[colors["Hex Number"] > 0]
        K = self.size
        X = colors[["Hex Number", "Counts"]]

        Centroids = (X.sample(n=K))
        diff = 1
        j = 0

        while (diff != 0):
            XD = X
            i = 1
            for index1, row_c in Centroids.iterrows():
                ED = []
                for index2, row_d in XD.iterrows():
                    d1 = (row_c["Hex Number"] - row_d["Hex Number"]) ** 2
                    d2 = (row_c["Counts"] - row_d["Counts"]) ** 2
                    d = np.sqrt(d1 + d2)
                    ED.append(d)
                X[i] = ED
                i = i + 1

            C = []
            for index, row in X.iterrows():
                min_dist = row[1]
                pos = 1
                for i in range(K):
                    if row[i + 1] < min_dist:
                        min_dist = row[i + 1]
                        pos = i + 1
                C.append(pos)
            X["Cluster"] = C
            Centroids_new = X.groupby(["Cluster"]).mean()[["Counts", "Hex Number"]]
            if j == 0:
                diff = 1
                j = j + 1
            else:
                diff = (Centroids_new['Counts'] - Centroids['Counts']).sum() + (
                        Centroids_new['Hex Number'] - Centroids['Hex Number']).sum()
                # print(diff.sum())
            Centroids = X.groupby(["Cluster"]).mean()[["Counts", "Hex Number"]]

        plt.scatter(X["Hex Number"], X["Counts"], c="black")
        plt.scatter(Centroids["Hex Number"], Centroids["Counts"], c="red")
        plt.xlabel("Hex Number")
        plt.ylabel("Counts")
        plt.show()

        output = "<div class='palette'>"

        for color in Centroids["Hex Number"].values:
            cent_form = '{:08X}'.format(int(color))[2:]
            color = f'{cent_form}'
            output += f"<div style='width:75px; height:75px; background-color:#{color}; display:inline-block'></div>"

        output += "</div>"
        # os.remove(f'static/img/{self.filename}')
        return output
