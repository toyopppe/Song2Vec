#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import os
import sys

mp3Dir = u"./music_mp3/RADWIMPS"
mfccDir = u"./mfcc/RADWIMPS"

def mp3_to_raw(mp3file, rawfile):
	os.system("lame --resample 16 -b 32 -a '%s' temp.mp3" % mp3file)
	os.system("lame --decode temp.mp3 temp.wav")
	os.system("sox temp.wav %s" % rawfile)
	os.remove("temp.mp3")
	os.remove("temp.wav")

def calculate_mfcc(rawfile, mfccfile):
	os.system("x2x +sf < '%s' | frame -l 400 -p 160 | mfcc -l 400 -f 16 -n 40 -m 19 -E > '%s'" % (rawfile, mfccfile))

if __name__ == "__main__":
	if not os.path.exists(mfccDir): os.mkdir(mfccDir)

	for file in os.listdir(mp3Dir):
		if not file.endswith(".mp3"): continue
		mp3file = os.path.join(mp3Dir, file).encode("utf_8")
		mfccfile = os.path.join(mfccDir, file.replace(".mp3", ".mfc")).encode("utf_8")

		try:
			mp3_to_raw(mp3file, "temp.raw")
			calculate_mfcc("temp.raw", mfccfile)
			print "%s => %s" % (mp3file, mfccfile)

			os.remove("temp.raw")
		except:
			continue
