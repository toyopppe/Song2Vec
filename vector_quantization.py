#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import os
import struct
import sys
import numpy as np
import scipy.cluster
import eyeD3
mfccDir='mfcc'
sigDir ='./sig'

def loadMFCC(mfccfile, dimension):
	mfcc = []
	fp = open(mfccfile, "rb")
	while True:
		b = fp.read(4)
		if b == "": break
		val = struct.unpack("f", b)[0]
		mfcc.append(val)
	fp.close()

	mfcc = np.array(mfcc)
	numframe = len(mfcc) / dimension
	mfcc = mfcc.reshape(numframe, dimension)
	return mfcc


def VQ(mfcc, k):
	codebook, destortion = scipy.cluster.vq.kmeans(mfcc, k)
	code, dist = scipy.cluster.vq.vq(mfcc, codebook)
	return code

if __name__ == "__main__":
	if not os.path.exists(sigDir): os.mkdir(sigDir)
	
	for file in os.listdir(mfccDir):
		if not file.endswith(".mfc"): continue
		mfccfile = os.path.join(mfccDir, file)
		sigfile = os.path.join(sigDir, file.replace(".mfc", ".sig"))
		print mfccfile, "=>", sigfile

		fout = open(sigfile, "w")

		mfc = loadMFCC(mfccfile, 20)
		mfcc = np.delete(mfc, np.where(mfc==0)[0],0)
		code = VQ(mfcc, 16)

		for k in range(16):
			frames = np.array([mfcc[i] for i in range(len(mfcc)) if code[i] == k])
			m = np.apply_along_axis(np.mean, 0, frames)
			sigma = np.cov(frames.T)
			w = len(frames)

			features = np.hstack((w, m, sigma.flatten()))
			features = [str(x) for x in features]
			print features
			fout.write(" ".join(features) + "\n")
		fout.close()
