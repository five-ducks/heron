#!/bin/sh

# 모든 컨테이너 중지
docker stop $(docker ps -qa)

# 모든 컨테이너 삭제
docker rm $(docker ps -qa)

# 모든 이미지 강제 삭제
docker rmi -f $(docker images -qa)

# 모든 볼륨 삭제
docker volume rm $(docker volume ls -q)

# 모든 네트워크 삭제 (기본 네트워크 제외)
docker network rm $(docker network ls -q) 2>/dev/null

