"""Small Polymetis example: move between two frames and use the gripper.

Start the Polymetis robot and gripper servers first, then run:

    pixi run python scripts/polymetis_quickstart.py

Frame A is the end-effector pose when this script starts. Frame B has the
same orientation and is 5 cm above frame A in the robot base frame.
"""

import argparse
import time

import torch
from polymetis import GripperInterface, RobotInterface


MOVE_DISTANCE = 0.15  # metres
MOVE_TIME = 1.0  # seconds for each slow arm movement
GRIPPER_OPEN_WIDTH = 0.08  # metres
GRIPPER_CLOSED_WIDTH = 0.0  # metres
GRIPPER_SPEED = 0.085  # metres per second
GRIPPER_FORCE = 10.0  # newtons


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--robot-ip",
        default="localhost",
        help="IP address running the Polymetis servers (default: localhost)",
    )
    args = parser.parse_args()

    print(f"Connecting to Polymetis at {args.robot_ip} ...")
    robot = RobotInterface(ip_address=args.robot_ip, enforce_version=False)
    gripper = GripperInterface(ip_address=args.robot_ip)

    # Use the current pose so the example does not depend on a hard-coded pose.
    frame_a_position, frame_a_orientation = robot.get_ee_pose()
    frame_b_position = frame_a_position + torch.tensor([0.0, 0.0, MOVE_DISTANCE])

    print(f"Frame A position: {frame_a_position.tolist()}")
    print(f"Frame B position: {frame_b_position.tolist()}")
    input(
        "Clear the workspace and keep a hand near the emergency stop. "
        "Press Enter to move, or Ctrl-C to cancel..."
    )

    print("Moving slowly from frame A to frame B...")
    robot.move_to_ee_pose(
        frame_b_position,
        frame_a_orientation,
        time_to_go=MOVE_TIME,
    )

    print("Moving slowly from frame B back to frame A...")
    robot.move_to_ee_pose(
        frame_a_position,
        frame_a_orientation,
        time_to_go=MOVE_TIME,
    )

    print("Closing the gripper...")
    gripper.goto(
        width=GRIPPER_CLOSED_WIDTH,
        speed=GRIPPER_SPEED,
        force=GRIPPER_FORCE,
    )

    time.sleep(1.0)  # wait for the gripper to close

    print("Opening the gripper...")
    gripper.goto(
        width=GRIPPER_OPEN_WIDTH,
        speed=GRIPPER_SPEED,
        force=GRIPPER_FORCE,
    )

    print("Done.")


if __name__ == "__main__":
    main()
