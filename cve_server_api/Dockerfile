FROM openeuler/openeuler:21.03

MAINTAINER TommyLike<tommylikehu@gmail.com>

RUN yum update && \
    yum install -y vim wget git xz tar make automake autoconf libtool gcc gcc-c++ kernel-devel libmaxminddb-devel pcre-devel openssl openssl-devel tzdata \
        readline-devel libffi-devel python3-devel mariadb-devel python3-pip net-tools.x86_64 iputils

RUN pip3 install uwsgi

WORKDIR /home/worker/app-sbom-cve/cve_server_api
COPY . /home/worker/app-sbom-cve/cve_server_api


RUN cd /home/worker/app-sbom-cve/cve_server_api && pip3 install  -r requirements.txt && sed -i "s/TMMOUT=300/TMOUT=0/g" /etc/bashrc

RUN cp /usr/bin/python3 /usr/bin/python
ENV LANG=en_US.UTF-8


EXPOSE 8100
CMD ["uwsgi", "--ini", "/home/worker/app-sbom-cve/cve_server_api/uwsgi.ini"]



