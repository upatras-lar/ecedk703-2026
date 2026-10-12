from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    blink_led_period = LaunchConfiguration('blink_led_period')

    return LaunchDescription([
        DeclareLaunchArgument('blink_led_period', default_value = '1.0', description = "Blink LED timer period (in sec)."),
        
        Node(
            package = 'leds_rpi_pkg',
            executable = 'pub_blink_node',
            name = 'pub_blink_node',
            output = 'screen',
            emulate_tty = True,
            parameters = [{
                'blink_led_period': blink_led_period,
            }],
        ),
        
        ### ENTER CODE #########


        ########################
    ])
