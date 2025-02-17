import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np

class MapSaver:
    def __init__(self, mapname):
        self.mapname = mapname
        self.saved_map = False
        rospy.init_node('map_saver', anonymous=True)
        rospy.Subscriber("/map", OccupancyGrid, self.map_callback)
        rospy.loginfo("Waiting for the map...")
        rospy.spin()

    def map_callback(self, msg):
        if self.saved_map:
            return
        
        rospy.loginfo(f"Received a {msg.info.width} x {msg.info.height} map @ {msg.info.resolution:.3f} m/pix")
        mapdatafile = f"{self.mapname}.pgm"
        
        # Convert occupancy data to a numpy array
        data = np.array(msg.data, dtype=np.int8).reshape((msg.info.height, msg.info.width))
        data = np.where(data == -1, 205, data)  # Unknown pixels to gray
        data = np.where(data == 0, 254, data)   # Free space to white
        data = np.where(data == 100, 0, data)   # Occupied space to black
        
        # Write PGM file
        with open(mapdatafile, "wb") as f:
            f.write(f"P5\n{msg.info.width} {msg.info.height}\n255\n".encode())
            f.write(bytearray(data.flatten()))
        
        rospy.loginfo(f"Map saved to {mapdatafile}")
        self.saved_map = True

if __name__ == "__main__":
    try:
        map_saver = MapSaver("map")
    except rospy.ROSInterruptException:
        pass
