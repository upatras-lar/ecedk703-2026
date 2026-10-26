import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from pymycobot.myarm import MyArm
import math
import time

class SliderControlNode(Node):
    def __init__(self):
        super().__init__("slider_control")

        # Connection port as configurable parameter
        self.declare_parameter('port', '/dev/ttyAMA0')
        port = self.get_parameter('port').value

        # Connection baud rate as configurable parameter
        self.declare_parameter('baudrate', 115200)
        baudrate = self.get_parameter('baudrate').value

        # Print the connection settings
        self.get_logger().info(f"Connecting to port: {port}, with baudrate: {baudrate}")

        # Joint speed as configurable parameter (0-100)
        self.declare_parameter('joint_speed', 80)
        joint_speed = self.get_parameter('joint_speed').value

        # Create arm object
        self.mc = MyArm(port = port, baudrate = baudrate, timeout = 1.0)
        time.sleep(0.1)

        # Set mode: 1 always execute latest command first, 0 to execute in a queue
        self.mc.set_fresh_mode(mode = 1)
        time.sleep(0.1)

        # Set the arm to zero configuration
        self.mc.set_encoders([2048, 2048, 2048, 2048, 2048, 2048, 2048], joint_speed) 

        # Create publisher and timer for the joint states
        ############ ENTER CODE HERE ###############


        ############################################

        # Create subscriber to read the joint states targets from the GUI sliders
        ############ ENTER CODE HERE ###############


        ############################################
    
    def publish_states(self) -> None:
        """
        This function is periodically called by the timer. It publishes the current state (joint angles)
        of the arm's joints to the /joint_states topic.
        """

        # Create the message with the time stamp
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()

        # Set the joint names
        msg.name = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"]

        # Read the current positions of th joints (in degrees)
        joint_angles_list = self.mc.get_angles()
       
       # Convert the joint angles to radians
        positions = []
        for angle_deg in joint_angles_list:
            angle_rad = round(math.radians(angle_deg), 3)
            positions.append(angle_rad)

        # Set joint positions
        msg.position = positions

        # Publish the message
        ############ ENTER CODE HERE ###############


        ############################################

    def move_arm(self, msg: JointState) -> None:
        """
        This function is used to move the arm to the desired position by reading JointState messages
        from the GUI sliders.
        """

        # Read the desired positions from the message
        joint_angles_list = []
        for angle_rad in msg.position:
            angle_deg = round(math.degrees(angle_rad), 3)
            joint_angles_list.append(angle_deg)

        # Read the desired speed (parameter value)
        joint_speed = max(1, min(int(self.get_parameter('joint_speed').value), 100))

        # Move the arm to the desired position at the desired speed
        ############ ENTER CODE HERE ###############


        ############################################

def main(args = None):
    try:
        rclpy.init(args = args)
        node = SliderControlNode()
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