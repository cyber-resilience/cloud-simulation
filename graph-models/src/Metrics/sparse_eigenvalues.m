function [ eigenvalues ] = sparse_eigenvalues( file_path, directory )
%Takes a csv input file and saves a figure and a tsv file of eigenvalues to the specified directory.
%If is_normalized == 0, additional code is run to normalize the input file.
tic
%if is_normalized ~= 0
    disp('Loading normalized sparse graph...');
    [sparse_matrix,a] = load_normalized_sparse_graph(file_path);
%else
%    disp('Loading unnormalized sparse graph...');
%    [sparse_matrix,a] = load_unnormalized_sparse_graph(file_path);
%end
toc
disp('Computing Eigenvalues...');
tic
eigenvalues = eig(sparse_matrix);
eigenvalues = sort(eigenvalues);
toc
disp('Generating and saving figures...');
tic
plot(eigenvalues);
set(gca, 'FontSize', 14);
xlabel('EigenValues', 'FontSize', 14);
ylabel('Magnitude of eigenvalues', 'FontSize', 14);
ylim([0,2]);
[pathstr,name,ext] = fileparts(file_path);
title(strcat('Graph spectra from  ', name), 'FontSize', 14);
h = gcf;
save_fig(h, directory, name);
save_eigs(directory, name, eigenvalues);
toc
end