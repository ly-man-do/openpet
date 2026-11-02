<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Third-Party Licences

OpenPet uses the components below. Each keeps its own licence. Only permissive or weak-copyleft dependencies (MIT, BSD, Apache, LGPL used as a library) are accepted (plan Section 8.1). Add a row whenever a dependency, vendored file or model is added.

| Component | Used for | Licence | Where |
|---|---|---|---|
| build123d | Code-CAD | Apache-2.0 | `requirements-dev.txt` |
| OpenCascade (via cadquery-ocp) | CAD kernel used by build123d | LGPL-2.1 with exception (library use) | `requirements-dev.txt` |
| pytest | Tests | MIT | `requirements-dev.txt` |
| ROS 2 Lyrical (rclpy, std_msgs, launch) | Robot middleware | Apache-2.0 | `ros2_ws/` |
| ESP-IDF | Firmware framework | Apache-2.0 | `firmware/` |
| MuJoCo, MJX | Simulation | Apache-2.0 | `cloud/` |
| MuJoCo Playground | RL training | Apache-2.0 | `cloud/` |
| JAX | Training | Apache-2.0 | `cloud/` |
| NVIDIA CUDA base image | Training container runtime (not redistributed in releases) | NVIDIA Deep Learning Container licence | `cloud/Dockerfile` |

Not part of OpenPet and never distributed with it: the cat voice model (owner-supplied).
