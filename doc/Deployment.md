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

安装 virtualenv

`pip3 install virtualenv`

创建 virtualenv 目录

`virtualenv venv`

进入 venv 环境

`source ./venv/bin/active`

安装 requirements

`pip3 install -r requirements.txt`



## Step 4 配置服务器

请确保 Settings 符合下面的文件夹结构：
```
├─Settings
│      Database.py
│      Server.py
│      URLS.py
│      __init__.py
```
（其中，`Database.py` 和 `Server.py` **不应**出现在 git 中）

这两个文件应由开发者自己编写，对于 `Database.py`，内容如下：

```
NAME = ''
USER = ''
PASSWORD = ''
HOST = ''
PORT = ''
```

对于 `Server.py`，内容如下： 
```
SECRET_KEY = 'yfyzhc%840_!g%!#(sqy(ccock4^z4ohl=$-*3xpoe+v^cq)ih'
```

## Database

数据库：

must_plus

编码字符集：

utf8mb4_unicode_ci