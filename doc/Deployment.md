# 服务器部署

## Prerequisites

You may need to install the Python and MySQL development headers and libraries like:

`sudo apt install python3-dev default-libmysqlclient-dev python3-pip`

`pip3 install mysqlclient requests beautifulsoup4 lxml`


## Step 1 安装系统

推荐操作系统：Ubuntu 18.04

上来第一步，修改默认 ssh 端口，并且关闭密码登录，只允许使用密钥文件登录

`sudo nano /etc/ssh/sshd_config`

...

之后添加自己的 ssh pub key 到服务器的 authorized_keys 文件夹中

安装 MySQL

`sudo apt update`

`sudo apt install mysql-server`

`sudo mysql_secure_installation`

按照提示做出相应选择

然后编辑 Mysql 端口

`cd /etc/mysql/mysqld.conf.d/`

`nano mysqld.cnf`

修改默认端口为其他（端口要要大于1000！）

修改bindaddress为0.0.0.0

## Step 2 开启防火墙

`ufw default deny`

`ufw allow 你的SSH端口/tcp`

`ufw allow 你的MYSQL端口/tcp` (如果不暴露 MySQL 这条可以忽略 )

`ufw enable` （enable 前请确认已经修改了SSH端口之类的，否则会被拒绝连接到服务器）

！！！注意。在这一步里，你应该创建一个名为 must_plus 的新用户，并且牢牢限定它的用户权限，以保证安全！！！
！！！注意。在这一步里，你应该创建一个名为 must_plus 的新用户，并且牢牢限定它的用户权限，以保证安全！！！
！！！注意。在这一步里，你应该创建一个名为 must_plus 的新用户，并且牢牢限定它的用户权限，以保证安全！！！


## Step 3 部署 Python

执行该操作之前请先 clone 本 repository 到本地，并且 cd 到项目根目录

安装 virtualenv

`pip3 install virtualenv`

创建 virtualenv 目录

`python3 -m virtualenv venv`

进入 venv 环境

`source ./venv/bin/activate`

安装 requirements

`pip3 install -r requirements.txt`

创建表（请确认数据库配置无误，才可进入此操作）
```
find ./services -name migrations | xargs rm -rf
find ./services -name __pycache__ | xargs rm -rf

python3 manage.py makemigrations --empty authentication basic course moments news student teacher timetable mustplus spider

python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000
```

出现

```
Loading RSA Key ...
RSA Key Loaded.
Loading RSA Key ...
RSA Key Loaded.
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 27, 2020 - 11:24:27
Django version 3.0b1, using settings 'mustplus.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```

即表示成功部署服务器

## 安装 uwsgi （非常建议）

修改 `uwsgi.ini` 内容

把 chdir 改为现在的目录

把 daemonize 改为其他目录

processes、workers、threads 按需修改

`pip3 install uwsgi`

## Step 4 配置服务器

请确保 Settings 符合下面的文件夹结构：
```
├─settings
│      database.py
│      server.py
│      urls.py
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

对于 `server.py`，内容示例如下： 
```
SECRET_KEY = 'yfyzhc%840_!g%!#(sqy(ccock4^z4ohl=$-*3xpoe+v^cq)ih'
```


## 启动服务器

记得也配置一下防火墙允许 8000 端口出入（django端口）

`uwsgi --ini uwsgi.ini`



## 其他：Database

数据库：

must_plus

编码字符集：

utf8mb4_unicode_ci


## 其他：整体流程

```
# 换国内源:
sudo nano /etc/apt/sources.list
# 在文件添加以下条目:
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse

sudo apt update
sudo apt install openssh-server
sudo apt install git python3-dev python3-pip python3-venv default-libmysqlclient-dev 






# MySQL
# https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04
sudo apt install mysql-server
sudo mysql_secure_installation
# 输入想要设置MySQL的root的密码
# Yes, Yes, Yes, Yes
sudo mysql
SELECT user,authentication_string,plugin,host FROM mysql.user;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的密码';
FLUSH PRIVILEGES;
SELECT user,authentication_string,plugin,host FROM mysql.user;
exit

# 创建用户

```
CREATE USER 'mustplus'@'%' IDENTIFIED BY 'qNg%AbN3#8#kqOAr';
```

```
GRANT ALL PRIVILEGES ON must_plus.* TO 'mustplus'@'%' WITH GRANT OPTION;
```

# 创建数据库 

```
CREATE DATABASE must_plus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```


`cd /etc/mysql/mysql.conf.d/`

`sudo nano mysqld.cnf`

# 修改默认端口为其他（端口要要大于1000！）

# 修改bindaddress为0.0.0.0 （如果要暴露的话）


# 开启防火墙
sudo ufw default deny
sudo ufw allow 22/tcp
sudo ufw allow 3306/tcp
sudo ufw allow 8000/tcp
sudo ufw enable



# pip3切换源
mkdir ~/.pip
nano ~/.pip/pip.conf
# 然后将下面这两行复制进去就好了
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple


pip3 install mysqlclient requests beautifulsoup4 virtualenv lxml
git clone https://github.com/Military-Doctor/MUSTPlus.Server.git
cd MUSTPlus.Server
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```
