#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import numpy as np
import rpy2.robjects as rob

rob.r['library']('lpSolve')
transport = rob.r['lp.transport']

def ed(feature1, feature2):
	return np.sqrt(np.sum((feature1 - feature2) ** 2))

def emd(dist, w1, w2):
	costs = rob.r['matrix'](rob.FloatVector(dist),nrow=len(w1),ncol=len(w2),byrow=True)
	print costs
	row_signs = ["<"] * len(w1)
	row_rhs = rob.FloatVector(w1)
	col_signs = [">"] * len(w2)
	col_rhs = rob.FloatVector(w2)

	print("start")
	t = []
	t = transport(costs, "min", row_signs, row_rhs, col_signs, col_rhs)
	print t
	flow = t.rx2('solution')
	print flow

	dist = dist.reshape(len(w1), len(w2))
	flow = np.array(flow)
	work = np.sum(flow*dist)
	emd = work / np.sum(flow)
	return emd

if __name__ == "__main__":
	f1 = np.array([[100, 40, 22], [211, 20, 2], [32, 190, 150], [2, 100, 100]])
	f2 = np.array([[0, 0, 0], [50, 100, 80], [255, 255, 255]])

	w1 = np.array([4., 3., 2., 1.])
	w2 = np.array([5., 3., 2.])

	n1 = len(f1)
	n2 = len(f2)

	dist = np.zeros(n1 * n2)
	for i in range(n1):
		for j in range(n2):
			dist[i * n2 + j] = ed(f1[i], f2[j])
	print "emd =", emd(dist, w1, w2)
