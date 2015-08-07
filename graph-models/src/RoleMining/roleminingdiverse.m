%define number of roles to be used
roles = 6;
%set file to be used
file = 'ISCX-testbed11jun-feature_matrix.csv';
%read file to matrix
V = csvread(file,0,1);
%read in node labels from first column of file
node_labels = csvread(file);
node_labels = node_labels(:,1);
%get number of nodes and features
[nodes, features] = size(V);
%get unconstrained G and F
[G,F] = nnmf(V,roles);
L1 = geterror(V, G*F,roles);
L2 = L1;
%define upper bound on amount of allowable diverseness
dG = 0.5;
dF = 0.5;
% solve for each role (i.e. column of G and corresponding row of F)
while L2 <= L1
    for k = 1:roles
        %compute residual matrix
        Gk = [G(:,1:k-1) G(:,k+1:roles)];
        Fk = F([1:k-1,k+1:roles],:);
        R = V - (Gk*Fk);
        cvx_begin
            variable x1(nodes)
            minimize( norm(R - x1*F(k,:), 2) )
        cvx_end
        cvx_begin
            variable y1(nodes)
            minimize( norm(x1 - y1, 2) )
            subject to
                for j = 1:roles
                    if j ~= k
                        transpose(y1)*G(:,j) <= dG;
                    end
                end
        cvx_end
        cvx_begin
            variable x2(nodes)
            minimize( norm(R - x2*G(:,k), 2) )
        cvx_end
        cvx_begin
            variable y2(nodes)
            minimize( norm(x2 - y2, 2) )
            subject to
                for j = 1:roles
                    if j ~= k
                        F(j,:)*transpose(y2) <= dF;
                    end
                end
        cvx_end
        G = [G(:,1:k-1) y1 G(:,k+1:roles)];
        F = [F(1:k-1,:); y2; F(k+1:roles,:)];
        L1 = L2;
        L2 = geterror(V, G*F,roles);
    end
end
csvwrite('ISCX-11jun-diverseG6.csv', [node_labels G]);
csvwrite('ISCX-11jun-diverseF6.csv', [node_labels F]);