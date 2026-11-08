# ROS2 Laboratory 4 – Sensors, Cameras and LiDAR

In the previous lab we used **RViz2** and **RQT** to visualize the state of simulated robots (the double pendulum and the myArm 300 Pi) using topics, TF, and URDF descriptions.

In this lab we'll connect ROS2 to **real hardware sensors**:

- a **USB camera** that publishes images, and
- a **2D LiDAR** that publishes distance measurements around the robot.

We will use the ROS2 tools you already know (nodes, topics, parameters, launch files, RViz2) to:

- bring sensor data into ROS2,
- process it in our own nodes, and
- visualize the results in RViz2.

The lab is split into two big parts:

1. Working with the **camera** (`camera_pkg`)
2. Working with the **LiDAR** (`lidar_pkg` + `rplidar_ros`)

## Workspace layout and build

For this lab we will use the `sensors_ws` workspace that lives inside `lab4`:

- `camera_pkg` – code and launch files for the USB camera exercises
- `lidar_pkg` – code and launch files for the LiDAR exercises
- `rplidar_ros` – the driver package that talks to the physical RPLIDAR sensor
- `v4l2_camera` – the driver package that communicates with the physical camera

## 1. The USB Camera

In the first half of the lab we will use a **USB camera** connected to the Raspberry Pi. A ROS2 node from the `v4l2_camera` package will publish images, and our own node in `camera_pkg` will detect an **ArUco marker** and estimate its 3D pose.

We will visualize everything in RViz2.

### 1.1 The camera pipeline

The overall camera pipeline looks like this:

```text
USB camera
   │
   ▼
v4l2_camera node
   │
   |
/image_raw  (sensor_msgs/msg/Image)
   │
   └──► ArucoDetector node      (subscribes to /image_raw,
   |                             publishes TF and a visualization Marker)
   │
   ▼
RViz2 (Image + Marker + TF displays)
```

The configuration for the `v4l2_camera` node is stored in:

```text
camera_pkg/config/camera_info.yaml
```

The RViz2 config for the camera part of the lab is:

```text
camera_pkg/config/rviz/config.rviz
```

---

### 1.2 ArUco marker detection and pose estimation

The camera exercise uses **ArUco markers**, which are small black-and‑white square patterns that can be uniquely identified and whose 3D pose can be estimated from a single image using the camera intrinsics. We want to be able to detect an aruco marker with our camera and visualize it in RViz. We will use the camera frame as our reference frame.

The `ArucoDetector` node:

- subscribes to the camera image topic,
- detects aruco markers using OpenCV  and estimates their 3D pose
- publishes a TF transform from the **camera frame** to the aruco **marker frame**, and
- publishes a `visualization_msgs/msg/Marker` so that the marker pose is visible in RViz2.

The code for this lives in `camera_pkg/camera_pkg/aruco_detection.py`:

```python
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
```

> **Student TODO I:** Create a subscriber to listen to our camera. It should:
> - receive `Image` type messages,
> - listen to the `/image_raw` topic and
> - calls the `image_callback` function to try to detect the aruco marker 

> **Student TODO II:** In order to visualize our aruco marker, we need to publish a `Marker` message containing information like the shape, position etc. of the marker. Create a publisher that:
> - publishes `Marker` type messages at the `\marker` 
> - We don't need a timer this time! We will only publish our marker when we detect an aruco marker in the image.

> **Student TODO III:** In order to correctly detect the aruco marker, we need to know its length. As you can see we have two different sized markers in front of us. It makes sense to define the marker length as a configurable parameter. 
> - Declare `marker_length` as a configurable parameter with an initial value of 0.05m
> - Save it as a class member variable `self.marker_length` to be easily accessible from all the class functions.

> **Student TODO IV:** Each camera has different configuration parameters. Without these, the distances we calculate when using the camera will be wrong. Each camera is marked with a number on it.
> - Create a `camera_params_num` variable and set it its value to your camera number. This will let the program find the correct set of configuration parameters for your camera.

> **Student TODO V:** After we have detected and found the translation and rotation of an aruco marker relative to the camera frame, we want to apply an exponential moving average filter so that our data is smoother. As you can see we have already built `filter_pose` as a class member.
> - Use `filter_pose` on our marker spatial data. Remember to use the filtered values of our data!

> **Student TODO VI:** In `__init__` we created a instance of `TransformBroadcaster(self)`. We can use it to send `TransformStamped` type messages to the `/tf` topic. This is the topic that Rviz listens to. This means that Rviz will know where the marker frame is in relation to the camera frame and display it.
> - Inspect the format of the `TransformStamped` message type with `ros2 interface show geometry_msgs/msg/TransformStamped`
> - Insert the translation and rotation (quaternion) information into our `TransformStamped` message. 

> **Student TODO VII:** Lastly, we want to place visual marker (i.e. a small box) in our marker frame. This is just to visually represent the aruco marker.Remember, Rviz already knows where the aruco marker frame is because we published the `TransformBroadcaster` message to `/tf`.
> - Fill our the `pose.position.x`, `pose.position.y` and `pose.position.z` of our `Marker` message. Remember to use the filtered values of our data!
> - Fill out the `scale.x` and `scale.y` fields of our `Marker` message. They should be equal to the real size of our aruco marker. Remember, we already defined this as a configurable parameter. 

---

### 1.3 Launching the camera stack

We provide a launch file that wires everything together `camera_pkg/launch/camera_launch.py`.

It will:

- start the `v4l2_camera` driver node,
- start the camera processing nodes from `camera_pkg`, and
- open RViz2 with the correct config file.

To launch it:

```bash
colcon build --packages-select camera_pkg
source install/setup.bash
ros2 launch camera_pkg camera_launch.py
```

If everything is working:

- the camera LED should turn on,
- RViz2 should open, showing the live camera image, and
- additional displays (markers, axes, etc.)

> **Student TODO:** Use the printed aruco marker that was provided to you. Move it in front of the camera. Is everything working as epxected?  
> - Use `ros2 topic echo /tf` to see the transformation messages published to RViz.  
> - Is the translation that you are seeing correct?

## 2. The 2D LiDAR

In the second half of the lab we work with a **2D LiDAR** (RPLIDAR).  
The LiDAR continuously scans the environment and publishes a **LaserScan** message, which contains a set of distances and angles around the sensor.

We will:

- start the **LiDAR driver** (`rplidar_ros`),
- implement a **Radar** node that monitors a region in front of the sensor, and
- visualize both the raw scan and our processed output in RViz2.

### 2.1 Understanding LaserScan messages

The LiDAR driver publishes messages of type `sensor_msgs/msg/LaserScan` on a topic usually called `/scan`.

To inspect the message type:

```bash
ros2 interface show sensor_msgs/msg/LaserScan
```

Key fields:

- `angle_min`, `angle_max` – the start and end angle of the scan (radians)
- `angle_increment` – angular resolution between consecutive range measurements
- `range_min`, `range_max` – valid measurement range
- `ranges[]` – array of distance measurements (meters)
---

### 2.2 The Radar node – a virtual laser tripwire

In this exercise we will user the lidar sensor to built a radar. The idea is that we will define a cone area in front of the lidar and a minimum trigger distance. If an object enters that are a red marker should appear on Rviz, indicating where the obstacle is.
The **Radar** node (implemented in `lidar_pkg/lidar_pkg/radar.py`) behaves like a **virtual tripwire**:

- It looks at a **sector** of the LiDAR scan (for example ±20° around the front),
- finds the **closest obstacle** in that sector, and
- raises a **visual alert** (a Marker in RViz2) when something is closer than a threshold distance.

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
import math


class Radar(Node):
    def __init__(self):
        super().__init__('laser_tripwire_node')

        # Declare parameters
        ####### ENTER CODE HERE #######


        ###############################


        # Create Subscriber
        ####### ENTER CODE HERE #######


        ###############################


        # Create Publisher for RViz marker
        ####### ENTER CODE HERE #######


        ###############################


        self.get_logger().info('Radar node started.')

    def scan_callback(self, msg: LaserScan):

        min_angle_deg = self.get_parameter('min_radar_angle').value
        max_angle_deg = self.get_parameter('max_radar_angle').value
        trigger_dist = self.get_parameter('trigger_distance').value

        min_angle = math.radians(min_angle_deg)
        max_angle = math.radians(max_angle_deg)

        closest_range = None
        closest_angle = None

        for i, r in enumerate(msg.ranges):
            if math.isinf(r) or math.isnan(r):
                continue

            angle = msg.angle_min + i * msg.angle_increment

            if angle < min_angle or angle > max_angle:
                continue

            if closest_range is None or r < closest_range:
                closest_range = r
                closest_angle = angle

        # No obstacle inside cone: delete marker
        if closest_range is None:
            self.clear_marker(msg.header)
            return

        # Obstacle too far away: clear marker
        if closest_range >= trigger_dist:
            self.clear_marker(msg.header)
            return

        # In any other case: call publish_marker
        ####### ENTER CODE HERE #######


        ###############################


        self.get_logger().info(
            f'PING! Obstacle {closest_range:.2f} m at {math.degrees(closest_angle):.1f}°'
        )
    
    def clear_marker(self, header):
        """
        Clear the obstacle Marker
        """
        marker = Marker()
        marker.header.frame_id = header.frame_id
        marker.header.stamp = header.stamp
        marker.ns = 'radar'
        marker.id = 1
        marker.action = Marker.DELETE
        self.marker_pub.publish(marker)



    def publish_marker(self, dist, angle, header):
        """
        Publish a red sphere where the obstacle is detected.
        """
        marker = Marker()
        marker.header.frame_id = header.frame_id
        marker.header.stamp = header.stamp
        marker.ns = 'radar'
        marker.id = 1
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        # Position in the laser frame
        marker.pose.position.x = dist * math.cos(angle)
        marker.pose.position.y = dist * math.sin(angle)
        marker.pose.position.z = 0.0

        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05

        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        marker.lifetime.sec = 0

        # Publish the marker
        ####### ENTER CODE HERE #######


        ###############################


def main(args = None):
    try:
        rclpy.init(args = args)
        node = Radar()
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
```

> **Student TODO I:** Create a subscriber to listen to the lidar's data. The subscriber:
> - Listens to the `/scan` topic, receives `LaserScan` type messages and uses `scan_callback` as its callback function.

> **Student TODO II:** Create a publisher named `marker_pub` to publish `Marker` type messages. The publisher:
> - Publishes to the `/radar_marker` topic and sends `Marker` type messages.

> **Student TODO III:** We want to declare some of our radar's properties as configurable parameters. Specifically:
> - The range of our cone represented by a `min_radar_angle` and `max_radar_angle` (in degrees).
> - The minimum trigger distance in meters represented by: `trigger_distance`

> **Student TODO IV:** In our scan callback, if the obstacle is within our trigger distance and angle range we should publish a marker. As you can see, we have built a `publish_marker` method in our class.
> - Use the `publish_marker` of our class when an obstacle is within range.

> **Student TODO V:** Finally, in our `publish_marker` method we construct the `Marker` message. Now all we have to do is use our publisher to publish it:
> - Use our publisher to publisher the `Marker` message.

---

### 2.3 Launching the LiDAR stack

The launch file for the LiDAR exercise is `lidar_pkg/launch/lidar_launch.py`.

It:

- launches the appropriate `rplidar_ros` driver node,
- launches our **Radar** node from `lidar_pkg`, and
- starts RViz2 with a ready-made configuration file

To launch everything:

```bash
colcon build --packages-select lidar_pkg
source install/setup.bash
ros2 launch lidar_pkg lidar_launch.py
```

If everything is correct:

- the LiDAR should start spinning,
- RViz2 should show a 2D point cloud or colored scan and
- if an obstacle is within radar range, it should appear as a red marker

> **Student TODO:** While the radar is running:
> - Move obstacles in and out of the radar's range. Is everything working properly?
> - Inspect the scan messages being received with `ros2 topic echo /scan`
> - Inspect the marker messages being published with `ros2 topic echo /radar_marker`