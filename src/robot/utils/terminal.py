from enum import Enum


class Confirmation(Enum):
	GRANTED = 1
	DENIED = 2
	
	@staticmethod
	def from_string(string):
		if string.lower() in ["y", "yes"]:
			return Confirmation.GRANTED
		else:
			return Confirmation.DENIED


def request_confirmation(message="Confirm this action (y/n)"):
	answer = input(message)
	
	return Confirmation.from_string(answer)
