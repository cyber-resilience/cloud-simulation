function  [score]=segment_edge_score(A)

%A: U times N matrix
U=size(A,1); N=size(A,2); 
B=A'*A;
[u eig_max]=eigs(B,1,'lm');
score=(2*A*u*u'-ones(U,1)*u'.^2).*spones(A);

%{
[row col]=find(A>0);
score1=sparse(zeros(U,N));
length(row)
for k=1:length(row)
    %k
    score1(row(k),col(k))=2*u'*A(row(k),:)'*u(col(k))-(u(col(k)))^2;
end
%}


