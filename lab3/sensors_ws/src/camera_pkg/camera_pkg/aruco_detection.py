import numpy as np
import json
import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from camera_pkg.math_utils import rot_to_quat
from visualization_msgs.msg import Marker

class ArucoDetector(Node):
    def __init__(self):
        super().__init__("aruco_detector")

        self.bridge = CvBridge()

        # Create subscriber
        ####### ENTER CODE HERE #######


        ###############################

        # Create publisher
        ####### ENTER CODE HERE #######


        ###############################
        
        self.tf_broadcaster = TransformBroadcaster(self)

        # Aruco dictionary + parameters
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()

        # Load JSON file
        with open("src/camera_pkg/camera_pkg/camera_params.json", "r") as f:
            data = json.load(f)

        # Input your camera number
        ####### ENTER CODE HERE #######


        ###############################
        self.camera_matrix = np.array(data["camera_parameters"][str(camera_params_num)]["camera_matrix"]) # camera/intrinsic matrix
        self.dist_coeffs = np.array(data["camera_parameters"][str(camera_params_num)]["dist_coeffs"])  # distortion coefficients

        ####### ENTER CODE HERE #######


        ###############################

        # Smoothing state
        self.filtered_tvec = None
        self.filtered_q = None

        # Params to control image filtering
        self.declare_parameter("smoothing", True)
        self.declare_parameter("alpha", 0.3)

    def image_callback(self, msg: Image):
        """
        This method is called whenever the subscriber receives a new image.
        Convert it to CV Image frame and try to detect an aruco marker.
        """

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        self.detect_aruco(frame)
    
    def filter_pose(self, tvec: np.ndarray, q: np.ndarray):
        """
        Apply exponential moving average to translation and quaternion.
        tvec: shape (3,)
        q:    shape (4,) [x, y, z, w]
        """

        use_smoothing = self.get_parameter("smoothing").get_parameter_value().bool_value
        alpha = self.get_parameter("alpha").get_parameter_value().double_value

        if not use_smoothing:
            # Do not apply filter
            return tvec, q
        
        # Initialize the first time
        if self.filtered_tvec is None or self.filtered_q is None:
            self.filtered_tvec = tvec.copy()
            self.filtered_q = q.copy()
            return tvec, q
        
        # Exponential moving average
        self.filtered_tvec = (1. - alpha) * self.filtered_tvec + alpha * tvec
        self.filtered_q = (1.0 - alpha) * self.filtered_q + alpha * q

        # Renormalize quaternion
        self.filtered_q = self.filtered_q / np.linalg.norm(self.filtered_q)

        return self.filtered_tvec, self.filtered_q
    
    def detect_aruco(self, frame):
        """
        Detects ArUco markers in the given image frame, estimates the 3D pose
        (rotation and translation) of the first detected marker relative to the
        camera frame, and publishes the corresponding TF transform.
        """

        self.marker_length = self.get_parameter("marker_length").value

        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, self.aruco_dict, parameters=self.aruco_params
        )

        if ids is not None:
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, self.marker_length,
                self.camera_matrix, self.dist_coeffs
            )

            # First detected aruco marker pose
            tvec = tvecs[0][0]
            rvec = rvecs[0][0]

            # Calculate rotation matrix and convert to quaternion
            R, _ = cv2.Rodrigues(rvec)
            q = rot_to_quat(R)

            # Apply filter
            ####### ENTER CODE HERE #######


            ###############################

            # Construct message
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = "camera_link"
            t.child_frame_id = "aruco_marker"

            # Put spatial info in message
            ####### ENTER CODE HERE #######


            ###############################

            # Publish message to /tf
            self.tf_broadcaster.sendTransform(t)

            # Create the marker message
            marker = Marker()
            marker.header.stamp = t.header.stamp
            marker.header.frame_id = "camera_link"

            marker.ns = "aruco_board"
            marker.id = 0
            marker.type = Marker.CUBE
            marker.action = Marker.ADD

            # Marker pose in camera frame
            ####### ENTER CODE HERE #######


            ###############################
            
            # Marker size
            ####### ENTER CODE HERE #######


            ###############################
            marker.scale.z = 0.001

            # Marker colour
            marker.color.r = 0.8
            marker.color.g = 0.8
            marker.color.b = 0.8
            marker.color.a = 1.0

            self.marker_publisher.publish(marker)


def main(args = None):
    try:
        rclpy.init(args = args)
        node = ArucoDetector()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()