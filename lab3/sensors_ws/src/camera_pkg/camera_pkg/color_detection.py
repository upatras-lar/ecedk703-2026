#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point


class ColorDetector(Node):
    def __init__(self):
        super().__init__("color_detector")

        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, "/camera/image_raw", self.callback, 10
        )

        self.pub = self.create_publisher(Point, "/color_target_centroid", 10)

        # HSV thresholds for RED (students modify)
        self.lower = np.array([0,120,70])
        self.upper = np.array([10,255,255])

    def callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)

        M = cv2.moments(mask)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            p = Point()
            p.x = float(cx)
            p.y = float(cy)
            p.z = 0.0
            self.pub.publish(p)


def main():
    rclpy.init()
    node = ColorDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
