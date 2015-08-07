function [ output_args ] = output_top_k_files( directory, extension, k )
%UNTITLED2 Writes out the *.topk.csv files for every file with the given
%extension in the directory. This needs to be run from a folder that
%contains the top_k.m file
%   @PARAM directory:   directory with target files, and where files will be
%   written
%   @PARAM extension:   file extension of input files without the '.' (csv, tsv...)
%   @PARAM k:           number of top eigenvalues to compute
files = dir(strcat(directory, '*.', extension));
for file=files'
    disp(strcat('Processing: ', file.name))
    [eigenvalues, vertices, edges] = top_k(strcat(directory, file.name), k);
    dlmwrite(strcat(directory, file.name, '.top', int2str(k), '.csv'), eigenvalues, ',');
end