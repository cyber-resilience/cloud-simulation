function [ eigenvalues ] = get_eigenvalues( path )
tic
disp('Loading sparse graph...');
edge_list = dlmread(path);
edge_list = edge_list+1;
a = length(edge_list);
b = max(max(edge_list));
Adj = zeros(b);
for i = 1:a
    if edge_list(i,1) ~= edge_list(i,2)
        Adj(edge_list(i,1), edge_list(i,2)) = -1;
        Adj(edge_list(i,2), edge_list(i,1)) = -1;
    end
end
for i = 1:b
    Adj(i,i) = -sum(Adj(i,:));
end
for i = 1:b
    for j = 1:b
        if i~=j && Adj(i,j)~=0
            Adj(i,j) = Adj(i,j)/sqrt(Adj(i,i)*Adj(j,j));
        end
    end
end
for i = 1:b
    Adj(i,i) = 1;
end
matrix = Adj;
toc
disp('Computing Eigenvalues...');
tic
eigenvalues = eig(matrix);
eigenvalues = sort(eigenvalues);
toc
disp('Generating and saving figures...');
tic
plot(eigenvalues);
set(gca, 'FontSize', 14);
xlabel('EigenValues', 'FontSize', 14);
ylabel('Magnitude of eigenvalues', 'FontSize', 14);
ylim([0,2]);
[pathstr,name,ext] = fileparts(path);
title(strcat('Graph spectra from  ', name), 'FontSize', 14);
h = gcf;
save_fig(h, 'C:\Users\rodr144\Documents\MATLAB\Spectral Analysis\Figures', name);
save_eigs('C:\Users\rodr144\Documents\MATLAB\Spectral Analysis\Eigenvalues\', name, eigenvalues);
toc
end
