function r_s=cascading_tripartite(A,P,B,a,r_initial);

n=length(r_initial);
J=B+(kron(P,ones(n,1)))'*A';

flag=1;
r_old=r_initial;
while(flag)
    r_tmp=r_old+J*r_old;
    % treshold 
    r_new_tmp=r_tmp; r_new_tmp(find(r_tmp>1))=1;
    % compare to hardening level
    ind=find(r_new_tmp-a>0);
    r_new=r_initial; r_new(ind)=1;
    if(nnz(r_new-r_old)==0)
        flag=0;
        r_s=r_new;
    else
        r_old=r_new;
    end
end