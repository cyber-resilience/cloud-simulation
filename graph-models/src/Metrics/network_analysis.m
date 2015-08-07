function network_analysis()
clear all;
close all;
[labels, num_vertices, num_vertices_multiscale, num_edges, flow_aggr, flow_filtered, edges_filtered] = textread('DATA/summary.csv', '%s %d %d %d %d %d %d', 'delimiter', ',', 'endofline', '\n');
N = length(labels);
k = 1;
max_eigenvalues = zeros(N, k);
filter_fraction = zeros(N, 1);
line_styles = ['rgbcmykw'];
figure;
N = 7;
for i = 1:N
%     path = strcat('DATA/spectra/nccdc-filtered-', labels(i), '.tsv.dimacs_WtdLap.mtx_allEigs');
%     eigen_values = load(char(path));
%     max_eigenvalues(i,:) = eigen_values(end); %(end-2:end);
%     filter_fraction(i) = 100*edges_filtered(i)/(num_edges(i) + edges_filtered(i));
%     
    %kcore_path = char(strcat('DATA/kcore/num_edges-10000/nccdc-filtered-', labels(i), '.tsv.kcore_summary.csv'));
    kcore_path = char(strcat('testbed-1', int2str(i), 'jun.txt.tsv.kcore_summary.csv'));
    disp(kcore_path);
    kcore_data = csvread(kcore_path);
    %figure;
    semilogy(kcore_data(2:7,2)); %, line_styles(i));
    %title(kcore_path);
    hold on;
    
%     pagerank_path = char(strcat('DATA/pagerank/num_edges-10000/nccdc-filtered-', labels(i), '.tsv_pagerank.csv'));
%     disp(pagerank_path);
%     pagerank = csvread(pagerank_path);
%     mode(pagerank)
%     %subplot(N, 1, i);
%     figure
%     bar(pagerank);
end
%filter_fraction
%max_eigenvalues
% plot(filter_fraction, max_eigenvalues, 'o');
% set(gca,'FontSize',14);
% xlabel('k-core Index', 'FontSize', 14);
% ylabel('Number of Vertices in k-th Core', 'FontSize', 14);
% title('Number of Edges in Aggegated Graph: 1M', 'FontSize', 14);
% %bar(filter_fraction, max_eigenvalues);
%axis equal;