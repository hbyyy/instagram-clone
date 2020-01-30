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

# 프로젝트의 requirements.txt 업데이트
# poetry export를 사용해서 requirements.txt를 생성
echo '=====================requirements.txt 생성====================='
poetry export -f requirements.txt > requirements.txt

# 도커 이미지 업데이트
docker build -q -t lloasd33/wps-instagram -f Dockerfile "$HOME"/projects/wps12th/python/instagram/
docker push lloasd33/wps-instagram
#
# 서버 스크린 만들기
# 실행중이던 screen 종료
echo '=====================실행중이던 screen 종료====================='
${SSH_CMD} -C 'screen -X -S docker quit'
# 실행중이던 docker 종료
echo '=====================실행중이던 docker 종료====================='
${SSH_CMD} -C 'docker stop instagram'
# screen 실행
echo '=====================screen 실행====================='
${SSH_CMD} -C 'screen -S docker -d -m'

# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "sudo chmod 666 /var/run/docker.sock"


#도커 이미지 업데이트
echo '=====================서버 docker 이미지 업데이트====================='
${SSH_CMD} -C "docker pull lloasd33/wps-instagram"

# 로컬의 aws profile을 전달
echo '=====================로컬의 aws profile을 전달====================='
${SSH_CMD} -C "sudo rm -rf /home/ubuntu/.aws"
scp -q -i "${IDENTITY_FILE}" -r "$HOME/.aws/" ${TARGET}:/home/ubuntu
## 서버 실행 asd
#${SSH_CMD} -C "screen -r runserver -X stuff 'docker run --rm -it --name instagram -p 8001:8000 lloasd33/wps-instagram\n'"

# 실행중이던 screen 세션종료
echo '=====================실행중이던 screen 세션종료====================='
${SSH_CMD} -C 'screen -X -S docker quit'
# screen 실행
echo '=====================screen 실행====================='
${SSH_CMD} -C 'screen -S docker -d -m'
# 실행중인 screen에서 docker container를 사용해서 bash실행
echo '=====================실행중인 screen에서 docker container를 사용해서 bash실행====================='
${SSH_CMD} -C "screen -r docker -X stuff 'sudo docker run --rm -it -p 80:8000 --name=instagram lloasd33/wps-instagram /bin/bash\n'"
# bash를 실행중인 container에 HOST의 ~/.aws폴더를 복사
echo '=====================bash를 실행중인 container에 HOST의 ~/.aws폴더를 복사====================='
${SSH_CMD} -C "sudo docker cp ~/.aws/ instagram:/root"
# container에서 bash를 실행중인 screen에 runserver명령어를 전달
echo '=====================container에서 bash를 실행중인 screen에 runserver명령어를 전달====================='
${SSH_CMD} -C "screen -r docker -X stuff 'python manage.py runserver 0:8000\n'"
echo "=====================finish!====================="


