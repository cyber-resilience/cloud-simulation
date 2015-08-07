function plot_spectra(path)

is_dir = isdir(path);
line_styles = ['rgbcmykw'];
if is_dir
    disp('Loading files from directory ...');
    dirpath = path;
    files = dir(strcat(dirpath, '/*CombLap.mtx_allEigs'));
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
        %disp(strcat('    Processing ', filepath));
        plot_eigenvalues(filepath, line_styles(i));
        hold on;
    end 
    %legend('dsdsds')
else
    plot_eigenvalues(path, 'r--');
end

function plot_eigenvalues(file, line_style)
disp(file);
eigen_values = load(file);
%fig_id = figure;
figure
semilogy(eigen_values, line_style);
%hold on;
axis tight;
xlabel('Eigen values');
ylabel('Magnitude of eigen values');
%title(strcat('Eigenvalue distribution for  ', strrep(file, '_', '-')));
% outfig = strcat(file, '.jpg');
% saveas(fig_id, outfig);
% outfig = strcat(file, '.eps');
% saveas(fig_id, outfig);


