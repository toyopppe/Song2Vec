#!/usr/bin/env pyhton
#! -*- coding: utf-8 -*-
import os
import struct
import sys
import numpy as np

if len(sys.argv) != 2:
	print "f**k you!"
	sys.exit()

mfccfile = sys.argv[1]
dimension = 20

mfcc = []
f = open(mfccfile, "rb")
while True:
	b = f.read(4)
	if b == "": break;
	val = struct.unpack("f", b)[0]
	mfcc.append(val)
f.close()

mfcc = np.array(mfcc)
print mfcc
numframe = len(mfcc) / dimension

if numframe * dimension != len(mfcc):
	print "ERROR"
	sys.exit(1)

mfcc = mfcc.reshape(numframe, dimension)
#for i in range(len(mfcc)):
#	print "\t".join("%.2f" % x for x in mfcc[i,])
