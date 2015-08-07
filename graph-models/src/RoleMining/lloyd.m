function [new_part, new_codes] = lloyd(dat, init_part, init_codes)

num_bins = length(init_codes);
new_part = zeros(1,num_bins+1);
new_codes = zeros(1,num_bins);
new_part(1) = init_part(1);
new_part(num_bins+1) = init_part(num_bins+1);

for k = 1:num_bins
   s = 0;
   c = 0;
   for d = 1:length(dat)
       if dat(d) > init_part(k) && dat(d) < init_part(k+1)
           s = s + dat(d);
           c = c + 1;
       end
   end
   new_codes(k) = (s/c);
end

for j = 2:num_bins
    new_part(j) = (new_codes(j-1) + new_codes(j))/2.0;
end
