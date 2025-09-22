#!/usr/bin/env python3
"""Print the raw Present_Position values for the SO101 leader arm."""

from __future__ import annotations

import argparse
import sys

from lerobot.teleoperators.utils import make_teleoperator_from_config
from lerobot.teleoperators.so101_leader.config_so101_leader import SO101LeaderConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Display the current encoder readings for the SO101 leader teleoperator"
    )
    parser.add_argument(
        "--port",
        default="/dev/tty.usbmodem5A680104371",
        help="Serial port the teleoperator is connected to (default: %(default)s)",
    )
    parser.add_argument(
        "--id",
        default="ahab",
        help="Teleoperator ID to use when constructing the config (default: %(default)s)",
    )
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Skip clearing the homing offsets before reading (defaults to same behaviour as calibration)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = SO101LeaderConfig(port=args.port, id=args.id)
    teleop = make_teleoperator_from_config(config)

    positions = {}
    try:
        teleop.connect(calibrate=False)

        if not args.no_reset:
            # Match calibration behaviour: clear homing offsets so we see the raw multi-turn counts.
            teleop.bus.reset_calibration()

        positions = teleop.bus.sync_read("Present_Position", normalize=False)
    except Exception as exc:  # pragma: no cover - diagnostic utility
        print(f"Error while reading positions: {exc}", file=sys.stderr)
        return 1
    finally:
        if getattr(teleop, "is_connected", False):
            try:
                teleop.disconnect()
            except Exception:
                pass

    print("Raw encoder counts (Present_Position):")
    for motor, value in positions.items():
        print(f"  {motor:>12}: {value:5d}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
