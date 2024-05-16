FROM ubuntu:latest

# Install SSH server and pwgen
RUN apt-get update && apt-get install -y openssh-server pwgen inetutils-ping
RUN mkdir /var/run/sshd

# Create a student user
ARG USERNAME
ARG PASSWORD
RUN useradd -m -s /bin/bash $USERNAME

# Set the password for the student user
RUN echo "$USERNAME:$PASSWORD" | chpasswd

# Expose SSH port
EXPOSE 22

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]