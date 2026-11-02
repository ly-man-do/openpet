# SPDX-License-Identifier: Apache-2.0
"""Phase 0 smoke test: publishes a heartbeat so we know ROS 2 runs on the Pi."""

import platform

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class Hello(Node):
    def __init__(self):
        super().__init__("openpet_hello")
        self.publisher = self.create_publisher(String, "openpet/hello", 10)
        self.count = 0
        self.create_timer(1.0, self.tick)

    def tick(self):
        msg = String()
        msg.data = f"OpenPet hello #{self.count} from {platform.node()} ({platform.machine()})"
        self.publisher.publish(msg)
        self.get_logger().info(msg.data)
        self.count += 1


def main():
    rclpy.init()
    node = Hello()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
