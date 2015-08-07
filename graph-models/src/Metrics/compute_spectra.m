%function [adj_matrix, num_vertices, degrees, lambda] = compute_spectra(path)
function [algeb_connec, lambda, norm_graph_laplacian] = compute_spectra(path)

disp('Loading graph ...');
[adj_matrix, num_vertices] = load_graph(path);
% disp('Computing degrees ...');
% degrees = zeros(num_vertices, 1);
% 
% for i = 1:num_vertices
%     degrees(i) = nnz(adj_matrix(:, i));
% end
% 
% disp('Computing graph Laplacian ...');
% norm_graph_laplacian = zeros(num_vertices);
% 
% for i = 1:num_vertices
%     for j = 1:num_vertices
%         if i == j && degrees(i) ~= 0
%             %norm_graph_laplacian(i, i) = 1;
%             norm_graph_laplacian(i, i) = degrees(i);
%         elseif i ~= j && adj_matrix(i, j) ~= 0
%             %norm_graph_laplacian(i, j) = -1/sqrt(degrees(i)*degrees(j));
%             norm_graph_laplacian(i, j) = -1;
%         end
%     end
% end

norm_graph_laplacian = get_laplacian(adj_matrix, num_vertices);

% disp('Computing top 6 Eigenvalues of Laplacian matrix ...');
% d = eigs(norm_graph_laplacian);
% %disp(d);
% %algeb_connec = d(2);
% disp(algeb_connec);
% disp('Computing Eigenvalues of Laplacian matrix ...');
%lambda = eig(norm_graph_laplacian);
lambda = eig(adj_matrix);
%plot(lambda)
algeb_connec = lambda(2);
%disp(lambda(2));
N = size(lambda, 1);
%disp(N)
%disp(lambda(N-1));
disp('Spectral gap = ');
disp(lambda(N) - lambda(N-1));
disp('-----');
% downsampling_factor = int32(num_vertices/100);
% lambda_s = downsample(lambda, downsampling_factor);
% out_path = sprintf('%s.spectra.csv', path);
% disp('Storing downsampled spectra ...');
% disp(out_path);
% fid = fopen(out_path, 'w');
% for i = 1:size(lambda_s, 1)
%     if lambda_s(i) < 0.000001
%         lambda_s(i) = 0
%     end
%     fprintf(fid, '%f\n', lambda_s(i));
% end
% fclose(fid);

% semilogy(lambda(2:size(lambda, 1)));
% set(gca, 'FontSize', 14);
% xlabel('EigenValues', 'FontSize', 14);
% ylabel('Magnitude of eigenvalues', 'FontSize', 14);
% 
% [pathstr,name,ext] = fileparts(path);
% title(strcat('Graph spectra from ', name), 'FontSize', 14);