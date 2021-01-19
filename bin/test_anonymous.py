"""Test anonymous file
"""
from anonymous import *

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2021-1-19"

def test():
	"""Tests the anonymous function in the anonymous class
	Write here all test you want to do.
	REMEMBER to test your programm you can't use __init__ function
	"""
	assert anonymous.anonymous() == "anonymous", "test failed"
	#assert anonymous.<function>(<values>) == <the result(s) you would like to have>, "<the fail message>"
	
if __name__ == "__main__":
	test()
