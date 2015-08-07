function save_eigs(out_dir, name, eigenvalues)
n = length(eigenvalues);
eigenvalues = [eigenvalues, zeros(n,1)];
for i = 1:n
    eigenvalues(i,2) = eigenvalues(i,1);
    eigenvalues(i,1) = i/n;
end
dlmwrite(strcat(out_dir, name, '-eigs.tsv'), eigenvalues, '\t');
end
