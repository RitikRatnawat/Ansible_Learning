FROM ubuntu:latest

RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository --yes --update ppa:ansible/ansible
RUN apt install ansible -y
RUN echo "Hello World, I'm Ansible"

CMD ["sleep", "infinity"]