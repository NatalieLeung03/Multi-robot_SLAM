#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np
from PIL import Image
from decimal import *

class save_map:

    def __init__(self):
        # initialize variables
        self.last_saved = 0
        self.last_savedtb3_0 = 0
        self.last_savedtb3_1 = 0        
        self.date = '2903'
        self.save_path = rospy.get_param("~save_path")                                                                                                                                                  
        self.multi_robot = 'false'

        # subscribe to the map topic
        if self.multi_robot == 'true':
            rospy.Subscriber("/map", OccupancyGrid, self.callback, callback_args='main')
            rospy.Subscriber("/tb3_0/map", OccupancyGrid, self.callback, callback_args='tb3_0')
            rospy.Subscriber("/tb3_1/map", OccupancyGrid, self.callback, callback_args='tb3_1')
        else:
            rospy.Subscriber("/map", OccupancyGrid, self.callback, callback_args='main')                
        
    def callback(self, data, robot_namespace):
        # change date
        date=self.date
        # Get the map data and info
        map_data = data.data
        width = data.info.width
        height = data.info.height
        map_img_data = [0] * (data.info.width * data.info.height)
        rospy.loginfo("Received a %s x %s map", width, height)
        
        # Get parameters
        save_path = self.save_path
                
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
        # Reshape the data to a 2D array
        map_img_data = np.array(map_img_data).reshape((height, width))
        
        # Convert the array to a grayscale image and save it
        map_img = Image.fromarray(map_img_data.astype(np.uint8))
        now = rospy.get_rostime()

        # Save the map, counter using namespace
        if robot_namespace == 'main':
            last_saved = self.last_saved
            t=now.secs - last_saved
            rospy.loginfo("Time since last save %s", t)
            if t > 10:     
                save_path = save_path + date + '_' + str(now.secs) + '_' + robot_namespace + '.png'
                map_img.save(save_path)
                self.last_saved = now.secs
                rospy.loginfo("Map saved to %s", save_path)
        elif robot_namespace == 'tb3_0':
            last_saved = self.last_savedtb3_0
            t=now.secs - last_saved
            rospy.loginfo("Time since last save %s", t)
            if t > 10:     
                save_path = save_path + date + '_' + str(now.secs) + '_' + robot_namespace + '.png'
                map_img.save(save_path)
                self.last_savedtb3_0 = now.secs
                rospy.loginfo("Map saved to %s", save_path)
        elif robot_namespace == 'tb3_1':
            last_saved = self.last_savedtb3_1
            t=now.secs - last_saved
            rospy.loginfo("Time since last save %s", t)
            if t > 10:     
                save_path = save_path + date + '_' + str(now.secs) + '_' + robot_namespace + '.png'
                map_img.save(save_path)
                self.last_savedtb3_1 = now.secs
                rospy.loginfo("Map saved to %s", save_path)                

def main():
    # Initialize the node
    rospy.init_node('save_map', anonymous=True)
    save_map()    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS save_map module")

if __name__ == '__main__':
    main()   
    