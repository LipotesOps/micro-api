FROM centos:centos7.9.2009

# 设置编码
ENV LANG en_US.UTF-8
# 同步时间
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 1. 安装基本依赖
RUN yum update -y && yum install epel-release -y && yum install wget unzip epel-release nginx xz gcc automake zlib-devel openssl-devel supervisor  groupinstall development  libxslt-devel libxml2-devel libcurl-devel git libffi-devel -y
#WORKDIR /var/www/

WORKDIR /home

# 2. 准备python
# RUN wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tar.xz
COPY Python-3.8.6.tar.xz Python-3.8.6.tar.xz
RUN xz -d Python-3.8.6.tar.xz && tar xvf Python-3.8.6.tar && cd Python-3.8.6 && ./configure && make && make install

RUN rm -f Python-3.8.6.tar.xz

COPY requirements.txt /home/requirements.txt


RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN pip3 config set install.trusted-host mirrors.aliyun.com
RUN pip3 install -U pip
# bugfix for installing pdbpp
RUN pip3 install setuptools_scm
RUN python3 -m pip install --no-cache -r requirements.txt

EXPOSE 5000

RUN mkdir -p /home/micro-api
WORKDIR /home/micro-api
RUN export FLASK_APP=/home/micro-api/autoapp.py
CMD ["python3", "-m flask run"]