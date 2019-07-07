import logging
from time import sleep

from robot.devices.output.base import PigpioServoOutput
from robot.utils import terminal

LOGGER = logging.getLogger(__name__)


class BrushlessMotor(PigpioServoOutput):
    def __init__(
        self,
        *args, **kwargs
    ):
      super().__init__(*args, **kwargs)
      
      if terminal.request_confirmation("Arm brushless motor? (y/n)") == terminal.Confirmation.GRANTED:
         LOGGER.debug("Arming brushless motor...")
         self._pi.set_servo_pulsewidth(self._gpio_pin, self._max_pw)
         sleep(3)
         self._pi.set_servo_pulsewidth(self._gpio_pin, self._min_pw)
         sleep(3)
         LOGGER.debug("Arming brushless motor COMPLETE")

    def _power_to_pulse_width(self, power):
      if power < 0:
         return self._min_pw
    		
      # scale power (-1 to 1) to self._max_pw to self._min_pw
      min_power = 0
      max_power = 1
		    	
      return (self._max_pw - self._min_pw) * ((power - min_power) / (max_power - min_power)) + self._min_pw