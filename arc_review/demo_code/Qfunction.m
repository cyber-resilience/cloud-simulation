function Q=Qfunction(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,z,A,L,grad_g,intercept,beta_q,q)
       n=size(A,1); m=size(A,2); Q=0;
       for j=1:m
         ej=zeros(m,1); ej(j)=1;
         [Lfunc_s Lgrad_s]=Latency_Request(task_th(j),task_critical(j),a,b,c,intercept); % stable 
         [Lfunc Lgrad]=Latency_Request(task(j)-r'*A*ej,task_critical(j),a,b,c,intercept); % controled
         [Lcost Lcost_grad]=latency_cost(Lfunc,Lfunc_s,phi);
         Q=Q+Lcost;
       end
       Q=Q+lambda*r'*d+(z-r)'*(grad_g+beta_q*q)+L/2*norm(z-r)^2+beta*sum(abs(z))+beta_q*q'*r;
