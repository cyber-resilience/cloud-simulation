 clear all; close all; clc

%%

enable_plot=0

%filename_test='2_min_normal.out'; %  current application graph
filename_test='2_min.out'; %  current application graph
filename_steady='10_min.out'; %  Steady State application Graph

user_name={'dev1','dev2','ceo','sales'}
server_name={'web1','web2'}

% web1 web2: server   
% db1 db2: data base
% ceo dev1 dev2 sales : user 
% ingest: data collecting machine 

%% Load hosting file
%filename_host='host_20150707.txt'
%delimiterIn=','; headerlinesIn=1;
%data_host=importdata(filename_host,delimiterIn);
load host20150707;data_host=host20150707;
ip_ID=cell2mat(data_host(:,1));

ind_user=[];
ind_server=[];
for i=1:length(user_name)
    tmp=strcmp(data_host(:,2),user_name(i));
    ind_user=[ind_user find(tmp==1)];
end
for i=1:length(server_name)
    tmp=strcmp(data_host(:,2),server_name(i));
    ind_server=[ind_server find(tmp==1)];
end

ind_user
ind_server
n_user=length(ind_user)
n_server=length(ind_server)


% dummy IP
%dummy_mac1=172031001007;
%dummy_mac2=172031000002;

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
fs=18;

%% Latency-request fucntion
%{
% 3 attacking 9 
ind=find((data_steady(:,3)==3)&(data_steady(:,4)==9));
data_tmp=data_steady(ind,:);
data_tmp(:,1)=data_tmp(:,1)-data_tmp(1,1);

time_end=data_tmp(end,1)+data_tmp(end,2);


time_interval=1;  % time interval 

figure;
plot(data_tmp(:,1),data_tmp(:,2),'.')

%figure;
%semilogy(data_tmp(:,1),data_tmp(:,2))
m=size(data_tmp,1);
[num_request time_centers]=hist(data_tmp(:,1),linspace(0,time_end,m));
duration=data_tmp(:,2);
%[duration duration_centers]=hist(data_tmp(:,2),linspace(0,max(data_tmp(:,2)),length(0:time_interval:time_end)));
figure;
subplot 311
bar(linspace(0,time_end,m),num_request)
xlabel('time'); ylabel('# of requests')
cum_request=cumsum(num_request);
subplot 312
bar(linspace(0,time_end,m),cum_request)
xlabel('time'); ylabel('cumulated # of requests')
subplot 313
plot(cum_request,duration,'.')
xlabel('# of requests'); ylabel('duration')
% latency
Pkt_median=median([data_tmp(:,7) data_tmp(:,8)],2); % median # packets
Byte_median=median([data_tmp(:,5) data_tmp(:,6) ],2); % median bytes
Latency=duration./(num_request'.*Pkt_median.*Byte_median);
Latency(find(isnan(Latency)==1))=0;

window_end=800
figure;
plot(cum_request(1:window_end),duration(1:window_end),'.')
xlabel('# of requests'); ylabel('duration')


figure;
plot(cum_request(1:window_end),Latency(1:window_end),'.')
xlabel('# of requests'); ylabel('latency')
%for i=0:time_interval:time_end
%    num_flow()=
%end
%}

load attack_20150712
tmp=attack_20150712;
% time coversion
start_time=floor(tmp(:,2))+10^-6*(tmp(:,2)-floor(tmp(:,2)));  
start_time=start_time-start_time(1);
duration=tmp(:,4);
%figure;
%plot(start_time,duration)
%xlabel('time','FontSize',fs); ylabel('duration','FontSize',fs)

% 1: flow tag
%2 :Start Time
%3 :Last Recived Packet	Time
%4 :Duration	
% 5 SIP	
% 6 DIP	
% 7 SBY	
% 8 DBY	
% 9 SPK	
% 10 DPK	
% 11 SPT	
% 12 DPT	
% 13 Excel Start Time

flow_tag=unique(tmp(:,1));
for i=1:length(flow_tag)
    ind=find(tmp(:,1)==flow_tag(i));
    
    duration_nan=duration(find(isnan(duration(ind))==0));
    qq=tmp(ind,8);
    des_byte_nan=qq(find(isnan(qq)==0));
    qq=tmp(ind,10);
    des_pkt_nan=qq(find(isnan(qq)==0));
     % mean
    %{
    duration_median(i)=mean(duration_nan);
    des_byte_median(i)=mean(des_byte_nan);
    des_pkt_median(i)=mean(des_pkt_nan);
    %}
    % median
    %
    duration_median(i)=median(duration_nan);
    des_byte_median(i)=median(des_byte_nan);
    des_pkt_median(i)=median(des_pkt_nan);
    %}
end
latency=duration_median./(des_byte_median.*des_pkt_median);

%figure;
%plot(flow_tag,duration_median,'o-')
%xlabel('# of requests','FontSize',fs); ylabel('duration','FontSize',fs)

if(enable_plot)
figure;
plot(flow_tag,latency,'o-'); hold on
xlabel('# of requests','FontSize',fs); ylabel('latency','FontSize',fs)
end
%}
%% Latency-Request Function Set up

b=1.4
c=10^-8
phi=2
intercept=latency(1)
knee_point=2500
a=mean((latency(2:find(flow_tag==2500))-latency(1:find(flow_tag==2500)-1))/(flow_tag(2)-flow_tag(1)))

for i=1:length(flow_tag)
    [Lfit(i) dummy]=Latency_Request(flow_tag(i),knee_point,a,b,c,intercept);
end

if(enable_plot)
plot(flow_tag(1:find(flow_tag==3000)),Lfit(1:find(flow_tag==3000)),'s-'); hold on
end
run=10

eta=2;penalty_exp_loss=0;stop_criterion=10^-5; penalty_loss_connection=0;
penalty_sparsity=10^-5  % \alpha in the paper
beta_q=10^-5                    % beta in the paper
q=ones(n_user,1)       % node priority

task_critical=knee_point*ones(n_server,1);  % critical task/request



%% Load Test Statistics
[Atest Ltest data_test]=load_AWS_data_V2(filename_test,ip_ID,n_user,n_server,ind_user,ind_server);
if(data_test==0)
    h = figure; 
    if(~enable_plot)
        set(h, 'Visible', 'off'); 
    end
    subplot 211
    ind11=find(max(data_test(:,1))-120<=data_test(:,1)&data_test(:,1)<=max(data_test(:,1)));
    plot(0:120,0*(0:120),'-')
    axis([0,120,0,10])
    xlabel('time (secs)','FontSize',fs);ylabel('latency','FontSize',fs);title('2-min window','FontSize',fs)

else
%ind=find(data_test(:,4)==9);
ind=1:size(data_test,1);
duration_test=data_test(ind,2);
dst_byte=data_test(ind,6);
dst_pkt=data_test(ind,8);
Latency_test=duration_test./(dst_byte.*dst_pkt);
h = figure; 
if(~enable_plot)
  set(h, 'Visible', 'off'); 
end
subplot 211
ind11=find(max(data_test(:,1))-120<=data_test(:,1)&data_test(:,1)<=max(data_test(:,1)));
plot(data_test(ind11,1)-min(data_test(ind11,1)),Latency_test(ind11),'o')
axis([0,120,0,10])
%plot(data_test(ind,1),duration_test,'o')
xlabel('time (secs)','FontSize',fs);ylabel('latency','FontSize',fs);title('2-min window','FontSize',fs)

%Lavg_test=mean(Ltest,1)';
Lavg_test=max(Ltest)'+intercept;
%Lavg_test=[1 1]';
%Lavg_test=[max(Latency_test) max(Latency_test)]';
% A(i,j) # of flow between user i and server j 
% L(i,j) median latency between user i and server j 
% Lavg_test(j) average median latency of an user to server (j)
end
%% Load Steady State Statistics
[Asteady Lsteady data_steady]=load_AWS_data(filename_steady,ip_ID,n_user,n_server,ind_user,ind_server);
%Lavg_steady=mean(Lsteady,1)';
if(data_steady==0)
    subplot 212
    plot([0:600],0*[0:600],'-')
    axis([0,600,0,10])
%end
%plot(data_steady(ind,1),duration_steady,'o')
xlabel('time (secs)','FontSize',fs);ylabel('latency','FontSize',fs);title('10-min window','FontSize',fs)
 saveas(h,'latency_window.png');
else
Lavg_steady=max(Lsteady)'+intercept;
%ind=find(data_steady(:,4)==9);
ind=1:size(data_steady,1);
duration_steady=data_steady(ind,2);
dst_byte=data_steady(ind,6);
dst_pkt=data_steady(ind,8);
Latency_steady=duration_steady./(dst_byte.*dst_pkt);

%if(enable_plot)
subplot 212
plot(data_steady(ind,1),Latency_steady,'o')
axis([0,600,0,10])
%end
%plot(data_steady(ind,1),duration_steady,'o')
xlabel('time (secs)','FontSize',fs);ylabel('latency','FontSize',fs);title('10-min window','FontSize',fs)
 saveas(h,'latency_window.png');
end
%% Steady state inference
if((size(data_test,2)==1)|(size(data_steady,2)==1))
    disp('no data in 2-min or 10-min window')
else
[task_steady]=latency2request(Lavg_steady,a,b,c,intercept,task_critical)  % steady state latency per server

%% Test State inference
[task_test]=latency2request(Lavg_test,a,b,c,intercept,task_critical)  % steady state latency per server

%% Action Recommendation

A=Atest;
for k=1:run
     [r_FISTA_BT(:,k) iteration_FISTA_BT(k)]=user_removal_FISTA_BackTracking_0612(A,penalty_loss_connection,penalty_sparsity,...
         penalty_exp_loss,stop_criterion,task_test,task_steady,eta,a,b,c,phi,task_critical,intercept,beta_q,q);
    %[r_ISTA_BT(:,k) iteration_ISTA_BT(k)]=user_removal_ISTA_BackTracking_0612(A,penalty_loss_connection,penalty_sparsity,...
       % penalty_exp_loss,stop_criterion,task_test,task_steady,eta,a,b,c,phi,task_critical,intercept,beta_q,q);   
end

r_FISTA_BT_avg=mean(r_FISTA_BT,2);  iteration_FISTA_BT_avg=mean(iteration_FISTA_BT)
%r_ISTA_BT_avg=mean(r_ISTA_BT,2); iteration_ISTA_BT_avg=mean(iteration_ISTA_BT)

[FISTA_BT_sort rank_FISTA_BT]=sort(r_FISTA_BT_avg,'descend');
%[ISTA_BT_sort rank_ISTA_BT]=sort(r_ISTA_BT_avg,'descend');

T_FISTA=table(FISTA_BT_sort,'Rownames',user_name(rank_FISTA_BT))
%T_ISTA=table(ISTA_BT_sort,'Rownames',user_name(rank_ISTA_BT))
end

exit
