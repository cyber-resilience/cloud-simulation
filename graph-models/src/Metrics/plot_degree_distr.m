function plot_degree_distr(path, type, style)

if nargin < 3
    style = 'o';
end
is_dir = isdir(path);
%line_styles = ['rgbcmykw'];
line_styles = ['ggcrmgk'];
if is_dir
    disp('Loading files from directory ...');
    dirpath = path;
    files = dir(strcat(dirpath, '/*', type, '-deg.csv'));
    dims = size(files);
    num_files = dims(1);
    disp(strcat('Plotting first 8 entries out of ', num2str(num_files), ' files'))
    if num_files > 8 
        num_plots = 8;
    else
        num_plots = num_files;
    end 
    for i = 1:num_plots
        filepath = strcat(dirpath, '/', files(i).name);
        disp(strcat('    Processing ', filepath));
        dist = load(filepath);
        loglog(dist(:, 1), dist(:,2), strcat(line_styles(i), ''));
        hold on; 
    end 
    legend('06/11 normal', '06/12 normal', '06/13 infiltration', '06/14 HTTP DoS', '06/15 DDoS Botnet', '06/16 normal', '06/17 brute force SSH');
else
    dist = load(path);
    [pathstr,name,ext] = fileparts(path);
    loglog(dist(:, 1), dist(:,2), style);
    legend(name);
end
set(gca,'FontSize',14);
xlabel('Vertex degree', 'FontSize', 14);
ylabel('Number of vertices with specific degree', 'FontSize', 14);
if strcmp(type, 'in') == 1
    title('Incoming degree distribution', 'FontSize', 14);
elseif strcmp(type, 'out') == 1
    title('Outgoing degree distribution', 'FontSize', 14);
elseif strcmp(type, 'out') == 1
    title('Cumulative degree distribution', 'FontSize', 14);
else
    title('Degree distribution', 'FontSize', 14);
end