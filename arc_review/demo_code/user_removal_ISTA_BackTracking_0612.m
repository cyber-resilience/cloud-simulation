function [r k]=user_removal_ISTA_BackTracking_0612(A,lambda,beta,gamma,epsilon,task,task_th,eta,a,b,c,phi,task_critical,intercept,beta_q,q)
% task threshold: stable statistic

n=size(A,1); m=size(A,2);
x=rand(n,1); flag=1; d=A*ones(m,1);
Kmax=10^3; k=0; L0=2;
tmp=0;
while(flag)
        x_old=x;
         
      % Backtracking
      ite=0; L=L0;

      % gadiemt at x_old
      r=x_old;
      grad_g=grad_compute(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,A,intercept,beta_q,q);    
       %
       tmp_x=x_old-1/L* grad_g; % gradient step
       tmp_x_s=soft_treshold(tmp_x,1/L,beta); % treshold
       % F
        r=tmp_x_s;
        F=Ffunction(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,A,intercept,beta_q,q);
       % Q(z,r)       
        r=x_old;  z=tmp_x_s;
       Q=Qfunction(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,z,A,L,grad_g,intercept,beta_q,q);
       
      if(F<=Q)
          flag_2=0;
      else
          flag_2=1;
         while(flag_2)
             ite=ite+1;
             L=eta^ite*L0;
                   % gadiemt at x_old
                  r=x_old;
                  grad_g=grad_compute(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,A,intercept,beta_q,q);    
                   %
                   tmp_x=x_old-1/L* grad_g; % gradient step
                   tmp_x_s=soft_treshold(tmp_x,1/L,beta); % treshold
                   % F
                    r=tmp_x_s;
                    [F]=Ffunction(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,A,intercept,beta_q,q);
                   % Q(z,r)       
                    r=x_old;  z=tmp_x_s;
                  Q=Qfunction(task,task_th,task_critical,a,b,c,phi,lambda,beta,d,r,z,A,L,grad_g,intercept,beta_q,q);
                 if(F<=Q)     flag_2=0;     end
          end
      end
                      
    % soft threshold for tmp_x    
         tmp_x=x_old-1/L* grad_g; % gradient step
       tmp_x_s=soft_treshold(tmp_x,1/L,beta); % treshold
    
    % projection to convex set    
    if(nnz(tmp_x_s)==0)
        x=zeros(n,1);
    else
        x=tmp_x_s/max(abs(tmp_x_s)); x(find(x>1))=1;  x(find(x<0))=0;
    end    
    tmp_pre=tmp;
    tmp=norm(x-x_old); 
    % stop criterion
    if(tmp<=epsilon)  flag=0; end
    
    k=k+1;     
    if(k==Kmax)  
        if(abs(tmp-tmp_pre)<epsilon)
            disp('alternating')
            flag=0;  
            flag_alternating=1;
        else
             disp('not converge'); 
             flag_alternating=1;
             flag=0;
            %{
             x=rand(n,1); 
             k=0;
             flag_alternating=0;
            disp('not converge'); 
            %}
        end
    else
           flag_alternating=0;
    end
end
% recover r from x
if(flag_alternating)
    r=(x+x_old)/2;
else
    r=x;
end

