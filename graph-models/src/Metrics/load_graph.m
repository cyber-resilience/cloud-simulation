function [adj_mat, num_vertices] = load_graph(tsv_path)
edge_data = dlmread(tsv_path, ' ') + 1;
nrows = size(edge_data, 1);

num_vertices = 0;
for i = 1:(nrows-1)
    if edge_data(i, 1) > num_vertices
        num_vertices = edge_data(i, 1);
    end
    if edge_data(i, 2) > num_vertices
        num_vertices = edge_data(i, 2);
    end
end

adj_mat = zeros(num_vertices);
for i = 1:(nrows-1)
    u = edge_data(i, 1);
    v = edge_data(i, 2);
    adj_mat(u, v) = 1;
    adj_mat(v, u) = 1;
end