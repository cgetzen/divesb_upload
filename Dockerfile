FROM centos:7
MAINTAINER Charlie Getzen

EXPOSE 5000

RUN yum -y install git
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python36u
RUN yum -y install python36u-pip

RUN cd /home
RUN python3.6 -m venv /home/venv
RUN git clone https://github.com/cgetzen/divesb_upload.git /home/divesb_upload/
RUN source /home/venv/bin/activate && pip install -r /home/divesb_upload/requirements.txt


CMD source /home/venv/bin/activate && nohup python /home/divesb_upload/app.py &
