function [A W]=bipartite_random(n,m,p,weight)

A=double((rand(n,m)<=p));
if(weight==1)
    W=A.*rand(size(A));
elseif(weight==0)
    W=A;
else
    error('weight not specified')
end


