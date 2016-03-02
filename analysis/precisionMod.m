function [mapping] = precisionMod(trn_label, trn_binary, tst_label, tst_binary, top_k, mode, fileTest, fileTrain)   
K = top_k;
QueryTimes = size(tst_binary,2);


QueryTimes=5;
K=5;
mapping=repmat({''},QueryTimes,K+1);
for i = 1:QueryTimes
    mapping{i,1}={fileTest{i}};
    fprintf('query %d\n',i);
    query_binary = tst_binary(:,i);
    if mode==1
    tic
    similarity = pdist2(trn_binary',query_binary','hamming');
    toc
    fprintf('Complete Query [Hamming] %.2f seconds\n',toc);
    elseif mode ==2
    tic
    similarity = pdist2(trn_binary',query_binary','euclidean');
    toc
    fprintf('Complete Query [Euclidean] %.2f seconds\n',toc);
    end
    [x2,y2]=sort(similarity);
    for j = 1:K
        mapping{i,j+1}={fileTrain{y2(j)}};
    end
end  

end
