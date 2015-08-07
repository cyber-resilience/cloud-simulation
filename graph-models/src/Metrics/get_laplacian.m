function [ norm_graph_laplacian ] = get_laplacian( adj_matrix, num_vertices )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
disp('Computing degrees ...');
degrees = zeros(num_vertices, 1);

for i = 1:num_vertices
    degrees(i) = nnz(adj_matrix(:, i));
end

disp('Computing graph Laplacian ...');
norm_graph_laplacian = zeros(num_vertices);

for i = 1:num_vertices
    for j = 1:num_vertices
        if i == j && degrees(i) ~= 0
            norm_graph_laplacian(i, i) = 1;
            %norm_graph_laplacian(i, i) = degrees(i);
        elseif i ~= j && adj_matrix(i, j) ~= 0
            norm_graph_laplacian(i, j) = -1*adj_matrix(i, j)/sqrt(degrees(i)*degrees(j));
            %norm_graph_laplacian(i, j) = -1*adj_matrix(i, j); %-1;
        end
    end
end


end

