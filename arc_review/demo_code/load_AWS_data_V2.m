function [A L data_ext]=load_AWS_data_V2(filename,ip_ID,n_user,n_server,ind_user,ind_server)

delimiterIn=',';
headerlinesIn=1;
data_tmp=importdata(filename,delimiterIn);

if(size(data_tmp,1)==0)
    data_ext=0;
    A=zeros(n_user,n_server);
    L=zeros(n_user,n_server);
else   
src_ip=data_tmp(:,3); dst_ip=data_tmp(:,4);
for i=1:length(ip_ID)
    src_ip(find(src_ip==ip_ID(i)))=i;
    dst_ip(find(dst_ip==ip_ID(i)))=i;
end

% clean dummy IP (machines for keeping records)  and nan value
ind1=find(src_ip>length(ip_ID));
ind2=find(dst_ip>length(ip_ID));
ind_nan=[];

% make nan dst bytes & dst pkt 1
    tmp=find(isnan(data_tmp(:,6))==1);    data_tmp(tmp,6)=1;
    tmp=find(isnan(data_tmp(:,8))==1);    data_tmp(tmp,8)=1;

for j=1:size(data_tmp,2)
    tmp=find(isnan(data_tmp(:,j))==1);
    if(nnz(tmp)>0)
        ind_nan=[ind_nan;tmp];
    end
end
ind_dummy=union(ind1,ind2);
ind_dummy=union(ind_nan,ind_dummy);
%

 data_tmp_clean=data_tmp(setdiff(1:size(data_tmp,1),ind_dummy),:);
 src_ip_clean=src_ip(setdiff(1:size(data_tmp,1),ind_dummy));
 dst_ip_clean=dst_ip(setdiff(1:size(data_tmp,1),ind_dummy));


 
 data_ext=data_tmp_clean;
data_ext(:,3:4)=[src_ip_clean dst_ip_clean];

% convert time format to second
data_ext(:,1)=floor(data_ext(:,1))+10^-6*(data_ext(:,1)-floor(data_ext(:,1)));  
data_ext(:,1)=data_ext(:,1)-data_ext(1,1); % starting at time 0
data_ext(:,2)=floor(data_ext(:,2))+10^-6*(data_ext(:,2)-floor(data_ext(:,2)));  

% extract data associated with user and server 
m=size(data_ext,1);

    for i=1:n_user
        %i
        for j=1:n_server
            %j
            %{
            ind1=find((data_ext(:,3)==ind_user(i))&(data_ext(:,4)==ind_server(j)));
            ind2=find((data_ext(:,4)==ind_user(i))&(data_ext(:,3)==ind_server(j)));
            A(i,j)=nnz(ind1)+nnz(ind2); % number of flows (back and forth counts twice)
            D=([data_ext(ind1,2);data_ext(ind2,2) ]); % median duration of the flows
            Pkt=([data_ext(ind1,7);data_ext(ind2,8) ]); % median packets
            B=([data_ext(ind1,5);data_ext(ind2,6) ]); % median bytes
            %}
            ind1=find((data_ext(:,3)==ind_user(i))&(data_ext(:,4)==ind_server(j)));
            A(i,j)=nnz(ind1); % number of flows (back and forth counts twice)
            D=([data_ext(ind1,2)]); % median duration of the flows
            Pkt=([data_ext(ind1,7) ]); % median packets
            B=([data_ext(ind1,5)]); % median bytes            
            % compute latency =  duration / ( # flow * packet * bytes )
            tmp=D./(Pkt.*B);
            if((length(tmp)==0))
                L(i,j)=0;
            elseif(isnan(tmp))
                L(i,j)=0;
            else
                %L(i,j)=median(tmp);  % latency   note that nan may appear
                L(i,j)=max(tmp);  % latency   note that nan may appear
            end
        end
    end

    
    % Time format x.y =  x secs + y micro second
% 1:Last time # 3
% 2:duration # 4
% 3:src ip # 8
% 4:desip # 9
% 5:sec bytes # 11
% 6:dst bytes # 12
% 7:src pkt # 15
% 8:dst pkt # 16
% 9:src port # 19
% 10:dst port # 20
    
    % server average latency 
           %Lavg=sum(D./(A.*Pkt.*B),1)';
           %Lavg(find(isnan(Lavg)==1))=0;

end
