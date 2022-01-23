import sys
import os

def startCollection(argv):
	print('Running data collection script...')
	os.system('/usr/lib/piaware/helpers/faup1090 --stdout > ~/{0}.txt'.format(str(argv)))
	print('Terminating data collection script...')

if __name__ == '__main__':
	startCollection(sys.argv[1])
