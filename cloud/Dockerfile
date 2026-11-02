# SPDX-License-Identifier: Apache-2.0
# OpenPet training image: MuJoCo + MJX + MuJoCo Playground on JAX/CUDA (NVIDIA GPUs only).
# Build: docker build -t openpet-train -f cloud/Dockerfile .
FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    MUJOCO_GL=egl

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-pip git libegl1 libgl1 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY cloud/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /workspace
COPY cloud/ /workspace/cloud/
ENTRYPOINT ["python", "/workspace/cloud/smoke_test.py"]
