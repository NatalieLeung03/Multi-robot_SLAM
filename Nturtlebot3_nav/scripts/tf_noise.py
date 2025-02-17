#!/usr/bin/env python

import rospy
import tf
import tf2_ros
import numpy as np
from geometry_msgs.msg import TransformStamped

def add_noise_to_transform(transform, noise_std_dev):
    noisy_transform = TransformStamped()
    noisy_transform.header = transform.header
    noisy_transform.child_frame_id = transform.child_frame_id

    # Add Gaussian noise to translation
    noisy_transform.transform.translation.x = transform.transform.translation.x + np.random.normal(0, noise_std_dev)
    noisy_transform.transform.translation.y = transform.transform.translation.y + np.random.normal(0, noise_std_dev)
    noisy_transform.transform.translation.z = transform.transform.translation.z + np.random.normal(0, noise_std_dev)

    # Add Gaussian noise to rotation
    noisy_quat = [
        transform.transform.rotation.x + np.random.normal(0, noise_std_dev),
        transform.transform.rotation.y + np.random.normal(0, noise_std_dev),
        transform.transform.rotation.z + np.random.normal(0, noise_std_dev),
        transform.transform.rotation.w + np.random.normal(0, noise_std_dev)
    ]

    # Normalize quaternion to ensure it's valid
    norm = np.linalg.norm(noisy_quat)
    noisy_transform.transform.rotation.x = noisy_quat[0] / norm
    noisy_transform.transform.rotation.y = noisy_quat[1] / norm
    noisy_transform.transform.rotation.z = noisy_quat[2] / norm
    noisy_transform.transform.rotation.w = noisy_quat[3] / norm

    return noisy_transform

def tf_noise():
    rospy.init_node('tf_noise')
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    broadcaster = tf2_ros.TransformBroadcaster()

    noise_std_dev = rospy.get_param('~noise_std_dev', 0.01)  # Standard deviation of the noise
    input_frame = rospy.get_param('~input_frame', 'odom')
    output_frame = rospy.get_param('~output_frame', 'base_link')
    noisy_frame = rospy.get_param('~noisy_frame', 'base_link_noisy')

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        try:
            # Get the transformation from the input_frame to the output_frame
            transform = tf_buffer.lookup_transform(input_frame, output_frame, rospy.Time(0))
            
            # Add noise to the transformation
            noisy_transform = add_noise_to_transform(transform, noise_std_dev)
            
            # Update the child frame ID for the noisy transform
            noisy_transform.child_frame_id = noisy_frame
            
            # Publish the noisy transformation
            broadcaster.sendTransform(noisy_transform)

        except tf2_ros.LookupException:
            rospy.logwarn("Transform not available yet.")
        except tf2_ros.ExtrapolationException:
            rospy.logwarn("Transform extrapolation error.")
        rate.sleep()

if __name__ == '__main__':
    try:
        tf_noise()
    except rospy.ROSInterruptException:
        pass
