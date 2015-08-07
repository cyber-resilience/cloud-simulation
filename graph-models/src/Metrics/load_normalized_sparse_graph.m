function [ norm_lap , a ] = load_sparse_graph(path)
%Returns the normalized laplacian in sparse matrix form
edges = csvread(path) + 1;
a = max(max(edges));
b = 2*length(edges(:,1));
degrees = zeros(a,1);
for i = 1:b/2
    degrees(edges(i,1)) = degrees(edges(i,1))+1;
    degrees(edges(i,2)) = degrees(edges(i,2))+1;
end
%need to count edges in both directions for it to be symmetric
edges = [edges;[edges(:,2),edges(:,1)]];
for i = 1:b
    edges(i,3) = -1/sqrt(degrees(edges(i,1))*degrees(edges(i,2)));
end
for i = 1:a
    edges(b+i, :) = [i,i,1];
end
norm_lap = sparse(edges(:,1), edges(:,2), edges(:,3), a, a);
end

