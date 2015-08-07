function y = set_roles(files, in_path, r)
num_files = size(files,2);

%read in first feature matrix for training to define roles
V = dlmread(strcat(in_path,files(1,:)),' ',0,1);
[n,m] = size(V);

%initialize G and F
%includes option to read from file if wanting to use a previously generated
%matrix
init_G = rand(n,r);
dlmwrite('initial_G.csv', init_G, 'delimiter',',','precision',12);
init_F = rand(r,m);
dlmwrite('initial_F.csv', init_F, 'delimiter',',','precision',12);
%init_G = dlmread('initial_G.csv',',');
%init_F = dlmread('initial_F.csv',',');


%read in node labels from first column of file
node_labels = dlmread(strcat(in_path,files(1,:)), ' ');
node_labels = node_labels(:,1);
%get unconstrained G and F
[G,F] = nnmf(V,r,'w0',init_G,'h0',init_F);
G_out = sprintf('%s-node-by-role%d_forcedF.csv',files(1,1:(length(files(1))-4)),r);
F_out = sprintf('%s-role%d-by-feature_forcedF.csv',files(1,1:(length(files(1))-4)),r);
dlmwrite(strcat(in_path,G_out),[node_labels G], 'delimiter', ',', 'precision',12);
dlmwrite(strcat(in_path,F_out), F, 'delimiter',',','precision',12);
%read in remaining files and get node assignments
for f = 2:num_files
    V1 = dlmread(strcat(in_path,files(f,:)),' ',0,1);
%     node_labels = dlmread(strcat(in_path,files(f,:)),' ');
%     node_labels = node_labels(:,1);
    G1 = V1*pinv(F);
    G_out = sprintf('%s-node-by-role%d_forcedF.csv',files(f,1:(length(files(f))-4)),r);
    dlmwrite(strcat(in_path,G_out),[node_labels G1], 'delimiter', ',', 'precision',12);
end
end