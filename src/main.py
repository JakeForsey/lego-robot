import asyncio
import logging

from common import arguments
from robot.devices.output.motor import BrushlessMotor
from robot.devices.output.servo import Servo
from robot.devices.input.gamepad import GamepadAxisInput
from robot.streaming.camera import ImageStream
from hivemind import server


def run_robot(args: dict):

	with BrushlessMotor(13, max_power=0.4, min_pw=1000, max_pw=2000) as motor, \
			Servo(5, min_pw=1250, max_pw=2500) as servo, \
			GamepadAxisInput("Microsoft X-Box 360 pad", 1, "EV_ABS") as forward_axis, \
			GamepadAxisInput("Microsoft X-Box 360 pad", 0, "EV_ABS") as steering_axis, \
			ImageStream(port=8000, hivemind_ip=args.hivemind_ip) as image_stream:

		loop = asyncio.get_event_loop()
		connections = asyncio.gather(
			# asyncio.async(forward_axis.connect_to(motor)),
			# asyncio.async(steering_axis.connect_to(servo)),
			asyncio.async(image_stream.stream())
		)
		loop.run_until_complete(connections)


def run_hivemind(args: dict):
	server.run()


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)

	args = arguments.main_args()

	if args.mode == "hivemind":
		run_hivemind(args)
	elif args.mode == "robot":
		run_robot(args)
