import numpy as np
from scipy.spatial import distance
def precision (trn_label, trn_binary, tst_label, tst_binary, top_k, mode):
    K = top_k;
    QueryTimes = tst_binary.shape[0]
    print QueryTimes
    correct = np.zeros((K,1));
    total = np.zeros((K,1));
    error = np.zeros((K,1));
    AP = np.zeros((QueryTimes,1));

    Ns = np.arange(1,K+1)
    sum_tp = np.zeros((1, Ns.size))

    for i in range(QueryTimes):
        query_label = tst_label[i];
	print query_label
        print 'query',i,'\n'
	print tst_binary.shape
        query_binary = tst_binary[i,:]
	
	print query_binary.shape
	print tst_binary.shape
        if mode==1:
            similarity = distance.cdist(trn_binary,query_binary,'hamming')
        elif mode ==2:
            similarity = distance.cdist(trn_binary,query_binary,'euclidean')

        y2=np.argsort(similarity);
        
        buffer_yes = np.zeros((K,1));
        buffer_total = np.zeros((K,1));
        total_relevant = 0;
        
        for j in range(K):
            retrieval_label = trn_label(y2[j]);
            
            if (query_label==retrieval_label):
                buffer_yes[j,1] = 1;
                total_relevant = total_relevant + 1;

            buffer_total[j,1] = 1;
        
        # % compute precision
        P = np.true_divide(np.cumsum(buffer_yes),Ns);
        
        if (np.sum(buffer_yes) == 0):
           AP[i] = 0;
        else:
           AP[i] = np.sum(np.multiply(P,buffer_yes)) / np.sum(buffer_yes);
       
        sum_tp = sum_tp + cumsum(buffer_yes)

    precision_at_k = np.true_divide(sum_tp,(Ns * QueryTimes))
    mapRes = np.mean(AP);
    
    return mapRes, precision_at_k
