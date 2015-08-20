clear all; close all; clc;

%% Input Data - Indivisual 
%{
tmp=csvread('plogon20111001.user-host.csv');
% 1st column: host  2nd column: user 3rd column: frequency 
user_id=unique(tmp(:,2));
host_id=unique(tmp(:,1));

U=length(user_id)  % # of users
N=length(host_id)  % # of machines/hosts
%K=  % # of applications

% User-host 
% renumber
edgelist=zeros(size(tmp,1),3); edgelist(:,3)=tmp(:,3); % 1st column: user. 2nd column: host 3rd column: frequency
for i=1:U
    ind=find(tmp(:,2)==user_id(i));
    edgelist(ind,1)=i;
end
for i=1:N
    ind=find(tmp(:,1)==host_id(i));
    edgelist(ind,2)=i;
end    
WC=sparse(zeros(U,N)); % access graph weighted matrix
for k=1:size(edgelist,1)
    WC(edgelist(k,1),edgelist(k,2))=edgelist(k,3);
end
AC=double(WC>0); AC(U,N)=0;  % access graph adjacency matrix
B=AC'*AC; BC=double(B>0);

% Host-App
tmp2=csvread('plogon20111001.host-appl.csv');
% Windows  4624 - 2   An account was successfully logged on
% Windows  528 - 3713    Successful Logon
% Windows  540 - 5    Successful Logon
app_id=[2;5;3713];
host_id2=unique(union(tmp2(:,1),tmp2(:,3)));
%host_id=unique(tmp2(:,1));
K= length(app_id) % # of applications
N2=length(host_id2);
hostapp=tmp2;
 for i=1:N2
     ind=find(tmp2(:,1)==host_id2(i));
     hostapp(ind,1)=i;
     ind=find(tmp2(:,3)==host_id2(i));
     hostapp(ind,3)=i;
 end  
  for i=1:K
      ind=find(tmp2(:,2)==app_id(i));
      hostapp(ind,2)=i;
  end
  % delete failure log in
  ind_del=find(hostapp(:,2)>K);
  hostapp(ind_del,:)=[];
  figure;
  bin_count=hist(hostapp(:,2),1:K); bar(1:K,100*(bin_count)/sum(bin_count)); xlabel('applications'); ylabel('fraction of usage (%)');
A=[];
for k=1:K
    tmpA=0*speye(N2);
    ind=find(hostapp(:,2)==k);
    for i=1:length(ind)
        tmpA(hostapp(ind(i),1),hostapp(ind(i),3))=1;
    end
    A=[A tmpA];
end
  
% random bypartite graph
%[AC WC]=bipartite_random(5,10,0.5,0);
%}

%% Input Data - Tripartite
%
% check consistency
%{
delimiterIN=',';
tmp1=importdata('tripartite\plogon20111001.user-host.csv.keys.csv',delimiterIN);
name1=tmp1.textdata; label1=tmp1.data;
tmp2=importdata('tripartite\plogon20111001.host-appl.csv.keys.csv',delimiterIN); 
name2=tmp2.textdata; label2=tmp2.data;

for i=1:size(name1,1)
    tmp3=strcmp(name1{i},name2);
    ind=find(tmp3==1);
    if(label1(i)~=label2(ind))
        error('name inconsistent')
    end
end

for i=1:size(name2,1)
    tmp3=strcmp(name2{i},name1);
    ind=find(tmp3==1);
    if(label2(i)~=label1(ind))
        error('name inconsistent')
    end
end
%}
 % Extract Common Sets
%tmp=csvread('tripartite\plogon20111001.user-host.csv');
%tmp2=csvread('tripartite\plogon20111001.host-appl.csv');
tmp=csvread('plogon20111001.user-host.csv');
tmp2=csvread('plogon20111001.host-appl.csv');

host_id1=unique(tmp(:,1));
host_id2=unique(union(tmp2(:,1),tmp2(:,3)));
host_id_common=intersect(host_id1,host_id2);

[dummy ia]=setdiff(tmp(:,1),host_id_common);
[dummy ib]=setdiff(tmp2(:,1),host_id_common);
[dummy ic]=setdiff(tmp2(:,3),host_id_common);
tmp(ia,:)=[];
tmp2(union(ib,ic),:)=[];
%

% 1st column: host  2nd column: user 3rd column: frequency 
user_id=unique(tmp(:,2));

U=length(user_id)  % # of users
N=length(host_id_common)  % # of machines/hosts
%K=  % # of applications

% User-host 
% renumber
edgelist=zeros(size(tmp,1),3); edgelist(:,3)=tmp(:,3); % 1st column: user. 2nd column: host 3rd column: frequency
for i=1:U
    ind=find(tmp(:,2)==user_id(i));
    edgelist(ind,1)=i;
end
for i=1:N
    ind=find(tmp(:,1)==host_id_common(i));
    edgelist(ind,2)=i;
end    
WC=sparse(zeros(U,N)); % access graph weighted matrix
for k=1:size(edgelist,1)
    WC(edgelist(k,1),edgelist(k,2))=edgelist(k,3);
end
AC=double(WC>0); AC(U,N)=0;  % access graph adjacency matrix
B=AC'*AC; BC=double(B>0);

% Host-App

% Windows  4624 - 10338   An account was successfully logged on
% Windows  528 - 10345   Successful Logon
% Windows  540 - 10339    Successful Logon
app_id=[10339;10338; 10345];
%host_id2=unique(union(tmp2(:,1),tmp2(:,3)));
%host_id=unique(tmp2(:,1));
K= length(app_id) % # of applications
N2=length(host_id_common);
hostapp=tmp2;
 for i=1:N2
     ind=find(tmp2(:,1)==host_id_common(i));
     hostapp(ind,1)=i;
     ind=find(tmp2(:,3)==host_id_common(i));
     hostapp(ind,3)=i;
 end  
  for i=1:K
      ind=find(tmp2(:,2)==app_id(i));
      hostapp(ind,2)=i;
  end
  % delete failure log in
  ind_del=find(hostapp(:,2)>K);
  hostapp(ind_del,:)=[];
  figure;
  bin_count=hist(hostapp(:,2),1:K); bar(1:K,100*(bin_count)/sum(bin_count)); xlabel('applications'); ylabel('fraction of usage (%)');
A=[];
for k=1:K
    tmpA=0*speye(N2);
    ind=find(hostapp(:,2)==k);
    for i=1:length(ind)
        tmpA(hostapp(ind(i),1),hostapp(ind(i),3))=1;
    end
    A=[A tmpA];
end

if(max(edgelist(:,2))>N|max(max(hostapp(:,1),hostapp(:,3)))>N2)
    error('renumber error')
end

% random bypartite graph
%[AC WC]=bipartite_random(5,10,0.5,0);
%}

%% Segmentation
%{
compromise_ration=0.001
compromise_num=ceil(N*compromise_ration)
num_removed_edges=10
rem_int=1
run=2


topo_ratio_vec=0.1:0.1:1;
%topo_ratio_vec=1;

for h=1:length(topo_ratio_vec)
    h
        for z=1:run     
        z
        topo_ratio=topo_ratio_vec(h);
        r_initial=zeros(N,1); r_initial(randi(N,compromise_num,1))=1;
            if(topo_ratio_vec(h)==1)
                 r_s=cascading_bypartite(B,r_initial);
            else
                MASK=double(sprand(AC)<=topo_ratio);
                AC_new_M=AC.*MASK;
                BC_new=AC_new_M'*AC_new_M;     
                r_s=cascading_bypartite(BC_new,r_initial);
            end
        % initial reachability
       
        reach_ini(z,h)=sum(r_s);
        
        % without recalculation
        [score]=segment_edge_score(AC);
        [score_sort ind_score]=sort(nonzeros(score),'descend');
        for k=rem_int:rem_int:num_removed_edges
            %k
            [row col]=find(score>=score_sort(k));
            edgelist_removed=[row(1:k) col(1:k)];    
            [AC_new edgelist_new num_new_user_no_recal(z,h,k/rem_int)]=user_split(edgelist,edgelist_removed,AC);
            if(topo_ratio_vec(h)==1)
                AC_new_M=AC_new;
            else
                MASK=double(sprand(AC_new)<=topo_ratio);
                AC_new_M=AC_new.*MASK;
            end
            %BC_new=AC_new'*AC_new;            
             BC_new=AC_new_M'*AC_new_M;            
            r_k=cascading_bypartite(BC_new,r_initial);
            reach_no_recal(z,h,k/rem_int)=sum(r_k);
        end
        AC_new_no=AC_new;
        

         % machine first heuristic  
        AC_left=AC; edgelist_new=edgelist;  edgelist_removed=[]; edgelist_left=edgelist; AC_inc=AC;
        for k=rem_int:rem_int:num_removed_edges
            %k
            %{
             if(k==rem_int)  disp('user first');end
            [dummy row]=max(sum(AC_left,2));  
            ind_col=find(AC_left(row,:)>0);
            [dummy col_ind]=max(sum(AC_left(:,ind_col),1));
            col=ind_col(col_ind(1)); row=row(1);
            %}
            %
            if(k==rem_int) disp('mac first'); end
            [dummy col]=max(sum(AC_left,1));            
            ind_row=find(AC_left(:,col)>0);
            [dummy row_ind]=max(sum(AC_left(ind_row,:),2));
            col=col(1); row=ind_row(row_ind(1));
            %
            edgelist_removed_inc=[row col];    
            [AC_left edgelist_left]=user_split_removal(edgelist_left,edgelist_removed_inc,AC_left);            
            
            edgelist_removed=[edgelist_removed; edgelist_removed_inc];    
            num_new_user_heu_mac(z,h,k/rem_int)=length(unique(edgelist_removed(:,1)));
            [AC_new edgelist_new dummy]=user_split(edgelist,edgelist_removed,AC);

            if(topo_ratio_vec(h)==1)
                AC_new_M=AC_new;
            else            
                MASK=double(sprand(AC_new)<=topo_ratio);
                AC_new_M=AC_new.*MASK;
            end
            %BC_new=AC_new'*AC_new;
             BC_new=AC_new_M'*AC_new_M;      
            r_k=cascading_bypartite(BC_new,r_initial);
            reach_heu_mac(z,h,k/rem_int)=sum(r_k);
        end 
        AC_new_heu_mac=AC_new;
        
        % user first heuristic  
        AC_left=AC; edgelist_new=edgelist;  edgelist_removed=[]; edgelist_left=edgelist; AC_inc=AC;
        for k=rem_int:rem_int:num_removed_edges
            %k
            %
             if(k==rem_int)  disp('user first');end
            [dummy row]=max(sum(AC_left,2));  
            ind_col=find(AC_left(row,:)>0);
            [dummy col_ind]=max(sum(AC_left(:,ind_col),1));
            col=ind_col(col_ind(1)); row=row(1);
            %
            %{
            if(k==rem_int) disp('mac first'); end
            [dummy col]=max(sum(AC_left,1));            
            ind_row=find(AC_left(:,col)>0);
            [dummy row_ind]=max(sum(AC_left(ind_row,:),2));
            col=col(1); row=ind_row(row_ind(1));
            %}
            edgelist_removed_inc=[row col];    
            [AC_left edgelist_left]=user_split_removal(edgelist_left,edgelist_removed_inc,AC_left);            
            
            edgelist_removed=[edgelist_removed; edgelist_removed_inc];    
            num_new_user_heu_user(z,h,k/rem_int)=length(unique(edgelist_removed(:,1)));
            [AC_new edgelist_new dummy]=user_split(edgelist,edgelist_removed,AC);

            if(topo_ratio_vec(h)==1)
                AC_new_M=AC_new;
            else            
                MASK=double(sprand(AC_new)<=topo_ratio);
                AC_new_M=AC_new.*MASK;
            end
            %BC_new=AC_new'*AC_new;
             BC_new=AC_new_M'*AC_new_M;      
            r_k=cascading_bypartite(BC_new,r_initial);
            reach_heu_user(z,h,k/rem_int)=sum(r_k);
        end 
        AC_new_heu_user=AC_new;
        
        % with recalculation
        %
        AC_left=AC; edgelist_new=edgelist;  edgelist_removed=[]; edgelist_left=edgelist; AC_inc=AC;
        for k=rem_int:rem_int:num_removed_edges
            %k
            [score]=segment_edge_score(AC_left);
            [score_sort ind_score]=sort(nonzeros(score),'descend');
            [row col]=find(score>=score_sort(rem_int));
            
            edgelist_removed_inc=[row(1:rem_int) col(1:rem_int)];    % incremental removal
            [AC_left edgelist_left]=user_split_removal(edgelist_left,edgelist_removed_inc,AC_left);            
            
            edgelist_removed=[edgelist_removed; edgelist_removed_inc];    
            num_new_user_recal(z,h,k/rem_int)=length(unique(edgelist_removed(:,1)));
            [AC_new edgelist_new dummy]=user_split(edgelist,edgelist_removed,AC);

             if(topo_ratio_vec(h)==1)
                AC_new_M=AC_new;
             else
                MASK=double(sprand(AC_new)<=topo_ratio);
                AC_new_M=AC_new.*MASK;
             end
            %BC_new=AC_new'*AC_new;
             BC_new=AC_new_M'*AC_new_M;      
            r_k=cascading_bypartite(BC_new,r_initial);
            reach_recal(z,h,k/rem_int)=sum(r_k);
        end
end


%{
figure;
subplot 121
d=sum(AC,2); 
[nelements centers]=hist(d,0:max(d));
%bar((nelements/sum(nelements)));
semilogy(centers,nelements/sum(nelements),'o')
subplot 122
d_new=sum(AC_new,2); 
[nelements centers]=hist(d_new,0:max(d_new));
%bar((nelements/sum(nelements)));
semilogy(centers,nelements/sum(nelements),'o')
%}
end 

edge_int=100
ms=10
fs=16
NE=nnz(AC);



if(length(topo_ratio_vec)==1)
    %{
    figure;
    plot(0:rem_int:num_removed_edges,100*[squeeze(mean(reach_ini));squeeze(mean(reach_no_recal))]/N,'bs'); hold on;
    plot(0:rem_int:num_removed_edges,100*[squeeze(mean(reach_ini));squeeze(mean(reach_recal))]/N,'ro'); hold on;
    xlabel('modified edges');ylabel('reachability (%)');
    legend('greedy segmentation w/o recalculation','greedy segmentation w/ recalculation')
        
    figure;
    plot(0:rem_int:num_removed_edges,[0 squeeze(mean(num_new_user_no_recal))'],'bs'); hold on;
    plot(0:rem_int:num_removed_edges,[0 squeeze(mean(num_new_user_recal))'],'ro'); hold on;
    xlabel('modified edges');ylabel('number of newly added users');
    legend('greedy segmentation w/o recalculation','greedy segmentation w/ recalculation')
    %}
    tmp1=squeeze(mean(reach_no_recal));
    tmp2=squeeze(mean(reach_recal));
    tmp5=squeeze(mean(reach_heu_mac));
    tmp7=squeeze(mean(reach_heu_user));
    
        figure;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[squeeze(mean(reach_ini));tmp1(edge_int:edge_int:num_removed_edges)]/N,...
        'bs-','markersize',ms,'linewidth',2,'markerfacecolor','b'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[squeeze(mean(reach_ini));tmp2(edge_int:edge_int:num_removed_edges)]/N,...
        'ro-','markersize',ms,'linewidth',2,'markerfacecolor','r'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[squeeze(mean(reach_ini));tmp5(edge_int:edge_int:num_removed_edges)]/N,...
        'g^-','markersize',ms,'linewidth',2,'markerfacecolor','g'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[squeeze(mean(reach_ini));tmp7(edge_int:edge_int:num_removed_edges)]/N,...
        'md-','markersize',ms,'linewidth',2,'markerfacecolor','m'); hold on;
    xlabel('fraction of segmented edges (%)','fontsize',fs);ylabel('reachability (%)','fontsize',fs);
   legend('greedy segmentation w/o score recalculation','greedy segmentation w/ score recalculation','greedy host first segmentation',...
'greedy user first segmentation','fontsize',fs)
    
    tmp3=squeeze(mean(num_new_user_no_recal))';
    tmp4=squeeze(mean(num_new_user_recal))';
    tmp6=squeeze(mean(num_new_user_heu_mac))';
    tmp8=squeeze(mean(num_new_user_heu_user))';
    

        figure;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[0 tmp3(edge_int:edge_int:num_removed_edges) ]/U,'bs-','markersize',ms,'linewidth',2,'markerfacecolor','b'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[0 tmp4(edge_int:edge_int:num_removed_edges) ]/U,'ro-','markersize',ms,'linewidth',2,'markerfacecolor','r'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[0 tmp6(edge_int:edge_int:num_removed_edges) ]/U,'g^-','markersize',ms,'linewidth',2,'markerfacecolor','g'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*[0 tmp8(edge_int:edge_int:num_removed_edges) ]/U,'md-','markersize',ms,'linewidth',2,'markerfacecolor','m'); hold on;
    xlabel('fraction of segmented edges (%)','fontsize',fs);ylabel('fraction of newly added users (%)','fontsize',fs);
   legend('greedy segmentation w/o score recalculation','greedy segmentation w/ score recalculation','greedy host first segmentation',...
'greedy user first segmentation','fontsize',fs)

efficiency_no_recal=1./((1+[squeeze(mean(reach_ini));1+tmp1(edge_int:edge_int:num_removed_edges)]/N)'.*(1+[0 tmp3(edge_int:edge_int:num_removed_edges) ]/U));
efficiency_recal=1./((1+[squeeze(mean(reach_ini));1+tmp2(edge_int:edge_int:num_removed_edges)]/N)'.*(1+[0 tmp4(edge_int:edge_int:num_removed_edges) ]/U));
efficiency_heu_mac=1./((1+[squeeze(mean(reach_ini));1+tmp5(edge_int:edge_int:num_removed_edges)]/N)'.*(1+[0 tmp6(edge_int:edge_int:num_removed_edges) ]/U));
efficiency_heu_user=1./((1+[squeeze(mean(reach_ini));1+tmp7(edge_int:edge_int:num_removed_edges)]/N)'.*(1+[0 tmp8(edge_int:edge_int:num_removed_edges) ]/U));
    figure;
    
    plot(100*[0:edge_int:num_removed_edges]/NE,100*efficiency_no_recal,'bs-','markersize',ms,'linewidth',2,'markerfacecolor','b'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*efficiency_recal,'ro-','markersize',ms,'linewidth',2,'markerfacecolor','r'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*efficiency_heu_mac,'g^-','markersize',ms,'linewidth',2,'markerfacecolor','g'); hold on;
    plot(100*[0:edge_int:num_removed_edges]/NE,100*efficiency_heu_user,'md-','markersize',ms,'linewidth',2,'markerfacecolor','m'); hold on;
   xlabel('fraction of segmented edges (%)','fontsize',fs);ylabel('efficiency (%)','fontsize',fs);
   legend('greedy segmentation w/o score recalculation','greedy segmentation w/ score recalculation','greedy host first segmentation',...
'greedy user first segmentation','fontsize',fs)
else
    figure;
    imagesc(0:rem_int:num_removed_edges,topo_ratio_vec,100*[squeeze(mean(reach_ini));squeeze(mean(reach_no_recal))']/N)
    figure;
    imagesc(0:rem_int:num_removed_edges,topo_ratio_vec,100*[squeeze(mean(reach_ini));squeeze(mean(reach_recal))']/N)


    figure;
    imagesc(100*topo_ratio_vec,100*[0:rem_int:num_removed_edges]/NE,...
        100*[squeeze(mean(reach_ini));squeeze(mean(reach_no_recal(:,:,edge_int:edge_int:num_removed_edges)))']/N)
       ylabel('fraction of segmented edges (%)','fontsize',fs);xlabel('fraction of known accesses (%)','fontsize',fs); colorbar;
    
end

%}
%% Edge Hardening
%{
%den_vec=0.01:0.01:0.1;
den_vec=0.1;

%P=zeros(K,N2);
%P=0.001*rand(K,N2);
%P=[0.0001 0.001 0.001]'*ones(1,N2);
%P=ones(K,N2);

    compromise_ratio=0.001
    compromise_num=ceil(N2*compromise_ratio)
    num_modified_edges=10
    rem_int=1
    run=2

for h=1:length(den_vec)
    h
    sample_den=den_vec(h);
    for z=1:run            
        z

        P=sprand(K,N2,sample_den);

        J=(kron(P,ones(N2,1)))'*A';
        %d=sum(A');

        E=10^-5*ones(size(P)).*spones(P);
        %E=0*speye(size(P));

            r_initial=zeros(N2,1); r_initial(randi(N2,compromise_num,1))=1;        
            % hardening level
                a=rand(N2,1);
                %a=0.5*ones(N2,1);
                %a=1-sum(P)'; a(find(a<0))=0;
            % initial reachability
                r_s=cascading_prob(A,P,a,r_initial);
                reach_ini(z)=sum(r_s);
                score=hardening_edge_score(P,A,E);
                [score_sort ind_score]=sort(nonzeros(score),'descend');
            % without recalculation            
            Pnew=P;
            for k=rem_int:rem_int:num_modified_edges
                %k
                [row col]=find(score>=score_sort(k));
                %edgelist_harden_inc=[row(k) col(k)];                          
                %[Pnew anew]=mac_harden(edgelist_harden_inc,Pnew,E,a);  
                edgelist_harden=[row(1:k) col(1:k)];            
                [Pnew anew]=mac_harden(edgelist_harden,P,E,a);  
                r_k=cascading_prob(A,Pnew,anew,r_initial);
                reach_no_recal(z,h,k/rem_int)=sum(r_k);
            end
            %
            % with recalculation
             Pnew=P;
            for k=rem_int:rem_int:num_modified_edges
                score=hardening_edge_score(Pnew,A,E);
                [score_sort ind_score]=sort(nonzeros(score),'descend');
                [row col]=find(score>=score_sort(1));
                edgelist_harden_inc=[row(1) col(1)];                          
                [Pnew anew]=mac_harden(edgelist_harden_inc,Pnew,E,a);  
                r_k=cascading_prob(A,Pnew,anew,r_initial);
                reach_recal(z,h,k/rem_int)=sum(r_k);
            end
            %
            % degree heuristic 
            Pnew=P;
            for k=rem_int:rem_int:num_modified_edges
                %[score_sort ind_score]=sort(nonzeros(Pnew),'descend');
                [row col]=find(Pnew>=max(nonzeros(Pnew)));
                edgelist_harden_inc=[row(1) col(1)];                         
                [Pnew anew]=mac_harden(edgelist_harden_inc,Pnew,E,a);  
                r_k=cascading_prob(A,Pnew,anew,r_initial);
                reach_heu(z,h,k/rem_int)=sum(r_k);
            end
    end
end
edge_int=50
ms=10
fs=16


if(length(den_vec)==1)
     figure;
    plot(100*[0:edge_int:num_modified_edges]/(den_vec*K*N2),100*[squeeze(mean(reach_ini)) squeeze(mean(reach_no_recal(:,edge_int:edge_int:num_modified_edges)))]/N2,...
        'bs-','markersize',ms,'linewidth',2,'markerfacecolor','b'); hold on;
    plot(100*[0:edge_int:num_modified_edges]/((den_vec*K*N2)),100*[squeeze(mean(reach_ini)) squeeze(mean(reach_recal(:,edge_int:edge_int:num_modified_edges)))]/N2,...
        'ro-','markersize',ms,'linewidth',2,'markerfacecolor','r'); hold on;
    plot(100*[0:edge_int:num_modified_edges]/((den_vec*K*N2)),100*[squeeze(mean(reach_ini)) squeeze(mean(reach_heu(:,edge_int:edge_int:num_modified_edges)))]/N2,...
        'g^-','markersize',ms,'linewidth',2,'markerfacecolor','g'); hold on;
    xlabel('fraction of hardened edges (%)','fontsize',fs);ylabel('reachability (%)','fontsize',fs);
    legend('greedy edge hardening w/o score recalculation','greedy edge hardening w/ recalculation','greedy heuristic-P','fontsize',fs)
else
    figure;
    imagesc(denvec,100*[0:edge_int:num_modified_edges]./((den_vec*K*N2)),...
        100*[squeeze(mean(reach_ini)) squeeze(mean(reach_no_recal(:,edge_int:edge_int:num_modified_edges)))]/N2)
end
%}

%% Node Hardening
%{
%den_vec=0.01:0.01:0.1;
den_vec=0.2;


    compromise_ratio=0.001
    compromise_num=ceil(N2*compromise_ratio)
    num_modified_nodes=10
    rem_int=1
    run=2

for h=1:length(den_vec)
    h
    sample_den=den_vec(h);
    for z=1:run            
        z

        P=sprand(K,N2,sample_den);

        J=(kron(P,ones(N2,1)))'*A';
        %d=sum(A');

        E=10^-5*ones(size(P)).*spones(P);
        %E=0*speye(size(P));

            r_initial=zeros(N2,1); r_initial(randi(N2,compromise_num,1))=1;        
            % hardening level
                a=rand(N2,1);
                %a=0.5*ones(N2,1);
                %a=1-sum(P)'; a(find(a<0))=0;
            % initial reachability
                r_s=cascading_prob(A,P,a,r_initial);
                reach_ini(z)=sum(r_s);
                score=hardening_edge_score(P,A,E);
                score_node=sum(score,1);
            % without recalculation            
            Pnew=P;
            for k=rem_int:rem_int:num_modified_nodes
                %k
                [anew]=node_harden(score_node,a,k);
                r_k=cascading_prob(A,Pnew,anew,r_initial);
                reach_no_recal(z,h,k/rem_int)=sum(r_k);
            end
            %
            % degree hearistic J
             Pnew=P; anew=a;
            score_node=sum(J,2);
            for k=rem_int:rem_int:num_modified_nodes          
                [anew]=node_harden(score_node,a,k);
                r_k=cascading_prob(A,Pnew,anew,r_initial);
                reach_recal(z,h,k/rem_int)=sum(r_k);         
            end
            %
            % degree heuristic 
            Pnew=P;
            score_node=a;
            for k=rem_int:rem_int:num_modified_nodes                
                [anew]=node_harden(score_node,a,k);
                r_k=cascading_prob(A,Pnew,anew,r_initial);
                reach_heu(z,h,k/rem_int)=sum(r_k);
            end
            %
    end
end
edge_int=50
ms=10
fs=16


if(length(den_vec)==1)
     figure;
    plot(100*[0:edge_int:num_modified_nodes]/N2,100*[squeeze(mean(reach_ini)) squeeze(mean(reach_no_recal(:,edge_int:edge_int:num_modified_nodes)))]/N2,...
        'bs-','markersize',ms,'linewidth',2,'markerfacecolor','b'); hold on;
    plot(100*[0:edge_int:num_modified_nodes]/N2,100*[squeeze(mean(reach_ini)) squeeze(mean(reach_recal(:,edge_int:edge_int:num_modified_nodes)))]/N2,...
        'ro-','markersize',ms,'linewidth',2,'markerfacecolor','r'); hold on;
    plot(100*[0:edge_int:num_modified_nodes]/N2,100*[squeeze(mean(reach_ini)) squeeze(mean(reach_heu(:,edge_int:edge_int:num_modified_nodes)))]/N2,...
        'g^-','markersize',ms,'linewidth',2,'markerfacecolor','g'); hold on;
    xlabel('fraction of hardened nodes (%)','fontsize',fs);ylabel('reachability (%)','fontsize',fs);
    legend('greedy node score hardening','greedy heuristic-J','greedy heuristic-a','fontsize',fs)
else
    figure;
    imagesc(denvec,100*[0:edge_int:num_modified_edges]./nnz(A),...
        100*[squeeze(mean(reach_ini)) squeeze(mean(reach_no_recal(:,edge_int:edge_int:num_modified_edges)))]/N2)
end
%}

%% Segmentation+Edge Hardening+Node Hardening
%

compromise_ration=0.001
compromise_num=ceil(N*compromise_ration)
num_removed_edges=2
num_modified_nodes=2
num_modified_edges=2
rem_int=1
run=2
sample_den=0.1
topo_ratio=1

% Seg w/0 recal + Edge w0 recal + Node Harden

choice_seg=1
% 1: segmentation w/o recal 
% 2: segmentation w recal 
% 3: segmentation user 
% 4: segmentation host
choice_edge=1
% 1: edge harden w/o recal 
% 2: edge harden w recal 

choice_node=1
% 1: node harden w/o recal 
% 2: node harden deg 

%% segmentation score that can be precomputed
 if(choice_seg==1)                  
           [score_seg]=segment_edge_score(AC);
           [score_sort_seg ind_score]=sort(nonzeros(score_seg),'descend');
 end



for z=1:run
    z
                P=sprand(K,N2,sample_den);
                J=(kron(P,ones(N2,1)))'*A';
                E=10^-5*ones(size(P)).*spones(P);                
                r_initial=zeros(N,1); r_initial(randi(N,compromise_num,1))=1;
                % hardening level
                a=rand(N2,1);
 %% edge harden score that can be precomputed               
                      if(choice_edge==1)
                            score_edge=hardening_edge_score(P,A,E);
                            [score_sort_edge ind_score]=sort(nonzeros(score_edge),'descend');
                      end
%% node harden score that can be precomputed
                    if(choice_node==1)
                        score_node_harden=hardening_edge_score(P,A,E);
                        score_node=sum(score_node_harden,1);
                    end
   
           
% Initialization
  AC_left=AC; edgelist_new=edgelist;  edgelist_removed=[]; edgelist_left=edgelist; AC_inc=AC; 
    for i=0:num_removed_edges  % segmentation
           %% Segmentation
                 % without recalculation
                 if(i==0)
                     AC_new=AC;
                 else
                    if(choice_seg==1)                  
                            k=i;
                           %[score]=segment_edge_score(AC);
                            %[score_sort ind_score]=sort(nonzeros(score),'descend');
                                [row col]=find(score_seg>=score_sort_seg(k));
                                edgelist_removed=[row(1:k) col(1:k)];    
                                [AC_new edgelist_new dummy]=user_split(edgelist,edgelist_removed,AC);            
                    end

                     % with recalculation
                     if(choice_seg==2)
                              k=i;
                             %AC_left=AC; edgelist_new=edgelist;  edgelist_removed=[]; edgelist_left=edgelist; AC_inc=AC;
                            [score]=segment_edge_score(AC_left);
                            [score_sort ind_score]=sort(nonzeros(score),'descend');
                            [row col]=find(score>=score_sort(rem_int));

                            edgelist_removed_inc=[row(1:rem_int) col(1:rem_int)];    % incremental removal
                            [AC_left edgelist_left]=user_split_removal(edgelist_left,edgelist_removed_inc,AC_left);            

                            edgelist_removed=[edgelist_removed; edgelist_removed_inc];    
                            [AC_new edgelist_new dummy]=user_split(edgelist,edgelist_removed,AC);  
                     end

                     % user first heuristic
                     if(choice_seg==3) 
                                k=i;
                                %AC_left=AC; edgelist_new=edgelist;  edgelist_removed=[]; edgelist_left=edgelist; AC_inc=AC;
                                     if(k==rem_int)  disp('user first');end
                                    [dummy row]=max(sum(AC_left,2));  
                                    ind_col=find(AC_left(row,:)>0);
                                    [dummy col_ind]=max(sum(AC_left(:,ind_col),1));
                                    col=ind_col(col_ind(1)); row=row(1);                          
                                    edgelist_removed_inc=[row col];    
                                    [AC_left edgelist_left]=user_split_removal(edgelist_left,edgelist_removed_inc,AC_left);            

                                    edgelist_removed=[edgelist_removed; edgelist_removed_inc];    
                                    [AC_new edgelist_new dummy]=user_split(edgelist,edgelist_removed,AC);    
                      end 
                      % machine first heuristic  
                      if(choice_seg==4)
                          k=i;
                          %AC_left=AC; edgelist_new=edgelist;  edgelist_removed=[]; edgelist_left=edgelist; AC_inc=AC;

                            if(k==rem_int) disp('mac first'); end
                            [dummy col]=max(sum(AC_left,1));            
                            ind_row=find(AC_left(:,col)>0);
                            [dummy row_ind]=max(sum(AC_left(ind_row,:),2));
                            col=col(1); row=ind_row(row_ind(1));
                            edgelist_removed_inc=[row col];    
                            [AC_left edgelist_left]=user_split_removal(edgelist_left,edgelist_removed_inc,AC_left);            

                            edgelist_removed=[edgelist_removed; edgelist_removed_inc];    
                            [AC_new edgelist_new dummy]=user_split(edgelist,edgelist_removed,AC);
                      end
                 end     
                                 if(topo_ratio==1)
                                    AC_new_M=AC_new;
                                else            
                                    MASK=double(sprand(AC_new)<=topo_ratio);
                                    AC_new_M=AC_new.*MASK;
                                end
                                 BC_new=AC_new_M'*AC_new_M;  
         % initialization
         Pnew=P;
        for j=0:num_modified_edges % edge harden
            
              %%   Edge Harden
                % without recalculation   
                if(j==0)
                    Pnew=P;
                    anew=a;
                else
                    if(choice_edge==1)
                        k=j;
                        %score=hardening_edge_score(P,A,E);
                        %[score_sort ind_score]=sort(nonzeros(score),'descend');
                        [row col]=find(score_edge>=score_sort_edge(k));
                        edgelist_harden=[row(1:k) col(1:k)];            
                        [Pnew dummy]=mac_harden(edgelist_harden,P,E,a);  
                    end
                    % with recalculation
                    if(choice_edge==2)
                        k=j;
                        score=hardening_edge_score(Pnew,A,E);
                        [score_sort ind_score]=sort(nonzeros(score),'descend');
                        [row col]=find(score>=score_sort(1));
                        edgelist_harden_inc=[row(1) col(1)];                          
                        [Pnew dummy]=mac_harden(edgelist_harden_inc,Pnew,E,a);  
                    end
                end
            % initialization
             anew=a;
            for s=0:num_modified_nodes % node harden                           
                %% Node Harden
                if(s==0)
                    anew=a;
                else
                    % w/o recal
                    if(choice_node==1)
                        k=s;
                        %score=hardening_edge_score(P,A,E);
                        %score_node=sum(score,1);
                        [anew]=node_harden(score_node,a,k);                    
                    end

                    % degree hearistic J
                    if(choice_node==2)
                        k=s;
                        score_node=sum(J,2); 
                        [anew]=node_harden(score_node,a,k);    
                    end
                end                             
                %% Reachability
                 r_s=cascading_tripartite(A,Pnew,BC_new,anew,r_initial);
                 reach(z,i+1,j+1,s+1)=sum(r_s);          
            end
        end
    end
end


[X Y Z]=meshgrid(0:num_removed_edges,0:num_modified_edges,0:num_modified_nodes);
C=squeeze(mean(reach))/N; [a1 a2 a3]=size(C); m=a1*a2*a3;
figure;
scatter3(reshape(X,m,1),reshape(Y,m,1),reshape(Z,m,1),100,reshape(C,m,1),'fill'); colorbar;

    


%}


