from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package = 'leds_rpi_pkg',
            executable = 'pub_button_node',
            name = 'pub_button_node',
            output = 'screen',
            emulate_tty = True,
        ),
        
        ### ENTER CODE #########


        ########################
    ])
