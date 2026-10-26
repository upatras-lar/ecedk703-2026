from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = FindPackageShare("pendu_control_pkg").find("pendu_control_pkg")

    urdf_file = PathJoinSubstitution([pkg_share, "urdf", "double_pendulum.urdf"])
    rviz_config_file = PathJoinSubstitution([pkg_share, "config", "display_double_pendulum.rviz"])

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": ParameterValue(Command(["cat ", urdf_file]), value_type=str)
            }],
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz_config_file],
            output="screen",
        ),
        ############ ENTER CODE HERE ###############


        ############################################
    ])