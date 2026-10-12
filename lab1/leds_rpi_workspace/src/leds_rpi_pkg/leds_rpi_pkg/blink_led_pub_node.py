import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from leds_rpi_pkg_interfaces.msg import LedValue
from rcl_interfaces.msg import SetParametersResult
from typing import List


class BlinkLedPublisherNode(Node):
    def __init__(self):
        super().__init__("blink_led_publisher")
        # Declare parameters
        ### ENTER CODE #########


        ########################

        # Current state of the LED
        self.current_led_value = 0

        # Create the publisher
        ### ENTER CODE #########


        ########################

        # Create timer
        ### ENTER CODE #########


        ########################

        self.add_on_set_parameters_callback(self.parameters_callback)
        self.get_logger().info("Blink LED publisher node has been started!")

    def blink_led_periodically(self):
        '''
        This method is periodically called by the timer to change the LED state and
        then publishes the new state of the LED in the relevant topic.
        '''
        # Change the value
        ### ENTER CODE #########


        ########################

        # Create the message
        ### ENTER CODE #########


        ########################

        # Publish the message
        ### ENTER CODE #########


        ########################

    def parameters_callback(self, params: List[Parameter]):
        '''
        This method is called whenever the parameters value change.
        It creates a new timer with a period equal to the new value of "blink_led_period"
        '''
        for param in params:
            if param.name == "blink_led_period":
                if param.type_ == Parameter.Type.DOUBLE:
                    new_period = param.value
                    if new_period > 0.:
                        self.timer.cancel()
                        # Create new timer and print a success message
                        ### ENTER CODE #########
                
                
                        ########################
                        self.blink_led_period = new_period
                    else:
                        self.get_logger().warn("Blink LED period must be > 0. Ignoring update.")
                        return SetParametersResult(successful = False, reason = "Blink LED period must be > 0.")
                else:
                    return SetParametersResult(successful = False, reason = "Blink LED period must be a DOUBLE.")
        return SetParametersResult(successful = True)

def main(args = None):
    try:
        rclpy.init(args = args)
        led_node = BlinkLedPublisherNode()
        rclpy.spin(led_node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        if led_node is not None:
            led_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
