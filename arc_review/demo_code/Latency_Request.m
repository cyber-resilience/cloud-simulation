function [Lfunc Lgrad]=Latency_Request(x,xstar,a,b,c,intersept)

if(b<1|a<0|c<0)
    error('not convex')
end

if(x<xstar)
    Lfunc=a*x+intersept;
    Lgrad=a;
else
    Lfunc=c*(x-xstar)^b+a*x+intersept;
    Lgrad=b*c*(x-xstar)^(b-1)+a;
end

