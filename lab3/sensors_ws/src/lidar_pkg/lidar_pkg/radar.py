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