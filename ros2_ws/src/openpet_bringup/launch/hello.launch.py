# SPDX-License-Identifier: Apache-2.0
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package="openpet_bringup", executable="hello", output="screen"),
    ])
