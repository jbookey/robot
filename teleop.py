from lerobot.teleoperators.so101_leader import SO101LeaderConfig, SO101Leader
from lerobot.robots.so101_follower import SO101FollowerConfig, SO101Follower

robot_config = SO101FollowerConfig(
    port="/dev/tty.usbmodem5A680133411",
    id="clawbert",
)

teleop_config = SO101LeaderConfig(
    port="/dev/tty.usbmodem5A680104371",
    id="ahab",
)

robot = SO101Follower(robot_config)
teleop_device = SO101Leader(teleop_config)
robot.connect()
teleop_device.connect()

try:
    while True:
        action = teleop_device.get_action()
        robot.send_action(action)
except KeyboardInterrupt:
    print("\nStopping teleoperation...")
finally:
    try:
        teleop_device.disconnect()
    except Exception:
        pass
    try:
        robot.disconnect()
    except Exception:
        pass
