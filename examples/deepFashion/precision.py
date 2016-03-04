import numpy as np
from scipy.spatial import distance
def precision (trn_label, trn_binary, tst_label, tst_binary, top_k, mode):
    K = top_k;
    QueryTimes = tst_binary.shape[0]
    correct = np.zeros((K,1));
    total = np.zeros((K,1));
    error = np.zeros((K,1));
    AP = np.zeros((QueryTimes,1));

    Ns = np.arange(1,K+1)
    sum_tp = np.zeros((1, Ns.size))




    for i in range(QueryTimes):
        query_label = tst_label[i];
        print 'query',i,'\n'
        query_binary = np.array([tst_binary[i,:]])

        if mode==1:
            similarity = distance.cdist(trn_binary,query_binary,'hamming')
        elif mode ==2:
            similarity = distance.cdist(trn_binary,query_binary,'euclidean')

        
        y2=np.argsort(similarity[:,0]);
        
        buffer_yes = np.zeros((K,1));
        total_relevant = 0;
        
        for j in range(K):
            retrieval_label = trn_label[y2[j]];
            
            if (query_label==retrieval_label):
                buffer_yes[j,0] = 1;
                total_relevant = total_relevant + 1;

        assert(np.sum(buffer_yes)==total_relevant)
        
        # % compute precision

        P = np.true_divide(np.cumsum(buffer_yes),Ns);
        buffer_yes=buffer_yes[:,0]

        if (np.sum(buffer_yes) == 0):
           AP[i] = 0;
        else:
           AP[i] = np.dot(P,buffer_yes) / np.sum(buffer_yes);

        assert(AP[i]>=0 and AP[i]<=1)
       
        sum_tp = sum_tp + np.cumsum(buffer_yes)

    precision_at_k = np.true_divide(sum_tp,(Ns * QueryTimes))
    mapRes = np.mean(AP);
    
    return mapRes, precision_at_k
