import numpy as np
def precision (trn_label, trn_binary, tst_label, tst_binary, top_k, mode):
	K = top_k;
	QueryTimes = tst_binary.shape[1]
	print QueryTimes
	
