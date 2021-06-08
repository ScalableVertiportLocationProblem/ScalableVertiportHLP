
import numpy as np
import pandas as pd
import random
import math
import csv
import codecs

from PIL import Image
from skimage.transform import resize
from collections import namedtuple
from math import radians, cos, sin, asin, sqrt
Coord = namedtuple("Coord", ['lat', 'longi'])
Vertex4=namedtuple("Vertex4",['p1','p2','p3','p4'])##from left upper to right upper clockwise

def data_write_csv_non_hub(file_name, non_hub):
    wri_row=[]
    file_csv = codecs.open(file_name,'w+','utf-8')
    writer = csv.writer(file_csv, quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    wri_row.append("non_hub")
    writer.writerow(wri_row)
    writer.writerow(non_hub)


class ProblemInstance:
    def __init__(self,n):
        self.n=n ##the number of the grids every line and row
        self.N=n*n
        self.non_hub()
        data_write_csv_non_hub("./non_hub_area/non_hub%s.csv"%n,self.l_non_hub)
    def non_hub(self):
        #Load image
        base=self.n
        data=np.array(Image.open('Base.png').convert('RGBA'))
        #Transform to b/w
        red,green,blue,alpha = data.T
        visible=(alpha>0)
        data[..., :-1][visible.T] =(0, 0, 0)
        #Resize to NxN
        dataResized=resize(data, (base, base),anti_aliasing=False,mode="constant")
        #Avoid semi-transparent pixels
        red,green,blue,alpha=dataResized.T
        visible=(alpha>0)
        non_hub_boolean=visible.T

        self.l_non_hub=[]
        for i in range(base):
            for j in range(base):
                if non_hub_boolean[i][j]!=0:
                    self.l_non_hub.append((base-1-i)*base+j)


if __name__=="__main__":
    for n in range(3,35):
        print(n)
        problem=ProblemInstance(n)



