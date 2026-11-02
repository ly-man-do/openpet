<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# Development Hosts

Phases 0 and 1 need no robot hardware. All of their work (code-CAD, simulation, ROS 2 software, CI) runs on an ordinary computer. The Raspberry Pi 5 is first needed for the Phase 2 bench build.

| Host | Good for |
|---|---|
| **Apple-silicon Mac** (reference: MacBook Pro M1 Pro, 16 GB) | Code-CAD, MuJoCo simulation, ROS 2 in an **arm64** Linux container (same CPU architecture as the Pi 5), ESP-IDF firmware builds |
| **Linux PC** (x86-64) | Native Ubuntu 26.04 + ROS 2 Lyrical, RViz/Gazebo with a real display, USB access to an ESP32-S3 dev board, optional local NVIDIA GPU for small MJX runs |
| **Cloud GPU** | RL training (Phase 6 onward), see `cloud/` |

## Python: code-CAD and simulation (Mac or Linux)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest
```

`requirements-dev.txt` includes build123d and MuJoCo. MuJoCo runs natively on Apple silicon. For an interactive viewer on macOS, use `.venv/bin/mjpython -m mujoco.viewer --mjcf=<file.xml>`; on Linux, `python -m mujoco.viewer`.

To review CAD visually, install the **OCP CAD Viewer** extension in VS Code, or open the STEP files from `build/stl/` in FreeCAD.

## ROS 2 Lyrical

### On a Mac: container

Install [OrbStack](https://orbstack.dev) or Docker Desktop and start it. Then:

```bash
tools/dev/ros2.sh                                          # shell with the workspace built
tools/dev/ros2.sh ros2 launch openpet_bringup hello.launch.py
```

The script runs `ros:lyrical-ros-base` (Ubuntu 26.04, arm64 on Apple silicon), mounts `ros2_ws/src` read-only, keeps build output in Docker volumes, and builds the workspace before running your command. GUI tools such as RViz are easier on a Linux PC; on the Mac, use Foxglove Studio over `--network host`.

### On a Linux PC: native

Install Ubuntu 26.04 LTS, then ROS 2 Lyrical from the official apt repository (follow the ROS 2 Lyrical "Ubuntu (deb packages)" install page), then:

```bash
source /opt/ros/lyrical/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install
source install/setup.bash
ros2 launch openpet_bringup hello.launch.py
```

`tools/dev/ros2.sh` also works on Linux if you'd rather not install ROS natively.

### Talking between hosts

Nodes on the Mac container (`--network host`) and a Linux PC on the same LAN discover each other automatically with the default DDS settings, as long as both use the same `ROS_DOMAIN_ID`. The Pi will join the same way from Phase 2.

## Firmware (ESP32-S3)

CI builds the firmware with ESP-IDF v5.5. To build locally, install ESP-IDF (macOS and Linux are both supported; follow Espressif's ESP-IDF v5.5 "Get Started" guide), then:

```bash
cd firmware
idf.py set-target esp32s3
idf.py build
```

An ESP32-S3 dev board (for example an ESP32-S3-DevKitC-1) is enough to start firmware work before the Pi arrives: flash it from the Mac or a Linux PC over USB and talk to it from ROS 2 on that same machine through the micro-ROS agent.
