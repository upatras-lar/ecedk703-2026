from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = FindPackageShare("myarm_300_pi").find("myarm_300_pi")

    urdf_file = PathJoinSubstitution([pkg_share, "urdf", "myarm_300_pi.urdf"])
    rviz_config_file = PathJoinSubstitution([pkg_share, "config", "display_myarm_300_pi.rviz"])

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": ParameterValue(Command(["cat ", urdf_file]), value_type = str)
            }],
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="joint_state_publisher_gui",
            output="screen",
            remappings=[("/joint_states", "/joint_states_targets")],
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