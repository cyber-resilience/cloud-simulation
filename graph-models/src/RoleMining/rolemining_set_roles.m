clear all;
file11 = '/Users/d3m432/Documents/MATLAB/mnms4graphs/roles/features.csv'
% file11 = 'ISCX-testbed11jun-feature_matrix.csv';
% file12 = 'ISCX-testbed12jun-feature_matrix.csv';
% file13 = 'ISCX-testbed13jun-feature_matrix.csv';
% file14 = 'ISCX-testbed14jun-feature_matrix.csv';
% file15 = 'ISCX-testbed15jun-feature_matrix.csv';
% file16 = 'ISCX-testbed16jun-feature_matrix.csv';
% file17 = 'ISCX-testbed17jun-feature_matrix.csv';
% 
% files = [file11; file12; file13; file14; file15; file16; file17;];
files = [file11];
num_files = 1;
r = 7;
%read file to matrix
V = csvread(files(1,:),0,1);
%read in node labels from first column of file
node_labels = csvread(files(1,:));
node_labels = node_labels(:,1);
%get unconstrained G and F
[G,F] = nnmf(V,r);
role_distribution = zeros(1, r);
num_nodes = size(G, 1);
fid_a = fopen('role_assignment.csv', 'w');
fid_d = fopen('role_distribution.csv', 'w');

for i = 1:num_nodes
    [role_strength, role] = max(G(i,:));
    role_distribution(role) = role_distribution(role) + 1;
    fprintf(fid_a, '%d\n', role);
end
for i = 1:r
    fprintf(fid_d, '%d\n', role_distribution(i));
end
fclose(fid_d);
fclose(fid_a);
save('role_description.txt', 'F', '-ascii');

% G_out = sprintf('node-by-role%d.csv',r);
% dlmwrite(G_out,[node_labels G], 'delimiter', ',', 'precision',12);
% for f = 2:num_files
%     V1 = csvread(files(f,:),0,1);
%     node_labels = csvread(files(f,:));
%     node_labels = node_labels(:,1);
%     G1 = V1*pinv(F);
%     G_out = sprintf('ISCX-%s-node-by-role%d_forcedF.csv',files(f,13:17),r);
%     dlmwrite(G_out,[node_labels G1], 'delimiter', ',', 'precision',12);
% end