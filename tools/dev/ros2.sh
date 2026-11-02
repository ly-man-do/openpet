#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Run ROS 2 Lyrical (Ubuntu 26.04) in a container on a development host.
# On an Apple-silicon Mac this is an arm64 container, the same architecture as the Pi 5.
#
#   tools/dev/ros2.sh                       # interactive shell, workspace built
#   tools/dev/ros2.sh ros2 launch openpet_bringup hello.launch.py
#
# Sources are mounted read-only; build/install/log live in a named volume so the
# repo stays clean and rebuilds are incremental.
set -euo pipefail

IMAGE="${OPENPET_ROS_IMAGE:-ros:lyrical-ros-base}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [ $# -eq 0 ]; then
  set -- bash
  TTY=(-it)
else
  TTY=()
  [ -t 0 ] && TTY=(-it)
fi

exec docker run --rm ${TTY[@]+"${TTY[@]}"} \
  --name "openpet-ros-$$" \
  --network host \
  -v "$ROOT/ros2_ws/src:/ws/src:ro" \
  -v openpet-ros-build:/ws/build \
  -v openpet-ros-install:/ws/install \
  -v openpet-ros-log:/ws/log \
  -w /ws \
  "$IMAGE" \
  bash -c 'source /opt/ros/lyrical/setup.bash \
    && colcon build --symlink-install >/tmp/colcon.log 2>&1 || { cat /tmp/colcon.log; exit 1; }; \
    source install/setup.bash && exec "$@"' openpet "$@"
