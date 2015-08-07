ratios = load('DATA/shortest_path/shortest_path_ratios.csv');
plot(ratios, '*');
set(gca, 'FontSize', 14);
xlabel('Vertex Pairs');
ylabel('d\_L1/d\_flat');