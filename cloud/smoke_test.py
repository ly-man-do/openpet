# SPDX-License-Identifier: Apache-2.0
"""End-to-end cloud smoke test: confirm the GPU is visible to JAX, step an MJX
model in parallel, and write a small JSON result to the output directory
(which the launch script uploads to storage before shutting the instance down).
"""

import argparse
import json
import time
from pathlib import Path

import jax
import mujoco
from mujoco import mjx

XML = """
<mujoco>
  <worldbody>
    <geom type="plane" size="1 1 0.1"/>
    <body pos="0 0 0.5"><freejoint/><geom type="sphere" size="0.05"/></body>
  </worldbody>
</mujoco>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("/workspace/out"))
    parser.add_argument("--batch", type=int, default=4096)
    parser.add_argument("--steps", type=int, default=500)
    args = parser.parse_args()

    devices = [str(d) for d in jax.devices()]
    model = mujoco.MjModel.from_xml_string(XML)
    mx = mjx.put_model(model)
    dx = mjx.make_data(mx)
    batch = jax.vmap(lambda _: dx)(jax.numpy.arange(args.batch))
    step = jax.jit(jax.vmap(mjx.step, in_axes=(None, 0)))

    batch = step(mx, batch)  # compile
    start = time.time()
    for _ in range(args.steps):
        batch = step(mx, batch)
    jax.block_until_ready(batch)
    elapsed = time.time() - start

    result = {
        "devices": devices,
        "gpu": any("cuda" in d.lower() or "gpu" in d.lower() for d in devices),
        "batch": args.batch,
        "steps": args.steps,
        "steps_per_second": args.batch * args.steps / elapsed,
        "final_height_mean": float(batch.qpos[:, 2].mean()),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "smoke_test.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
