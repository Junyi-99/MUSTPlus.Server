# 服务器部署

## Step 1 安装系统

推荐操作系统：Ubuntu 18.04

上来第一步，修改默认 ssh 端口

之后添加自己的 ssh pub key 到服务器的 authorized_keys 文件夹中

安装 MySQL

`sudo apt update`

`sudo apt install mysql-server`

`sudo mysql_secure_installation`

`cd /etc/mysql/mysqld.conf.d/`

`nano mysqld.cnf`

修改默认端口为其他（端口要要大于1000！）

修改bindaddress为0.0.0.0

## Step 2 开启防火墙

`ufw default deny`

`ufw allow 你的SSH端口/tcp`

`ufw allow 你的MYSQL端口/tcp`

`ufw enable`

## Step 3 部署 Python


