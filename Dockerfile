FROM jenkins/jenkins:lts

USER root

# Install tools
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install Docker CLI
RUN curl -fsSL https://get.docker.com | sh

# Install kubectl (IMPORTANT FIX)
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Allow Jenkins to use docker
RUN usermod -aG docker jenkins

USER jenkins
