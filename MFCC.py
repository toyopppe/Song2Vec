#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import os
import sys

mp3Dir = u"./music_mp3"
mfccDir = u"./mfcc"
rawDir = u"./raw"

def mp3_to_raw(mp3file, rawfile):
	os.system("lame --resample 16 -b 32 -a '%s' temp.mp3" % mp3file)
	os.system("lame --decode temp.mp3 temp.wav")
	os.system("sox temp.wav %s" % rawfile)
	os.remove("temp.mp3")
	os.remove("temp.wav")

def calcNumS(rawfile):
	filesize = os.path.getsize("temp.raw")
	numsample = filesize/2
	return numsample

def musicCenter(infile, outfile, period):
	numsample = calcNumS(infile)
	fs = 16000
	center = numsample/2
	start = center - fs * period
	end = center + fs * period
	if start < 0: start = 0
	if end > numsample -1: end = numsample -1
	os.system("bcut +s -s %d -e %d < '%s' > '%s'" % (start, end, "temp.raw", rawfile))

def calculate_mfcc(rawfile, mfccfile):
	os.system("x2x +sf < '%s' | frame -l 400 -p 160 | mfcc -l 400 -f 16 -n 40 -m 19 -E > '%s'" % (rawfile, mfccfile))

if __name__ == "__main__":
	if not os.path.exists(mfccDir): os.mkdir(mfccDir)
	if not os.path.exists(rawDir): os.mkdir(rawDir)
	print "start"

	for file in os.listdir(mp3Dir):
		if not file.endswith(".mp3"): continue
		mp3file = os.path.join(mp3Dir, file)
		mfccfile = os.path.join(mfccDir, file.replace(".mp3", ".mfc"))
		rawfile = os.path.join(rawDir, file.replace(".mp3", ".raw"))

		try:
			mp3_to_raw(mp3file, "temp.raw")
			musicCenter("temp.raw", rawfile, 15)
			calculate_mfcc(rawfile, mfccfile)
			print "%s => %s" % (mp3file, mfccfile)
			os.remove("temp.raw")
		except:
			continue
