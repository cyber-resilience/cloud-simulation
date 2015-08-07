clear all;
close all;
file1 = 'DATA/iscx/testbed-17jun.features.dat';
%file1 = 'ISCX-testbed13jun-feature_matrix.csv';
%file2 = 'nccdc-filtered-none.tsv_degree_values.txt';
%V1 = dlmread(file2,'\t',0,1);
%V2 = csvread(file1,0,1);
%V = [V1 V2];
V = dlmread(file1,' ',0,1); %V2;
[r,c] = size(V);
L = [];
bins = floor(log2(r));
for n = 2:(c-1)
    [G,F] = nnmf(V,n);
    GF = G*F;
    vec = [];
    %represent GF as single vector for measuring description length
    for row = 1:r
        vec = [vec GF(row,:)];
    end
    %define boundaries for initial bins
    bounds = [min(vec)];
    bin_size = (max(vec) - min(vec))/bins;
    for k = 1:(bins - 1)
        bounds = [bounds (min(vec) + bin_size*k)];
    end
    bounds = [bounds (max(vec) + 1)];
    %define value to represent each bin (avg of upper and lower bound)
    initcodebook = [];
    for b = 1:bins
        initcodebook = [initcodebook (bounds(b) + ((bounds(b + 1) - bounds(b))/2))];
    end 
    %define vector replacing original values of vec with the code
    %corresponding to the appropriate bin
    pvec = [];
    for e = 1:(r*c)
       f = 1;
       while (vec(e) > bounds(f) && f < bins)
          f = f + 1;
       end
       pvec = [pvec initcodebook(f)];
    end
    %apply lloyd-max quantization algorithm 
    [partition, codebook] = lloyd(vec, bounds, initcodebook);
    for iter = 1:20
       [partition, codebook] = lloyd(vec, partition, codebook); 
    end
    %find number of values in each bin
    counts = zeros(bins);
    for e = 1:(r*c)
       f = 1;
       while (vec(e) > partition(f) && f < bins)
          f = f + 1;
       end
       counts(f) = counts(f) + 1;
    end
    %use values per bin to create probability vector where each entry
    %is the probability that a randomly selected value belongs
    %in that bin
    probs = [];
    for p = 1:bins
       probs = [probs (counts(p)/(r*c))];
    end
    %create a huffman code tree where a codeword is generated for each bin
    codes = num2cell(codebook);
    [tr,tble] = hufftree(codes,probs);
    %find average word length factoring in probabilities as weights
    lsum = 0;
    for t = 1:bins
        lsum = lsum + (length(tble.code(t))*probs(t));
    end
    avglen = lsum/bins;
    %calculate description length
    M = avglen*n*(r + c);
    %compute error between V and GF
    E = 0;
    for i = 1:r
        for j = 1:c
            q = (V(i,j)*log(V(i,j)/GF(i,j)) - V(i,j) + GF(i,j));
            if isnan(q) == 0
               E = E + q; 
            end
        end
    end
    l = M + E;
    L = [L l];
end
%minimum length = optimal number of roles
[min_len, idx] = min(L);
sprintf('Optimal number of roles selected: %d',idx+1)