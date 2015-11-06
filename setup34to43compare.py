#!/tool/pandora64/bin/python2.7
import re
import os
import sys
import gzip
import time

#example execution:
#python /home/jlawrenc/bin/python/setupxtoycompare_asdf.py -tile asdf -parent_tile asdf -additional_params /home/jlawrenc/asdf/asdf.params -additional_controls /home/jlawrenc/asdf/asdf.controls -asdf_asdf __asdf__ -pubdir /proj/asdf_publish1/asdf/publish/base_asdf/asdf/cell/

usageFlag = 0

start=os.getcwd()

sysArgv = " ".join(sys.argv)
splitSysArgv = sysArgv.split()
#splitSysArgv == sys.argv

if re.search("-pubdir", sysArgv) and not re.search("-pubdir", splitSysArgv[-1]):
	pdName = sysArgv.split("-pubdir")
	pdName = pdName[1].split()
	pdName = pdName[0].rstrip("/")+"/"
else:
	usageFlag = 1

if re.search("-tile", sysArgv) and not re.search("-tile", splitSysArgv[-1]):
	tileName = sysArgv.split("-tile")
	tileName = tileName[1].split()
	tileName = tileName[0]
	if re.search("asdf", tileName):
		asdfflag = 1
else:
	usageFlag = 1

if re.search("-parent_tile", sysArgv) and not re.search("-parent_tile", splitSysArgv[-1]):
	ptileName = sysArgv.split("-parent_tile")
	ptileName = ptileName[1].split()
	ptileName = ptileName[0]
else:
	usageFlag = 1

if re.search("-asdf_d2c", sysArgv) and not re.search("-asdf_d2c", splitSysArgv[-1]):
	asdfd2cName = sysArgv.split("-asdf_d2c")
	asdfd2cName = asdfd2cName[1].split()
	asdfd2cName = asdfd2cName[0]
else:
	usageFlag = 1

if re.search("-additional_params", sysArgv) and not re.search("-additional_params", splitSysArgv[-1]):
	addl_params = sysArgv.split("-additional_params")
	addl_params = addl_params[1].split()
	addl_params = addl_params[0]
	addl_params_flag = 1
else: 
	addl_params_flag = 0

if re.search("-additional_controls", sysArgv) and not re.search("-additional_controls", splitSysArgv[-1]):
	addl_controls = sysArgv.split("-additional_controls")
	addl_controls = addl_controls[1].split()
	addl_controls = addl_controls[0]
	addl_controls_flag = 1
else:
	addl_controls_flag = 0


if usageFlag:
	print "ERROR:\n\t USAGE: python /home/jlawrenc/bin/python/setupxtoycompare.py -pubdir <publish_directory> -tile <tile_name> -parent_tile <parent_tile> -asdf <asdf>"
	sys.exit()

timestamp = time.strftime('%X_%x')

for unit in ['h','m']:
	timestamp = timestamp.replace(":",unit,1)

timestamp = timestamp.replace("_","s")
timestamp = timestamp.replace("/","-")

dirx = "x_collateral" + timestamp
diry = "y_collateral" + timestamp
os.system("mkdir " + dirx + " " + dirx)


if asdfflag:
	tileName_base = "asdf*"
	tileName_root = "asdf"
	tileName_orig = tileName	
	tileName0 = "asdf"
	tileName1 = "asdf"
	tileName2 = "asdf"
	tileName3 = "asdf"
	alltiles = [tileName0, tileName1, tileName2, tileName3]

fileset = [tileName_base+'.asdf.sdc.gz', tileName_base+'.asdf.sdc.gz', 'PrepForRelease.def.gz', 'PrepForRelease.modswp.v.gz', 'PrepForRelease.v.gz', tileName_base+'.def.gz', tileName_base+'.modswp.v.gz', tileName_base+'.v.gz']
sdcfiles = fileset[0:2]

os.chdir(dirx)
os.system("mkdir " + tileName0 + " " + tileName1 + " " + tileName2 + " " + tileName3)
for file in fileset:
	os.system("cp " + pdName + tileName0 + "/" + file + " " + tileName0)
	os.system("cp " + pdName + tileName1 + "/" + file + " " + tileName1)
	os.system("cp " + pdName + tileName2 + "/" + file + " " + tileName2)
	os.system("cp " + pdName + tileName3 + "/" + file + " " + tileName3)


#remove lines with set_.*put_delay in x_collateral/*.scd.gz files
for tile in alltiles:
	os.chdir(start + "/" + dirx + "/" + tile)
	for sdcfile in sdcfiles:
		sdcfile = sdcfile.replace(tileName_base, tile)
		sdc = gzip.open(sdcfile, 'rb')
	        sdcfile_mod = sdcfile.replace("gz", "mod")
	        sdc_mod = gzip.open(sdcfile_mod + ".gz", 'wb')
		#comment-out lines that have set_input_delay or set_output_delay
		for line in sdc.readlines():
			if re.search('set_.*put_delay', line):
				sdc_mod.write("#" + line)
			else:
				sdc_mod.write(line)
		sdc.close()
		sdc_mod.close()	
		os.system("cp " + sdcfile_mod + ".gz " + sdcfile)

os.chdir(start)
os.system("cp -rf " + dirx + "/* " + diry)

#hack files in diry
#need to cd to diry
for tile in alltiles:
	os.chdir(start + "/" + diry + "/" + tile)
	os.system('mv PrepForRelease.def.gz PrepForRelease.def_raw.gz')
	os.system('gzip -d -c PrepForRelease.def_raw.gz | /home/johndoe/bin/ppgrep -v "^(TRACKS|VIA|ROW|GCELLGRID)" > PrepForRelease_clean.def')
	os.system('/home/johndoe/bin/def_scale.pl -projrev asdf -Def PrepForRelease_clean.def')
	os.system('gzip -c scaled_x_to_y.def > PrepForRelease.def.gz')
	
	
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 1000 -r asdf -n asdf  | gzip -c > %s.asdf.sdc.gz' % 	(tile, tile))
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 1000 -r asdf -n asdf   | gzip -c > %s.asdf.sdc.gz' % 	(tile, tile))
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 5000 -r asdf -n asdf | gzip -c > %s.asdf.sdc.gz' % (tile, tile))
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 3333 -r asdf -n asdf  | gzip -c > %s.asdf.sdc.gz' % 	(tile, tile))
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 1000 -r asdf -n asdf  | gzip -c > %s.asdf.sdc.gz' % 	(tile, tile))
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 1000 -r asdf -n asdf   | gzip -c > %s.asdf.sdc.gz' % 	(tile, tile))
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 5000 -r asdf -n asdf | gzip -c > %s.asdf.sdc.gz' % (tile, tile))
	os.system('gzip -d -c %s.asdf.sdc.gz | /home/johndoe/bin/scale_sdc.pl -s 3333 -r asdf -n asdf  | gzip -c > %s.asdf.sdc.gz' % 	(tile, tile))
	
	#Scale FE_CORE values in PrepForRelease.def.gz (from /home/johndoe/bin/def_scale.pl):
	X_Scale = 90.0/130;
	Y_Scale = 572.0/900;
	
   	xcoord2change = "582400"
	xcoord2change2 = "582480"
	pfr_def = gzip.open("PrepForRelease.def.gz", 'rb')
	pfr_def_mod = gzip.open("PrepForRelease.def.mod.gz", 'wb')
	for line in pfr_def.readlines():
		if re.search("FE_CORE", line):
			linesplit = line.split()
			if "_X" in linesplit[1]:
				linesplit[3] = str(float(linesplit[3]) * X_Scale)
			else:
				linesplit[3] = str(float(linesplit[3]) * Y_Scale)
			linemod = " ".join(linesplit)
			pfr_def_mod.write("    " + linemod + "\n")	
		elif re.search(xcoord2change, line):
			pfr_def_mod.write(line.replace(xcoord2change, xcoord2change2) + "\n")	
		else:
			pfr_def_mod.write(line)
	pfr_def.close()
	pfr_def_mod.close()
	os.system("cp " + "PrepForRelease.def.mod.gz " + "PrepForRelease.def.gz")



#Setup x base run dir
os.chdir(start)
rundirx = "%s_x_ref_%s" % (tileName_root, timestamp)
os.system("mkdir %s" % rundirx)
os.chdir(rundirx)

os.system("/proj/asdf_setup_asdf1/asdf_shared/no_tech/asdf_pd_scripts/user_shared/bin/runasdf.py -fcfp_mode -tile %s -parent_tile %s -asdf_d2c %s -fcfp_dir %s" % (tileName_orig, ptileName, asdfd2cName, start+"/"+dirx+"/"+tileName_orig))

if addl_params_flag:
	#append addtional params/controls to my.params and my.controls
	print "appending addl_params to my.params"
	os.system("cat %s >> my.params" % addl_params)
if addl_controls_flag:
	print "appending addl_controls to my.controls"
	os.system("cat %s >> my.controls" % addl_controls)

os.system("/home/jlawrenc/bin/multi_run")
#Setup x base run dir
os.chdir(start)
#CHANGE
rundiry = "%s_x_%s" % (tileName_root, timestamp)
os.system("mkdir %s" % rundiry)
os.chdir(rundiry)
asdfd2cName_x = asdfd2cName.replace("D2C","asdf_D2C")
os.system("/proj/asdf_setup_asdf1/asdf_shared/no_tech/asdf_pd_scripts/user_shared/bin/runasdf.py -fcfp_mode -tile %s -parent_tile %s -asdf_d2c %s -fcfp_dir %s" % (tileName_orig, ptileName, asdfd2cName_asdf, start+"/"+diry+"/"+tileName_orig))

os.system("cp my.params my.orig.params")
os.system("cp my.controls my.orig.controls")

#vars to hack: TAPEOUT, RTL__DEPOT_PATH
#first add in asdf params to my.mod.params
paramsf = """#POWER_MMMC_LIB_LIST     = asdf
#PTPX_MACRO_CORNERS      = asdf
TILEBUILDER_FREEZEFLOWRELEASE   = _rel_0.3_DEV
STACK = asdft

"""
params_mod = open("my.mod.params", 'w')
params_mod.write(paramsasdf)

params = open("my.params", 'r')
for line in params.readlines():
	if re.search("RTL_asdf_DEPOT_PATH", line):
		params_mod.write(line.replace("d2c", "t_d2c") + "\n")
	
	elif re.search("TAPEOUT", line):
		params_mod.write("TAPEOUT = a0\n")
	else:
		params_mod.write(line)
params.close()
params_mod.close()
os.system("mv my.mod.params my.params")

#myrun = open("my_run", 'r')
#myrun_mod = open("my_run.mod", 'w')
#for line in myrun.readlines():
#	if re.search("tcsh", line):
#		myrun_mod.write("#!/bin/tcsh\nasdf asdf asdf.er\n")
#	else:
#		myrun_mod.write(line)
#
#os.system("mv my_run.mod my_run")		

if addl_params_flag:
	#append addtional params/controls to my.params and my.controls	
	print "appending addl_params to my.params"
	os.system("cat %s >> my.params" % addl_params)
if addl_controls_flag:
	print "appending addl_controls to my.controls"
	os.system("cat %s >> my.controls" % addl_controls)
os.system("echo TILEBUILDER_DATATREE_TOSYNC = tsdf >> my.controls")
os.system("/home/jlawrenc/bin/multi_run")
#os.system("cp ../" + rundirx + "/my_run_multiple .")
#if no -additional_params 
if not addl_params_flag:
	print "ADD TILE SPECIFIC PARAMS TO %s/my.*" % rundirx
	print "ADD TILE SPECIFIC PARAMS TO %s/my.*" % rundiry

#if no -additional_controls 
if not addl_controls_flag:
	print "ADD TILE SPECIFIC CONTROLS TO %s/my.*" % rundirx
	print "ADD TILE SPECIFIC CONTROLS TO %s/my.*" % rundiry

os.chdir(start)
print "make any addtional adjustments to params/controls/revrc/my_run then execute ./my_run or ./my_run_multiple in both %s and %s to kick off the runs" % (rundirx, rundiry)
print "remove asdf* cells from %s.v.gz in %s" % (tileName_base, diry)
