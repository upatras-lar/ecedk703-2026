import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32
import pyCandle
import sys
import math


class DoublePendulumNode(Node):
    def __init__(self):
        super().__init__("double_pendulum_node")
        
        # Initialize the double pendulum
        candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True, pyCandle.USB)

        # Check if motors are available
        motor_ids = candle.ping(pyCandle.CAN_BAUD_1M)
        self.get_logger().info(f"Motor ids: {motor_ids}")
        if len(motor_ids) == 0: sys.exit("EXIT FAILURE")

        # Add all found motor drives to the update list
        for id in motor_ids:  
            candle.addMd80(id)

        # Reset all encoders at 0 and enable the motor drives
        for id in motor_ids:
            candle.controlMd80SetEncoderZero(id)
            candle.controlMd80Mode(id, pyCandle.IMPEDANCE)
            candle.controlMd80Enable(id, True)
        
        # Begin auto-update loop for the data in candle.md80s vector
        candle.begin()

        self.shoulder_motor = candle.md80s[1]
        self.elbow_motor = candle.md80s[0]

        # Set the PD Controller gains for each motor
        self.shoulder_motor.setImpedanceControllerParams(0.2, 0.02)
        self.elbow_motor.setImpedanceControllerParams(0.2, 0.02)

        # Create publisher for the joint states (position and velocity)
        ############ ENTER CODE HERE ###############


        ############################################

        # Create subscription for the equilibrium point
        ############ ENTER CODE HERE ###############


        ############################################

    def timer_callback(self) -> None:
        """
        This function is periodically called by the timer. It publishes the current state (position and velocity)
        of the pendulum to the /joint_states topic.
        """

        # Create the message with the time stamp
        state_msg = JointState()
        state_msg.header.stamp = self.get_clock().now().to_msg()

        # Set the joint names (joint1: shoulder joint, joint2: elbow joint)
        state_msg.name = ["joint1", "joint2"]

        # Set the joint positions
        state_msg.position = [float(self.shoulder_motor.getPosition()), float(self.elbow_motor.getPosition())]

        # Set the velocity positions
        ############ ENTER CODE HERE ###############


        ############################################

        # Publish the message
        self.state_publisher.publish(state_msg)

        # Print the current position and velocity of the joints
        self.get_logger().info(f"{state_msg.name[0]}: Position {state_msg.position[0]}, Velocity: {state_msg.velocity[0]} \n{state_msg.name[1]}: Position {state_msg.position[1]}, Velocity: {state_msg.velocity[1]}")

    def subscriber_callback(self, msg: Int32) -> None:
        """
        This function is called by the control subscriber. Whenever it receives a command message, it uses the controllers to reach
        the desired equilibrium position.

        Equilibrium Point 1 --> shoulder = 0 rad, elbow = 0 rad
        Equilibrium Point 2 --> shoulder = 0 rad, elbow = pi rad
        Equilibrium Point 3 --> shoulder = pi rad, elbow = pi rad
        Equilibrium Point 4 --> shoulder = pi rad, elbow = 0 rad
        """

        # Read the command message
        equilibrium_point = msg.data

        # Give the appropriate motor command (depending on the message)
        if equilibrium_point == 1:
            self.shoulder_motor.setTargetPosition(0.0)
            self.elbow_motor.setTargetPosition(0.0)
        elif equilibrium_point == 2:
        ############ ENTER CODE HERE (delete pass) ################
            pass

        ###########################################################
        elif equilibrium_point == 3:
        ############ ENTER CODE HERE  (delete pass) ###############
            pass

        ##########################################################
        elif equilibrium_point == 4:
        ############ ENTER CODE HERE (delete pass) ###############
            pass

        ##########################################################
        else:
            pass

def main(args = None):
    try:
        rclpy.init(args = args)
        node = DoublePendulumNode()
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