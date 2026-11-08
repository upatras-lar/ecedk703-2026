from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

pkg_name = "camera_pkg"

def generate_launch_description():
    pkg_share = FindPackageShare(pkg_name).find(pkg_name)
    camera_config_file = PathJoinSubstitution([pkg_share, "config", "camera_info.yaml"])
    rviz_config_file = PathJoinSubstitution([pkg_share, "config", "rviz", "config.rviz"])

    return LaunchDescription([
        Node(
            package = "v4l2_camera",
            executable = "v4l2_camera_node",
            name = "camera",
            output = "screen",
            parameters = [camera_config_file],
        ),

        Node(
            package = "camera_pkg",
            executable = "aruco_detection",
            name = "aruco_detection",
            output = "screen",
            parameters=[{
                "smoothing": True,
                "alpha": 0.1,
                "marker_length": 0.10,
            }]
        ),

        Node(
            package = "rviz2",
            executable = "rviz2",
            name = "rviz2",
            arguments = ["-d", rviz_config_file],
            output = "screen",
        ),
    ])