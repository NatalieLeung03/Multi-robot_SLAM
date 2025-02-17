import rospy
from nav_msgs.msg import Odometry
import random

def add_noise(odom):
    noisy_odom = Odometry()
    noisy_odom.header = odom.header
    noisy_odom.pose = odom.pose
    noisy_odom.twist = odom.twist

    # Add Gaussian noise to position
    noisy_odom.pose.pose.position.x += random.gauss(0, 0.01)  # Mean 0, Std 0.01
    noisy_odom.pose.pose.position.y += random.gauss(0, 0.01)

    # Add Gaussian noise to orientation
    noisy_odom.pose.pose.orientation.x += random.gauss(0, 0.01)
    noisy_odom.pose.pose.orientation.y += random.gauss(0, 0.01)

    pub.publish(noisy_odom)

if __name__ == "__main__":
    rospy.init_node('odom_noise')
    sub = rospy.Subscriber('/odom', Odometry, add_noise)
    pub = rospy.Publisher('/odom_noisy', Odometry, queue_size=10)
    rospy.spin()
