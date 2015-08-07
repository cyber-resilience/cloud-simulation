function [H_sparse] = spectral_sparsifier(path)

disp('Loading graph ...');
[adj_matrix, num_vertices] = load_graph(path);

disp('Computing Laplacian ...');
L = get_laplacian(adj_matrix, num_vertices);
disp('Suppressing a row and column and computing the inverse of the rest');
D = zeros(num_vertices);
D(:, 1) = L(:,1);
D(1, :) = L(1, :);
D(2:num_vertices, 2:num_vertices) = inv(L(2:num_vertices, 2:num_vertices));

disp('Normalizing upper triangular matrix ...');
D_upper = triu(D, 1);
total = sum(sum(D_upper));
D_upper = D_upper/total;

disp('Creating arrays for probability and index data to sample ..');
N_upper = (num_vertices*num_vertices-num_vertices)/2;
disp(N_upper);
probability_dist = zeros(1, N_upper);
X = zeros(1, N_upper);
Y = zeros(1, N_upper);
k = 1;
for i = 2:num_vertices
    for j = 2:num_vertices
        probability_dist(k) = D(i, j);
        X(k) = i;
        Y(k) = j;
        k = k + 1;
    end
end

disp('Sampling NlogN edges ...')
N_sample = int64(num_vertices); %int64(num_vertices*log(num_vertices));
sampled_indices = discretesample(probability_dist, N_sample);

disp('Creating new sparse adjacency matrix ...');
fid = fopen('test.spectral_sparsified.csv', 'w');
H_sparse = zeros(num_vertices);
for i = 1:N_sample
    k = sampled_indices(i);
    x = X(k);
    y = Y(k);
    fprintf(fid, '%d,%d\n', x, y);
    H_sparse(x,y) = 1;
    H_sparse(y, x) = 1;
end
fclose(fid);
disp('Computing eigenvectors of L ...');
E = eig(L);
disp('Computing L_sparse ...');
L_sparse = get_laplacian(H_sparse, num_vertices);
disp('Computing eigenvectors of L_sparse ...');
E_sparse = eig(L_sparse);

%ADDED BY LUKE FOR PLOTTING
l = length(E);
index = zeros(l,1);
for i = 1:l
    index(i) = i/l;
end

%semilogy(E);
plot(index,E);
hold on;
%semilogy(E_sparse, 'k--');
plot(index, E_sparse, 'k--');