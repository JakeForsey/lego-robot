from abc import ABC
from abc import abstractmethod
import logging
import os
from time import sleep

import pigpio

LOGGER = logging.getLogger(__name__)

MAX_PW = 2500
MIN_PW = 500


class BaseOutput(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, type, value, traceback):
        pass

    @abstractmethod
    def set_power(self, power):
        pass


class PigpioServoOutput(BaseOutput):
	
    def __init__(
        self,
        gpio_pin,
        pi=None,
        # Proportion of motors power to use
        max_power=0.3,
        max_pw=MAX_PW,
        min_pw=MIN_PW,
        *args, **kwargs
    ):
      super().__init__(*args, **kwargs)

      if pi is None:
         LOGGER.debug("Initialising pigpiod")
         os.system("sudo pigpiod")
         sleep(2)
            
         local_pi = True
         pi = pigpio.pi()
      else:
         local_pi = False

      self._gpio_pin = gpio_pin
        
      self._pi_initialised_locally = local_pi
      self._pi = pi
      self._max_power = max_power
      self._max_pw = max_pw
      self._min_pw = min_pw
		
    def __enter__(self):
      return self
    
    def __exit__(self, type, value, traceback):
      LOGGER.debug("Shutting down gpio pin...")
      self._pi.set_servo_pulsewidth(self._gpio_pin, 0)
      LOGGER.debug("Shutting down gpio pin COMPLETE")
      
      # Only shut down the pi connection if this instance
      # initialised it
      if self._pi_initialised_locally:
         LOGGER.debug("Shutting down pigpio pi connection...")
         self._pi.stop()
         LOGGER.debug("Shutting down pigpio pi connection COMPLETE")

    def _power_to_pulse_width(self, power):
      # scale power (-1 to 1) to self._max_pw to self._min_pw
      min_power = -1
      max_power = 1
		    	
      return (self._max_pw - self._min_pw) * ((power - min_power) / (max_power - min_power)) + self._min_pw

    def set_power(self, power):
        self._pi.set_servo_pulsewidth(
            self._gpio_pin,
            self._power_to_pulse_width(power)
        )