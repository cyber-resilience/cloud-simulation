
yum update -y
yum install nfs-utils -y
yum install mysql-server -y
yum install gcc -y
yum install cpan -y

cpan (answer yes to everything)
install LWP::Simple
install DBI


cat >> /etc/fstab <<EOF
nfs:/data /data nfs rsize=8192,wsize=8192,timeo=14,intr
EOF


cat >> /etc/hosts <<EOF
10.0.100.139 nfs
10.0.100.140 getfile
10.0.100.141 genfile
10.0.100.142 ingestfile
10.0.100.143 db
10.0.100.144 web
EOF


mount /data

## /home/admin/.ssh/***


# /etc/exports on nfs
#/data *(rw,sync,no_root_squash)
# service rpcbind start
# service nfslock start
# service nfs start



# db
#su - mysql
#mysql_install_db
#mysqld_safe &
#mysql_secure_installation
#questions
#service mysqld restart


