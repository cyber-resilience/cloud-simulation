function r_s=cascading_bypartite(B,r_initial);

flag=1;
r_old=r_initial;
while(flag)
    r_tmp=r_old+B*r_old;
    r_new=r_tmp; r_new(find(r_tmp>1))=1;
    if(nnz(r_new-r_old)==0)
        flag=0;
        r_s=r_new;
    else
        r_old=r_new;
    end
end