#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/wps12thself.pem"
HOST="ubuntu@54.180.86.244"
ORIGIN_SOURCE="$HOME/projects/wps12th/python/instagram/"
DEST_SOURCE="/home/ubuntu/projects/"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${HOST}"


# 프로젝트의 requirements.txt 업데이트
echo 'requirements.txt 생성'
pip freeze > requirements.txt


echo '==runserver 배포=='
# 기존 폴더 삭제
echo '기존 폴더 삭제'
${SSH_CMD} sudo rm -rf ${DEST_SOURCE}

# 로컬에 있는 파일 업로드
echo '로컬에 있는 파일 업로드'
${SSH_CMD} mkdir -p ${DEST_SOURCE}
scp -q -i "${IDENTITY_FILE}" -r "${ORIGIN_SOURCE}" ${HOST}:${DEST_SOURCE}

# 서버에 패키지 설치
echo '서버에 패키지 설치 중'

${SSH_CMD} pip3 install -q -r /home/ubuntu/projects/instagram/requirements.txt
# 실행중이던 screen 종료
echo '실행중이던 screen 종료'
${SSH_CMD} -C 'screen -X -S runserver quit'

# screen 실행
echo 'screen 실행'
${SSH_CMD} -C 'screen -S runserver -d -m'

# 실행중인 세션에 명령어 전달
echo '서버 실행'
  ${SSH_CMD} -C "screen -r runserver -X stuff 'sudo python3 /home/ubuntu/projects/instagram/app/manage.py runserver 0:8000\n'"

echo '배포 완료'

