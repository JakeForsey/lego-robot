from robot.devices.output.base import PigpioServoOutput


class Servo(PigpioServoOutput):
	
    def __init__(
        self,
        *args, **kwargs
    ):
      super().__init__(*args, **kwargs)
