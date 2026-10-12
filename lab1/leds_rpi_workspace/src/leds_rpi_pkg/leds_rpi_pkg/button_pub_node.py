import rclpy
from rclpy.node import Node
import RPi.GPIO as rpigpio
from leds_rpi_pkg_interfaces.msg import LedValue


class ButtonPublisherNode(Node):
    def __init__(self):
        super().__init__("button_publisher")

        # Our button is connected to pin number 3
        self.pin_button = 3

        # This pin is for input
        rpigpio.setmode(rpigpio.BCM)
        rpigpio.setup(self.pin_button, rpigpio.IN)

        # Current state of the button
        ### ENTER CODE #########


        ########################

        # Create the publisher
        ### ENTER CODE #########


        ########################

        # Create a timer
        ### ENTER CODE #########


        ########################

        self.get_logger().info("Button publisher node has been started!")

    def send_button_state(self):
        '''
        This function is periodically called by the timer.
        It checks the state of the button and publishes the appropriate message.
        '''
        # Read the state of the button (!!! Inverted logic !!! When the button is pressed, it's state is 0. When it is not pressed, it's 1)
        self.button_state = 1 - rpigpio.input(self.pin_button)

        # Create the message
        ### ENTER CODE #########


        ########################

        # Publish the message
        ### ENTER CODE #########


        ########################
        
def main(args = None):
    try:
        rclpy.init(args = args)
        button_node = ButtonPublisherNode()
        rclpy.spin(button_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if button_node is not None:
            button_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
