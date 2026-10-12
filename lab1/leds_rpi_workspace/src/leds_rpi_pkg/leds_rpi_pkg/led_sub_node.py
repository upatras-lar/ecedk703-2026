import rclpy
from rclpy.node import Node
import RPi.GPIO as rpigpio
from leds_rpi_pkg_interfaces.msg import LedValue


class LedSubscriberNode(Node):
    def __init__(self):
        super().__init__("led_subscriber")
        
        # Our LED is connected to pin number 4
        self.pin_led = 4

        # This pin is for output
        rpigpio.setmode(rpigpio.BCM)
        rpigpio.setup(self.pin_led, rpigpio.OUT)

        # Create the subscriber
        ### ENTER CODE #########


        ########################

    def led_subscriber_callback(self, msg: LedValue):
        '''
        This function reads a LedValue message and turns the LED on/off accordingly
        '''
        # Read the message
        ### ENTER CODE #########


        ########################
        # Output the message value to the LED
        ### ENTER CODE #########


        ########################
        # Print the result
        ### ENTER CODE #########


        ########################

def main(args = None):
    try:
        rclpy.init(args = args)
        blink_led_subscriber_node = LedSubscriberNode()
        rclpy.spin(blink_led_subscriber_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if blink_led_subscriber_node is not None:
            blink_led_subscriber_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
