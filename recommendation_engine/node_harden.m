function [anew]=node_harden(score_node,a,k)

[score_sort ind_score]=sort(score_node,'descend');
anew=a;
anew(ind_score(1:k))=1;

 if(nnz(a-anew)~=k)
     error('hardening problem')
 end