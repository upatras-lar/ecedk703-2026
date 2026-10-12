from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    period = LaunchConfiguration('period')
    lin = LaunchConfiguration('linear_speed')
    ang = LaunchConfiguration('angular_speed')

    return LaunchDescription([
        DeclareLaunchArgument('period', default_value='0.5', description='Commander timer period (s)'),
        DeclareLaunchArgument('linear_speed', default_value='0.2', description='Linear speed (m/s)'),
        DeclareLaunchArgument('angular_speed', default_value='0.5', description='Angular speed (rad/s)'),

        Node(
            package='luna_package',
            executable='luna_driver',
            name='luna_driver',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'cmd_topic': 'cmd_vel',
                'pose_topic': 'pose',
                'publish_period': 0.2,
            }],
        ),

        ### ENTER CODE #########


        ########################
    ])
