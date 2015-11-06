#!/tool/pandora64/bin/python2.7
import re
import os
import sys
import gzip

#example excution:
#python /home/jlawrenc/bin/python/systemic_timing_issues.py -rpt <path_to_timing_report> -thresh <timing_failure_to_stop_looking_past ex:-0.150>

usageFlag = 0

sysArgv = " ".join(sys.argv)
splitSysArgv = sysArgv.split()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if re.search("-rpt", sysArgv) and not re.search("-rpt", splitSysArgv[-1]):
	rpt = sysArgv.split("-rpt")
	rpt = rpt[1].split()
	rpt = rpt[0]
else:
	usageFlag = 1

if re.search("-thresh", sysArgv) and not re.search("-thresh", splitSysArgv[-1]):
	thresh = sysArgv.split("-thresh")
	thresh = thresh[1].split()
	thresh = thresh[0]
	if not is_number(thresh):
		print "Value for timing threshold is not number\n"
		usageFlag = 1
else: 
	usageFlag = 1

if usageFlag:
	print "ERROR:\n\t USAGE: python /home/jlawrenc/bin/python/systemic_timing_issues.py -rpt <path_to_timing_report> -thresh <timing_failure_to_stop_looking_past ex:-0.150>"
	sys.exit()


input = gzip.open(rpt, 'rb')
splitrpt = rpt.split("/")
output = open("timing_issues_" + splitrpt[-1].replace(".rpt.gz",""), 'w')
 = 
for line in input.readlines():
	if findpoints:
		if re.search("Startpoint", line):
			start = line
		elif re.search("Endpoint", line):
			end = line
			findpoints = 0
	if not findpoints: #look for slack value
		if re.search("slack", line):
			splitline = line.split()
			if re.search("VIOLATED", splitline[1]) and (float(splitline[2]) <= float(thresh)):
				output.write("%s%s\n" % (start, end))
				findpoints = 1
			else:
				sys.exit()
	
	
