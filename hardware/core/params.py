# SPDX-License-Identifier: CERN-OHL-P-2.0
"""Shared parameters for all OpenPet code-CAD.

Every part imports its printer limits and servo dimensions from here so that
a change (a different printer, a different servo) is made in one place.
All lengths are in millimetres.

Servo dimensions are taken from Feetech datasheets and must be checked
against a physical sample with calipers before any part that mates with a
servo is frozen (tracked in Beads).
"""

from dataclasses import dataclass

# --- Printer: Bambu Lab P1S (plan Section 6.5) -------------------------------

BUILD_VOLUME = (256.0, 256.0, 256.0)  # X, Y, Z
MAX_PART_SIZE = 256.0  # every printed part, any axis, in its print orientation
NEAR_LIMIT = 240.0  # parts above this in X or Y need full-plate, no-brim settings

NOZZLE = 0.4
LAYER_HEIGHT = 0.2
WALLS_LOAD_BEARING = 3

# Clearances for FDM fits on the P1S (to be tuned with the test coupon)
CLEARANCE_SLIDING = 0.3
CLEARANCE_PRESS = 0.1


# --- Heat-set inserts ---------------------------------------------------------

@dataclass(frozen=True)
class HeatSetInsert:
    thread: str
    hole_diameter: float
    depth: float


INSERT_M2 = HeatSetInsert("M2", 3.2, 4.0)
INSERT_M2_5 = HeatSetInsert("M2.5", 3.6, 5.0)
INSERT_M3 = HeatSetInsert("M3", 4.0, 5.7)


# --- Servos (plan Section 6.1) ------------------------------------------------

@dataclass(frozen=True)
class Servo:
    name: str
    body: tuple[float, float, float]  # length, width, height of the case
    horn_offset: float  # output-shaft centre from the short end of the case
    stall_torque_kgcm: float
    voltage: float


STS3215 = Servo(
    name="Feetech STS3215",
    body=(45.2, 24.7, 35.0),
    horn_offset=11.0,
    stall_torque_kgcm=30.0,
    voltage=12.0,
)

SCS0009 = Servo(
    name="Feetech SCS0009",
    body=(23.2, 12.1, 25.25),
    horn_offset=6.0,
    stall_torque_kgcm=2.3,
    voltage=6.0,
)
