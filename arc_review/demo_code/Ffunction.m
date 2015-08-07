function [F]=Ffunction(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,A,intercept,beta_q,q)
n=size(A,1); m=size(A,2);  F=0;
       for j=1:m
         ej=zeros(m,1); ej(j)=1;
         [Lfunc_s Lgrad_s]=Latency_Request(task_th(j),task_critical(j),a,b,c,intercept); % stable 
         [Lfunc Lgrad]=Latency_Request(task(j)-r'*A*ej,task_critical(j),a,b,c,intercept); % controled
         [Lcost Lcost_grad]=latency_cost(Lfunc,Lfunc_s,phi);
         F=F+Lcost;
       end
       F=F+lambda*r'*d+beta*sum(abs(r))+beta_q*q'*r;


