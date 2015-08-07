function y=soft_treshold(x,step_length,lambda)

    y=(abs( x)-lambda*step_length);  y(find(y<0))=0;
    y=y.*sign(x);