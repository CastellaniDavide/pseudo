"""Test anonymous file
"""
import pseudo

__author__ = "help@castellanidavide.it", "Bellamoli Riccardo"
__version__ = "01.01 2021-1-23"

def test():
	"""Tests the anonymous function in the anonymous class
	Write here all test you want to do.
	REMEMBER to test your programm you can't use __init__ function
	"""
	assert pseudo.__author__ == ("Bellamoli Riccardo", "Castellani Davide"), "Sanity check fail"
	assert pseudo.pseudo() != "Error", "Run check fail"
	
if __name__ == "__main__":
	test()
