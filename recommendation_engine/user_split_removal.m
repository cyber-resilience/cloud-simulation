function [AC_left edgelist_left]=user_split_removal(edgelist,edgelist_removed,AC)

ind_rem=[];
m=size(edgelist_removed,1);
U=max(edgelist(:,1));
AC_new=AC;

% remove
for i=1:m
    tmp=find(edgelist(:,1)==edgelist_removed(i,1)&edgelist(:,2)==edgelist_removed(i,2));
    ind_rem=[ind_rem tmp];
    AC_new(edgelist_removed(i,1),edgelist_removed(i,2))=0;
end
%nnz(AC)-nnz(AC_new)
%nnz(AC_new)
%{
% merge

user_new=unique(edgelist_removed(:,1));
Unew=U+length(user_new);
edgeliest_add=zeros(size(edgelist_removed,1),2);
for i=1:length(user_new)
    ind=find(edgelist_removed(:,1)==user_new(i));    
    edgelist_add(ind,1)=U+i;
    edgelist_add(ind,2)=edgelist_removed(ind,2);
    %edgelist_add(ind,3)=edgelist(edgelist_removed(ind),3);    
    AC_new(U+i,edgelist_removed(ind,2)')=1;
end
%size(edgelist_add,2)
%size(edgelist_removed,2)
%nnz(AC_new)

if(size(edgelist_add,2)~=size(edgelist_removed,2)); error('removal problem 1'); end
if(nnz(AC_new)~=nnz(AC)); error('removal problem 2'); end
%}

edgelist(ind_rem,:)=[];
edgelist_left=edgelist;
AC_left=AC_new;



