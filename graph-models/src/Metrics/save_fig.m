function save_fig(fig_handle, out_dir, fig_desc)

fig_desc = strrep(fig_desc, '.', '-');
%extensions = {'fig', 'jpg', 'eps', 'pdf'};
%formats = {'fig', 'jpg', 'epsc', 'pdf'};

extensions = {'jpg'};
formats = {'jpg'};

for i = 1:size(formats, 2)
    fig_path = strcat(out_dir, '/', fig_desc, '.', extensions{i});
    disp(strcat('INFO Saving figure: ', fig_path));
    saveas(fig_handle, fig_path, formats{i});
end

end
