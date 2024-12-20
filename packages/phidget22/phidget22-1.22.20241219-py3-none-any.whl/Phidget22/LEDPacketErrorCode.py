import sys
import ctypes
class LEDPacketErrorCode:
	# No error
	LED_PACKET_ERROR_OK = 0
	# Unknown Error
	LED_PACKET_ERROR_UNKNOWN = 1
	# The response packet timed out
	LED_PACKET_ERROR_TIMEOUT = 2
	# Something about the sent or received data didn't match the expected format.
	LED_PACKET_ERROR_FORMAT = 3
	# The input lines are invalid. This likely means a cable has been unplugged.
	LED_PACKET_ERROR_INVALID = 4
	# Data is being received faster than it can be processed. Some has been lost.
	LED_PACKET_ERROR_OVERRUN = 5
	# Something behind the scenes got out of sequence.
	LED_PACKET_ERROR_CORRUPT = 6
	# One or more packets have received a NACK response
	LED_PACKET_ERROR_NACK = 7

	@classmethod
	def getName(self, val):
		if val == self.LED_PACKET_ERROR_OK:
			return "LED_PACKET_ERROR_OK"
		if val == self.LED_PACKET_ERROR_UNKNOWN:
			return "LED_PACKET_ERROR_UNKNOWN"
		if val == self.LED_PACKET_ERROR_TIMEOUT:
			return "LED_PACKET_ERROR_TIMEOUT"
		if val == self.LED_PACKET_ERROR_FORMAT:
			return "LED_PACKET_ERROR_FORMAT"
		if val == self.LED_PACKET_ERROR_INVALID:
			return "LED_PACKET_ERROR_INVALID"
		if val == self.LED_PACKET_ERROR_OVERRUN:
			return "LED_PACKET_ERROR_OVERRUN"
		if val == self.LED_PACKET_ERROR_CORRUPT:
			return "LED_PACKET_ERROR_CORRUPT"
		if val == self.LED_PACKET_ERROR_NACK:
			return "LED_PACKET_ERROR_NACK"
		return "<invalid enumeration value>"
