clear All;
close all;
path(path, '../Metrics');
% file1 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-11jun.features.dat';
% file2 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-12jun.features.dat';
% file3 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-13jun.features.dat';
% file4 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-14jun.features.dat';
% file5 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-15jun.features.dat';
% file6 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-16jun.features.dat';
% file7 = 'C:\Users\oler571\Desktop\New folder\MnMs\ISCX_flo_features\filteredtestbed-17jun.features.dat';
% 
% files = [file1; file2; file3; file4; file5; file6; file7];
dirpath = 'DATA/iscx';
pattern = '*features.dat';
files = dir(strcat(dirpath, '/', pattern));
num_files = size(files, 1);
r = 3;
training_day = 3;

titles = {'Normal Activity', 'Normal Activity', 'Inside-infiltration', 'HTTP DoS', 'DDoS using IRC Botnet', 'Normal Activity', 'Brute Force SSH'};
for training_day = 1:num_files
    training_file = files(training_day).name;
    training_path = strcat(dirpath, '/', training_file);

    %read file to matrix
    disp(strcat('Training from: ', training_path));
    V0 = dlmread(training_path, ' ',0,1);
    V = [V0(:,1:4) V0(:, 7:12)];
    [n,m] = size(V);
    init_G = rand(n,r);
    init_F = rand(r,m);
    %modifying to remove number of bytes as a feature
    %Vi = csvread(files(1,:),0,0);
    %Vj = csvread(files(1,:),0,7);
    %V = [Vi(:,1:5) Vj];
    %read in node labels from first column of file
    % DELtmp = dlmread(training_path, ' ');
    node_labels = dlmread(training_path, ' ', [0 0 (n-1) 0]); %tmp(:,1);
    %disp(node_labels);
    %get unconstrained G and F
    [G,F] = nnmf(V,r,'w0',init_G,'h0',init_F);
    %features = {'in-triangle', 'out-triangles', 'through-triangles', 'cycles', 'out-degree', 'in-degree', 'pagerank', 'k-core rank', 'inflow-size', 'outflow-size', 'inflow-duration', 'outflow-duration'};
    features = {'in-triangle', 'out-triangles', 'through-triangles', 'cycles', 'pagerank', 'k-core rank', 'inflow-size', 'outflow-size', 'inflow-duration', 'outflow-duration'};
    figure;
    disp(training_day);
    h = figure;
    barh(F.');
    title(titles(training_day));
    legend('Role A', 'Role B', 'Role C', 'Role D');
    set(gca, 'YTickLabel', features);
    set(gca, 'FontSize', 14);
    save_fig(h, 'figs', strcat(training_file, '_role_defs', sprintf('_%d', r)));
    close(h);
end
% for i = 1:r
%     figure;
%     barh(F(i, :));
%     set(gca, 'YTickLabel', features);
%     set(gca, 'FontSize', 14);
% end
return

% G_out = sprintf('%s-node-by-role%d_forcedF%d.csv',files(1,68:81),r,training_day);
% F_out = sprintf('%s-role%d-by-feature_forcedF%d.csv',files(1,68:81),r,training_day);
% dlmwrite(G_out,[node_labels G], 'delimiter', ',', 'precision',12);
% dlmwrite(F_out, F, 'delimiter',',','precision',12);
% for f = 2:num_files
%     path = strcat(dirpath, '/', files(f,:).name);
%     V1 = dlmread(path,' ',0,1);
%     %V1i = csvread(files(f,:),0,0);
%     %V1j = csvread(files(f,:),0,7);
%     %V1 = [V1i(:,1:5) V1j];
%     %node_labels = dlmread(files(f,:),' ');
%     node_labels = dlmread(path,' ', [0, 0 (size(V1, 1)-1) 0]);
%     G1 = V1*pinv(F);
%     G_out = sprintf('%s-node-by-role%d_forcedF%d.csv',files(f,68:81),r,training_day);
%     F_out = sprintf('%s-role%d-by-feature_forcedF%d.csv',files(1,68:81),r,training_day);
%     dlmwrite(G_out,[node_labels G1], 'delimiter', ',', 'precision',12);
%     dlmwrite(F_out, F, 'delimiter',',','precision',12);
% end