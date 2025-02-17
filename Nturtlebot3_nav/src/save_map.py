#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np
from PIL import Image
from decimal import *

global map_data, width, height, map_img_data

def callback(data):
    global map_img_data 
    map_data = data.data
    width = data.info.width
    height = data.info.height
    map_img_data = [0] * (data.info.width * data.info.height)
    rospy.loginfo("Received a %s x %s map", width, height)
    
    # Get the file path from the ROS parameter server
    save_path = rospy.get_param('~save_path', '/home/natalie/maps/greyscale_image.png')
    #rospy.loginfo(f"Map will be saved at: {save_path}")
    getcontext().prec = 3
    # convert to ranging from 0 to 255
    #width, height = width , height
    length = width * height
    for i in range(length):
        if map_data[i] == -1:
            map_img_data[i] = 205
        else:
            mapdata = Decimal(map_data[i])
            percen = Decimal(1 - mapdata / 100)
            map_img_data[i] = Decimal(percen) * 255
            #rospy.loginfo("map data %s percen %s map img %s ", mapdata,percen, map_img_data[i])

    # Reshape the data to a 2D array
    map_img_data = np.array(map_img_data).reshape((height, width))
    
    # Convert the array to a grayscale image and save it
    map_img = Image.fromarray(map_img_data.astype(np.uint8))
    map_img.save(save_path)
    rospy.loginfo("Map saved to %s", save_path)
      

def save_map():
    rospy.init_node('save_map', anonymous=True)
    rospy.Subscriber("/map", OccupancyGrid, callback)
    rospy.loginfo("Waiting for the map...")
    rospy.spin()


if __name__ == '__main__':
    save_map()
    