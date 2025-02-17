import rospy
from sensor_msgs.msg import LaserScan
import random

def add_noise(scan):
    noisy_scan = LaserScan()
    noisy_scan.header = scan.header
    noisy_scan.angle_min = scan.angle_min
    noisy_scan.angle_max = scan.angle_max
    noisy_scan.angle_increment = scan.angle_increment
    noisy_scan.time_increment = scan.time_increment
    noisy_scan.scan_time = scan.scan_time
    noisy_scan.range_min = scan.range_min
    noisy_scan.range_max = scan.range_max

    # Add Gaussian noise to ranges
    noisy_scan.ranges = [r + random.gauss(0, 0.05) for r in scan.ranges]
    noisy_scan.intensities = scan.intensities

    pub.publish(noisy_scan)

if __name__ == "__main__":
    rospy.init_node('lidar_noise')
    sub = rospy.Subscriber('/scan', LaserScan, add_noise)
    pub = rospy.Publisher('/scan_noisy', LaserScan, queue_size=10)
    rospy.spin()
