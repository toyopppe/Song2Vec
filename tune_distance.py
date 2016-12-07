#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import numpy.linalg
import rpy2.robjects as robjects
from collections import defaultdict
sigDir = './sig'

robjects.r['library']('lpSolve')
transport = robjects.r['lp.transport']

def loadsig(sigfile):
	mat = []
	fp = open(sigfile, "r")
	for line in fp:
		line = line.rstrip()
		mat.append([float(x) for x in line.split()])
	fp.close()
	return np.array(mat)

def KLDiv(mu1, s1, mu2, s2):
	try:
		invs1 = np.linalg.solve(s1, numpy.identity(20))
	except numpy.linalg.linalg.LinAlgError:
		raise;
	try:
		invs2 = np.linalg.solve(s2, numpy.identity(20))
	except numpy.linalg.linalg.LinAlgError:
		raise;
	
	t1 = np.sum(np.diag(np.dot(invs2, s1)))
	t2 = (mu2 - mu1).transpose()
	t3 = mu2 - mu1
	return t1 + np.dot(np.dot(t2, invs2), t3)

def symKLDiv(mu1, s1, mu2, s2):
	return 0.5*(KLDiv(mu1, s1, mu2, s2) + KLDiv(mu2, s2, mu1, s1))

def calcEMD(sigfile1, sigfile2):
	sig1 = loadsig(sigfile1)
	sig2 = loadsig(sigfile2)

	numFeatures = sig1.shape[0]
	dist = np.zeros(numFeatures * numFeatures)

	for i in range(numFeatures):
		mu1 = sig1[i, 1:21].reshape(20, 1)
		s1 = sig1[i, 21:421].reshape(20, 20) + numpy.identity(20)
		for j in range(numFeatures):
			mu2 = sig2[j, 1:21].reshape(20, 1)
			s2 = sig2[j, 21:421].reshape(20, 20) + numpy.identity(20)
			dist[i * numFeatures + j] = symKLDiv(mu1, s1, mu2, s2)

	w1 = sig1[:,0]
	w2 = sig2[:,0]

	costs = robjects.r['matrix'](robjects.FloatVector(dist), nrow=len(w1), ncol=len(w2), byrow=True)
	
	row_signs = ["<"] * len(w1)
	row_rhs = robjects.FloatVector(w1)
	col_signs = [">"] * len(w2)
	col_rhs = robjects.FloatVector(w2)

	t = transport(costs, "min", row_signs, row_rhs, col_signs, col_rhs)
	flow = t.rx2('solution')

	dist = dist.reshape(len(w1), len(w2))
	flow = np.array(flow)
	work = np.sum(flow * dist)
	emd = work / np.sum(flow)
	return emd

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "f**k you!"
		sys.exit()
	
	targetSigPath = sys.argv[1]
	data = defaultdict(float)

	for sigFile in os.listdir(sigDir):
		sigPath = os.path.join(sigDir, sigFile)
		emd = calcEMD(targetSigPath, sigPath)
		if emd < 0: continue
		data[sigFile] = emd

	N = 10
	rank = 0
	for sigFile, emd in sorted(data.items(), key=lambda x:x[1], reverse=False)[:N]:
		fname = sigFile.split(".")
		if rank == 0: print "target song : %s" % fname[0]
		else: print "%d\t%.2f\t%s" % (rank, emd, fname[0])
		rank += 1
