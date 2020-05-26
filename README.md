# MUSTPlus.Server

The back-end.

Macau University of Science and Technology Campus Application ( Server )

## Documentation

Please check the `doc` folder.
.

## API 文档

请移步 `\doc\API Document\API Document.md`

## Environments

Server: **Ubuntu 18.04**

Database Management: **MySQL**

Development Language: **Python 3.6.x**

Framework: **Django 3.0.6**

## Deployment

Please follow the [instructions](https://github.com/Military-Doctor/MUSTPlus.Server/blob/master/doc/Deployment.md)

建议 Nginx + uWSGI + Django 部署模式

以下为实测并发：

**腾讯云 1 核心 2G 内存，内网**

Django：`400`

uWSGI + Django：`480`

Nginx + uWSGI + Django：`1870`  （使用 socket 文件而非 port）

**I7-7700HQ  4 核 8 线程 4G 内存，内网**

Django: `360`

uWSGI + Django: `8860`

Nginx + uWSGI + Django: `没测`

**总结**

测试结果受限于带宽，就算 Nginx + uWSGI 的方案，跑在 1M 小水管下，只能跑出 240 Requests / sec 的成绩。同时还受限于腾讯云的服务器就1个核心。

Nginx 的性能表现非常出色，单独测试时每秒并发可以达到 `13300`

如果后期可以使用 Golang 重写，那么应该性能可以得到进一步提升


## License

The MUSTPlus.Server is released under version 3.0 of the [GNU GENERAL PUmaster/LICENSE).BLIC LICENSE](https://github.com/Military-Doctor/MUSTPlus.Server/blob/

