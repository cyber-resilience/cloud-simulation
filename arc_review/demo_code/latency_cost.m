function [Lcost Lcost_grad] =latency_cost(latency,latency_s,phi)
 
 if(latency-latency_s<0)
     Lcost=0;
     Lcost_grad=0;
 else
     Lcost=(latency-latency_s)^phi;
     Lcost_grad=phi*(latency-latency_s)^(phi-1);     
 end
 