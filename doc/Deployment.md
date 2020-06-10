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

## Step 2 安装 MySQL

参考自：https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04


`sudo apt update`

`sudo apt install mysql-server`

`sudo mysql_secure_installation`

按照提示做出相应选择，一般是输入一个密码，剩下的全都 YES

然后编辑 Mysql 端口

`cd /etc/mysql/mysqld.conf.d/`

`sudo nano mysqld.cnf`

修改默认端口为其他（端口要要大于1000！）

修改bindaddress为0.0.0.0

## Step 3 配置 MySQL

```MySQL
sudo mysql
SELECT user,authentication_string,plugin,host FROM mysql.user;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的密码';
FLUSH PRIVILEGES;
SELECT user,authentication_string,plugin,host FROM mysql.user;
exit
```

### 创建 must_plus 用户

```
CREATE USER 'must_plus'@'%' IDENTIFIED BY '这里写密码';
```



```
GRANT ALL PRIVILEGES ON must_plus.* TO 'must_plus'@'%' WITH GRANT OPTION;
```

### 创建 must_plus 数据库，编码 utf8mb4_unicode_ci

```
CREATE DATABASE must_plus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Step 4 添加用户~~~~

在这一步里，你应该创建一个名为 must_plus 的新**普通用户**，并且牢牢限定它的用户权限，以保证安全

这个账户**不要赋予** root 组权限

`sudo useradd -m must_plus`

-m 表示 自动建立用户的登入目录

由于我们的系统用户数量只有一个，所以就不设置用户组了。

然后我们来修改用户密码：

`sudo passwd must_plus`

输入你设置的密码，并且保管妥当

如果有需要，修改 `/etc/passwd` ，给用户设置 zsh 或 bash

## Step 5 设置公钥登录

`ssh-keygen` 生成属于该用户的密钥对

`cd ~/.ssh` 切换到 ssh 配置目录

`nano authorized_keys` 授权列表

然后把你的 id_rsa.pub 文件的内容粘贴进去

一条记录一行

保存

## Step 6 开启防火墙

这一步执行之前，你应该已经完成了 SSH 和 MySQL 的配置工作

`sudo ufw default deny`

`sudo ufw allow 你的SSH端口/tcp`

`sudo ufw allow 你的MYSQL端口/tcp` (如果不暴露 MySQL 这条可以忽略 )

`sudo ufw allow 服务器要用的端口/tcp` (如果不暴露 MySQL 这条可以忽略 )

`sudo ufw enable` （enable 前请确认已经修改了SSH端口之类的，否则会被拒绝连接到服务器）

## Step 7 配置服务器

请确保 settings 目录符合下面的文件夹结构：
```
├─settings
│      database.py
│      server.py
│      urls.py
│      __init__.py
```
（其中，`database.py` 和 `server.py` **不应**出现在 git 中）

这两个文件应由开发者自己编写，对于 `database.py`，内容如下：

```
NAME = ''
USER = ''
PASSWORD = ''
HOST = ''
PORT = ''
```

对于 `server.py`，内容示例如下： 
```
SECRET_KEY = '这里是只有自己知道的密码'
```

## Step 8 部署 Python

# 注意，对 MUSTPLUS 服务器的任何操作，都应当在 virtualenv 环境下进行

执行该操作之前请先 clone 本 repository 到本地，并且 cd 到项目根目录（以下操作在 must_plus 账户下进行）

安装 virtualenv

`sudo apt-get install python-virtualenv`

`pip3 install virtualenv`

创建 virtualenv 目录

`virtualenv -p python3 --no-site-packages venv`

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

### 安装 uwsgi （非常建议）

修改 `uwsgi.ini` 内容

把 chdir 改为现在的目录

把 daemonize 改为其他目录

processes、workers、threads 按需修改

`sudo pip3 install uwsgi` (系统级安装)

### 启动服务器（uwsgi）

记得也配置一下防火墙允许 8000 端口出入（django端口）

`uwsgi --ini uwsgi.ini`

用 ps 看看有没有启动成功

`ps -aux | grep uwsgi`

注意：你应该先用基本的 `python3 manage.py runserver 0.0.0.0:8000` 来测试是否能正常启动，再使用 uwsgi 启动

这样可以避免你遇到一些因为自己能力问题不知道怎么解决的问题

## 其他：

因为你懂得的原因，我们要把 apt 和 pip 的源都换成国内的

## Nginx + uWSGI + Django 部署：

`https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html`

看英文原版教程，就能配置成功，中文翻译的太差


### apt 换国内源:

`sudo nano /etc/apt/sources.list`

**在文件添加以下条目:**
```
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
```

# pip3切换源

`mkdir ~/.pip`

`nano ~/.pip/pip.conf`

# 然后将下面这两行复制进去就好了
```
np
```
