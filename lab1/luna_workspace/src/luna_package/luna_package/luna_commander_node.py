import random
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class LunaCommanderNode(Node):
    # Publishes velocity commands to move Luna around.

    def __init__(self) -> None:
        super().__init__('luna_commander')

        # One-off parameters
        self.declare_parameter('topic_name', 'cmd_vel')
        topic_name = self.get_parameter('topic_name').value

        # Continuously read parameters (can change them at runtime)
        ### ENTER CODE #########


        ########################
        # Timer uses the current value of period only at creation time
        ### ENTER CODE #########


        ########################
    
    def timer_callback(self) -> None:
        # Ask again for parameter values that may have changed
        v = self.get_parameter('linear_speed').value
        w = self.get_parameter('angular_speed').value

        ### ENTER CODE #########


        ########################
    
def main(args=None):
    try:
        rclpy.init(args=args)
        node = LunaCommanderNode()
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