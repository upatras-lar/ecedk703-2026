import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D

class LunaDriverNode(Node):
    # The Luna Driver is a very simple integrator that updates a pose from cmd_vel

    def __init__(self) -> None:
        super().__init__('luna_driver')

        # One-off parameters
        self.declare_parameter('cmd_topic', 'cmd_vel')
        self.declare_parameter('pose_topic', 'pose')
        self.declare_parameter('publish_period', 2.)

        ### ENTER CODE #########


        ########################

        ### ENTER CODE #########


        ########################

        self.x = 0.
        self.y = 0.
        self.theta = 0.
        self.last_twist = Twist()

        self.timer = self.create_timer(self.dt, self.calculate_pose)
    
    def execute_command(self, msg: Twist) -> None:
        self.last_twist = msg
        v = self.last_twist.linear.x
        w = self.last_twist.angular.z

        # Simple integration
        self.theta += w * self.dt
        self.x += (v * math.cos(self.theta)) * self.dt
        self.y += (v * math.sin(self.theta)) * self.dt
    
    def calculate_pose(self) -> None:
        msg = Pose2D(x=self.x, y=self.y, theta=self.theta)
        self.pub.publish(msg)
        self.get_logger().info(f'Pose -> x: {self.x:.2f}, y: {self.y:.2f}, theta: {self.theta:.2f}')

def main(args=None):
    try:
        rclpy.init(args=args)
        node = LunaDriverNode()
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

if __name__ == '__main__':
    main()