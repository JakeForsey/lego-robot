import logging

import evdev

from robot.devices.input.base import BaseInput

LOGGER = logging.getLogger(__name__)


class GamepadAxisInput(BaseInput):
   def __init__(self, device_name, event_code, event_type):
      devices = [evdev.InputDevice(d) for d in evdev.list_devices()]
      self._device = next(d for d in devices if d.name == device_name)
      self._event_code = event_code  # "EV_ABS"
      self._event_type = event_type  # 1

   def __enter__(self):
      return self
		
   def __exit__(self, type, value, traceback):
      pass
	
   async def connect_to(self, output):
      async for event in self._device.async_read_loop():
         print(event)
         if event.type == evdev.ecodes.ecodes[self._event_type] \
            and event.code == self._event_code:
            print(event)
            # Axis is kind of reversed (forwards is negative)
            power = (-1 * event.value) / 35000
				
            assert power <= 1.0
            assert power >= -1.0
            output.set_power(power)
