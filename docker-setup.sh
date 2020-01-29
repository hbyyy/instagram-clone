#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/wps12thself.pem"
USER="ubuntu"
HOST="52.78.84.148"
TARGET="${USER}@${HOST}"
ORIGIN_SOURCE="$HOME/projects/wps12th/python/instagram/"
DEST_SOURCE="/srv/"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${TARGET}"

${SSH_CMD} -C "sudo apt install apt-transport-https ca-certificates \\
    curl \\
    gnupg-agent \\
    software-properties-common"

${SSH_CMD} -C "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -"

${SSH_CMD} -C "sudo apt-key fingerprint 0EBFCD88"

${SSH_CMD} -C 'sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"'

${SSH_CMD} -C "sudo apt-get update"

${SSH_CMD} -C "sudo apt-get install docker-ce docker-ce-cli containerd.io"

${SSH_CMD} -C "sudo groupadd docker && sudo usermod -aG docker $USER && newgrp docker "



