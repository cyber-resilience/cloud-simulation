function score=hardening_edge_score(P,A,E)

n=size(A,1); K=size(P,1);
J=(kron(P,ones(n,1)))'*A';
[y dummy]=eigs(J,1,'lm');

for i=1:K
    for j=1:n
        DE=0*speye(K,n);  DE(i,j)=1;
        score(i,j)=(P(i,j)-E(i,j))*y'*kron(DE,ones(n,1))'*A'*y;
    end
end

