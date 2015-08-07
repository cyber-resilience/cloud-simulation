function grad_g=grad_compute(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,A,intercept,beta_q,q)
       n=size(A,1); m=size(A,2);
       grad_g=zeros(n,1);
       for j=1:m
         ej=zeros(m,1); ej(j)=1;
         [Lfunc_s Lgrad_s]=Latency_Request(task_th(j),task_critical(j),a,b,c,intercept); % stable 
         [Lfunc Lgrad]=Latency_Request(task(j)-r'*A*ej,task_critical(j),a,b,c,intercept); % controled
         [Lcost Lcost_grad]=latency_cost(Lfunc,Lfunc_s,phi);
         grad_g=grad_g+Lcost_grad*(-Lgrad)*A*ej;
       end
       grad_g= grad_g+lambda*d+beta_q*q;