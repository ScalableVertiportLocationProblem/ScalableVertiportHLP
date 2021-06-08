# @author liting

import numpy as np
import pandas as pd
import random
import math
import csv
import codecs
from collections import namedtuple
from math import radians, cos, sin, asin, sqrt
Coord = namedtuple("Coord", ['lat', 'longi'])
Vertex4=namedtuple("Vertex4",['p1','p2','p3','p4'])##from left upper to right upper clockwise

def haversine(p1, p2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [p1.longi, p1.lat, p2.longi, p2.lat])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def data_write_csv_wij(file_name, wij):
    wri_row=[]
    file_csv = codecs.open(file_name,'w+','utf-8')
    writer = csv.writer(file_csv, quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    for i in range(n*n):
        wri_row.append("wi%d"%i)
    writer.writerow(wri_row)
    for i in range(n*n):
        data2=[]
        for j in range(n*n):
            data2.append(wij[i][j])
        writer.writerow(data2)
def data_write_csv_cij(file_name, cij):
    wri_row=[]
    file_csv = codecs.open(file_name,'w+','utf-8')
    writer = csv.writer(file_csv, quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    for i in range(n*n):
        wri_row.append("ci%d"%i)
    writer.writerow(wri_row)
    for i in range(n*n):
        data2=[]
        for j in range(n*n):
            data2.append(cij[i][j])
        writer.writerow(data2)

class ProblemInstance:
    def __init__(self,dataset,n):
        self.dataset=dataset
        self.n=n ##the number of the grids every line and row
        self.N=n*n
        self.id_non_empty=[]
        self.loadDataFromFile(dataset)
        self.divide_into_grids()
        self.calculatewij()
        self.calculatecij()
        self.save()
    def loadDataFromFile(self,dataset):
        fn=pd.read_csv("%s.csv"%dataset)##requests
        self.origin=list(zip(fn.originLat.tolist(),fn.originLon.tolist()))
        self.destination=list(zip(fn.destinationLat.tolist(),fn.destinationLon.tolist()))


    def divide_into_grids(self):
        ## divide Beijing into grids
        ## row and column could be used in visualizaion
        city_lower1 = min(self.origin[i][0] for i in range(len(self.origin)))
        city_lower2 = min(self.destination[i][0] for i in range(len(self.origin)))
        self.city_lower= min(city_lower1,city_lower2)
        city_upper1= max(self.origin[i][0] for i in range(len(self.origin)))
        city_upper2= max(self.destination[i][0] for i in range(len(self.origin)))
        self.city_upper= max(city_upper1,city_upper2)
        city_left1 = min(self.origin[i][1] for i in range(len(self.origin)))
        city_left2 = min(self.destination[i][1] for i in range(len(self.origin)))
        self.city_left= min(city_left1,city_left2)
        city_right1 = max(self.origin[i][1] for i in range(len(self.origin)))
        city_right2 = max(self.destination[i][1] for i in range(len(self.origin)))
        self.city_right= max(city_right1,city_right2)
        self.city_center_lat=(self.city_upper+self.city_lower)/2
        self.city_center_long=(self.city_left+self.city_right)/2
        self.city_length = self.city_right-self.city_left##range of longitude
        self.city_width = self.city_upper-self.city_lower
        self.row = np.arange(self.city_left,self.city_right+self.city_length/n,self.city_length/n)##longitude
        self.column = np.arange(self.city_lower,self.city_upper+self.city_width/n,self.city_width/n)##latitude

    def calculatewij(self):
        ##wij frow grid i to grid j
        ##vertex4 the coordinates of the 4 vertexs of every grid
        ##the grid p1 p2
        ##         p4 p3
        ##the 0th grid is in the bottom left
        ##the n^2-1th grid is in the upper right
        n=self.n
        self.outflow=[0]*n*n
        self.wij=np.zeros((self.N,self.N))
        self.inflow=[0]*n*n
        self.vertex4=[0]*n*n
        self.center=[0]*n*n
        self.ssum=[0]*n*n
        for k in range(len(self.origin)):
            for i in range(self.n+1):
                ##longitude
                if self.origin[k][1]<self.row[i]:
                    row_of_origin=i-1
                    i+=1
                    break

            for j in range(self.n+1):
                if self.origin[k][0]<self.column[j]:
                    column_of_origin=j-1
                    j+=1
                    break
            origin_id = row_of_origin+column_of_origin*n
            self.outflow[origin_id]+=1

            for i in range(self.n+1):
                ##longitude
                if self.destination[k][1]<self.row[i]:
                    row_of_destination=i-1
                    i+=1
                    break

            for j in range(self.n+1):
                if self.destination[k][0]<self.column[j]:
                    column_of_destination=j-1
                    j+=1
                    break
            destination_id = row_of_destination+column_of_destination*n
            self.inflow[destination_id]+=1
            self.ssum[destination_id]=self.inflow[destination_id]+self.outflow[destination_id]
            self.wij[origin_id][destination_id]+=1

        for i in range (self.N):
            if self.ssum[i]>0:
                self.id_non_empty.append(i)
        y_interval= self.city_width/n ##latitude
        x_interval= self.city_length/n
        for i in range(self.n):
            for j in range(self.n):
                grid_id = i+j*self.n
                x1=self.city_left+i*x_interval
                x2=x1+x_interval
                y1=self.city_lower+j*y_interval
                y2=y1+y_interval
                p1=Coord(y2,x1)
                p2=Coord(y2,x2)
                p3=Coord(y1,x2)
                p4=Coord(y1,x1)
                self.vertex4[grid_id]=Vertex4(p1,p2,p3,p4)
                self.center[grid_id]=fun_fw(self.vertex4[grid_id])
    def calculatecij(self):
        self.cij=np.zeros((self.N,self.N))
        for i in range(self.N):
            for j in range(self.N):
                self.cij[i][j]=haversine(self.center[i],self.center[j])


    def save(self):
        data_write_csv_wij("./cw/wij%s.csv"%n,self.wij)
        data_write_csv_cij("./cw/cij%s.csv"%n,self.cij)

fun_fw= lambda grid : (Coord((grid.p1.lat+grid.p2.lat+grid.p3.lat+grid.p4.lat)/4,(grid.p1.longi+grid.p2.longi+grid.p3.longi+grid.p4.longi)/4))
if __name__=="__main__":

    dataset="requests"
    for n in range(3,35):
        print(n)
        problem=ProblemInstance(dataset,n)



