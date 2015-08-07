clear All;
file1 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-11jun.features.dat';
file2 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-12jun.features.dat';
file3 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-13jun.features.dat';
file4 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-14jun.features.dat';
file5 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-15jun.features.dat';
file6 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-16jun.features.dat';
file7 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-17jun.features.dat';

files = [file1; file2; file3; file4; file5; file6; file7];
disp(files(1,68:81));
return;
num_files = 7;
r = 2;
training_day = 12;

V0 = dlmread(files(1,:),' ',0,1);
%initialize G and F
[n,m] = size(V);
init_G = rand(n,r);
init_F = rand(r,m);

% %read initial matrices to be used in nnmf from file
% %this fixes problem of getting slightly different output every time
% init_G = dlmread('initial_G.csv',',');
% init_F = dlmread('initial_F.csv',',');
%read file to matrix
V = dlmread(files(1,:),' ',0,1);
%modifying to remove number of bytes as a feature
%Vi = csvread(files(1,:),0,0);
%Vj = csvread(files(1,:),0,7);
%V = [Vi(:,1:5) Vj];
%read in node labels from first column of file
node_labels = dlmread(files(1,:), ' ');
node_labels = node_labels(:,1);
%get unconstrained G and F
[G,F] = nnmf(V,r,'w0',init_G,'h0',init_F);

G_out = sprintf('%s-node-by-role%d_forcedF%d.csv',files(1,68:81),r,training_day);
F_out = sprintf('%s-role%d-by-feature_forcedF%d.csv',files(1,68:81),r,training_day);
dlmwrite(G_out,[node_labels G], 'delimiter', ',', 'precision',12);
dlmwrite(F_out, F, 'delimiter',',','precision',12);
for f = 2:num_files
    V1 = dlmread(files(f,:),' ',0,1);
    %V1i = csvread(files(f,:),0,0);
    %V1j = csvread(files(f,:),0,7);
    %V1 = [V1i(:,1:5) V1j];
    node_labels = dlmread(files(f,:),' ');
    node_labels = node_labels(:,1);
    G1 = V1*pinv(F);
    disp(files(f,68:81));
    return;
    G_out = sprintf('%s-node-by-role%d_forcedF%d.csv',files(f,68:81),r,training_day);
    F_out = sprintf('%s-role%d-by-feature_forcedF%d.csv',files(1,68:81),r,training_day);
    dlmwrite(G_out,[node_labels G1], 'delimiter', ',', 'precision',12);
    dlmwrite(F_out, F, 'delimiter',',','precision',12);
end