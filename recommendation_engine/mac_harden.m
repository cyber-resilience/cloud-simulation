function [Pnew anew]=mac_harden(edgelist_harden,P,E,a)

m=size(edgelist_harden,1);
Pnew=P;
for z=1:m
    Pnew(edgelist_harden(z,1),edgelist_harden(z,2))=E(edgelist_harden(z,1),edgelist_harden(z,2));
end

 %anew=1-sum(Pnew)';  anew(find(anew<0))=0;
 anew=a;
 
 if(nnz(P-Pnew)~=m)
     error('hardening problem')
 end