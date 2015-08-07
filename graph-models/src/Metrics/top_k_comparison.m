function [ cores, vertex_count, edge_count, all_eigenvalues ] = top_k_comparison( graph_name, k )
%The graph name should be the contents of the original graph. For example,
%if I were working with p2p-Gnutella31.tsv.norm.tsv originally, the graph name would
%be p2p-Gnutella31.
files = dir(strcat(graph_name, '.tsv.norm.tsv'));
files = [files; dir(strcat('kcore_', graph_name, '.*.tsv.norm.tsv'))];
len = length(files);
cores = zeros(len, 1);
vertex_count = zeros(len, 1);
edge_count = zeros(len, 1);
all_eigenvalues = [];
i = 1;
for file=files'
    [eigenvalues, vertices, edges] = top_k(file.name, k);
    elements = strsplit(file.name, '.');
    cores(i) = str2double(char(elements(2)));
    vertex_count(i) = vertices;
    edge_count(i) = edges;
    all_eigenvalues = [all_eigenvalues, eigenvalues];
    i = i+1;
end
