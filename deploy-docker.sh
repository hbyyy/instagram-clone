#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/wps12thself.pem"
USER="ubuntu"
HOST="15.164.226.135"
TARGET="${USER}@${HOST}"
ORIGIN_SOURCE="$HOME/projects/wps12th/python/instagram/"
DEST_SOURCE="/srv/"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${TARGET}"

echo '===docker 배포==='

#서버 초기 설정
echo "=====================apt-update, apt-upgrade, apt-autoremove============================"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove'

echo "=====================apt install python3-pip============================"
${SSH_CMD} -C 'sudo apt -y install python3-pip'
${SSH_CMD} -C "sudo apt -y install docker.io"

#서버에 docker 설치
#echo "=====================docker setup============================"
#${SSH_CMD} -C "sudo apt install apt-transport-https ca-certificates \\
#    curl \\
#    gnupg-agent \\
#    software-properties-common"
#
#${SSH_CMD} -C "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -"
#
#${SSH_CMD} -C "sudo apt install apt-transport-https ca-certificates \\
#    curl \\
#    gnupg-agent \\
#    software-properties-common"
#
#${SSH_CMD} -C "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -"
#
#${SSH_CMD} -C "sudo apt-key fingerprint 0EBFCD88"
#
#${SSH_CMD} -C 'sudo add-apt-repository \
#   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) \
#   stable"'
#
#${SSH_CMD} -C "sudo apt-get update"
#
#${SSH_CMD} -C "sudo apt-get install docker-ce docker-ce-cli containerd.io"
#
#${SSH_CMD} -C "sudo  groupadd docker && sudo usermod -aG docker $USER && newgrp docker "


# 프로젝트의 requirements.txt 업데이트
echo 'requirements.txt 생성'
"$HOME"/.pyenv/versions/3.7.5/envs/wps-instagram-env/bin/pip freeze > "$HOME"/projects/wps12th/python/instagram/requirements.txt

# 도커 이미지 업데이트
docker build -q -t lloasd33/wps-instagram -f Dockerfile "$HOME"/projects/wps12th/python/instagram/
docker push lloasd33/wps-instagram

# 서버 스크린 만들기
# 실행중이던 screen 종료
echo '실행중이던 screen 종료'
${SSH_CMD} -C 'screen -X -S runserver quit'
# 실행중이던 docker 종료
${SSH_CMD} -C 'docker stop instagram'
# screen 실행
echo 'screen 실행'
${SSH_CMD} -C 'screen -S runserver -d -m'

# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "sudo chmod 666 /var/run/docker.sock"
echo '서버 실행'
#도커 이미지 업데이트
${SSH_CMD} -C "docker pull lloasd33/wps-instagram"

#로컬의 aws profile을 전달
scp -q -i ${IDENTITY_FILE} -r $HOME/.aws ${TARGET}:$HOME/
# 서버 실행 asd
${SSH_CMD} -C "screen -r runserver -X stuff 'docker run --rm -it --name instagram -p 8001:8000 lloasd33/wps-instagram\n'"
echo "finish!"


