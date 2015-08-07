function [x]=latency2request(latency,a,b,c,d,x_critical)

n=size(latency,1);
x=(latency-d)/a; % steady state
for i=1:n
  if(x(i)<=d)
      x(i)=0;      
  elseif(x(i)>x_critical(i))
      disp('over critical')
      flag=1;
      k=x_critical(i);
          while(flag)
            tmp=latency(i)-c*(k-x_critical(i))^b-a*k-d;
                if(tmp>0)
                    k=k+1;
                else
                    x(i)=k;
                    flag=0;
                end
          end
  end
end
