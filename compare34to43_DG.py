#!/tool/pandora64/bin/python2.7
import re
import os
import sys
import gzip

#example excution:
#python /home/jlawrenc/bin/python/compareXtoY_DG.py -pathX <path_to_X> -pathY <path_to_Y>

usageFlag = 0

sysArgv = " ".join(sys.argv)
splitSysArgv = sysArgv.split()
convertXtoY = 0.001

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def processFINAL_qor(file_name):
	fileX = gzip.open(pathX + file_name, 'rb')
	fileY = gzip.open(pathY + file_name, 'rb')
	filecompare = open("compareFINAL_qor.rpt", 'w')
	for lineY in fileY.readlines():
		lineX = fileX.readline()
		splitlineY = lineY.split()
		try:
			#isinstance(splitlineY[1], (int,float))
			if is_number(splitlineY[-1]) and re.search(':$', splitlineY[-2]):
				splitlineX = lineX.split()
				print splitlineX
				dataX = float(splitlineX[-1])
				dataY = float(splitlineY[-1])
				diff = float(splitlineX[-1]) - float(splitlineY[-1])
				if dataY == 0 :
					linemod = lineY.rstrip() + "%15.4f%15.4f%15s\n" % (dataX, diff, "")
				else: 
					percent = (dataX - dataY)*100.0/dataY
					linemod = lineY.rstrip() + "%15.4f%15.4f%15.2f%s\n" % (dataX, diff, percent, "%")
				filecompare.write(linemod)
			else:
				filecompare.write(lineY)
		except IndexError:
			filecompare.write(lineY)	

if re.search("-pathX", sysArgv) and not re.search("-pathX",splitSysArgv[-1]):
	pathX = sysArgv.split("-pathX")
	pathX = pathX[1].split()
	pathX = pathX[0].rstrip("/")+"/"
else:
	usageFlag = 1

if re.search("-pathY", sysArgv) and not re.search("-pathY", splitSysArgv[-1]):
	pathY = sysArgv.split("-pathY")
	pathY = pathY[1].split()
	pathY = pathY[0].rstrip("/")+"/"
else:
	usageFlag = 1

if usageFlag:
	print "ERROR:\n\t USAGE: python /home/jlawrenc/bin/python/compareXtoY_DG.py -pathX <path_to_Xnm> -pathY <path_to_Ynm>"
	sys.exit()

fileset = ["FINAL_qor.rpt.gz"]

for file in fileset:
	if re.search("FINAL_qor.rpt.gz", file):
		processFINAL_qor(file)
	else:
		print "I don't know how to compare the file:" + file + " yet"
