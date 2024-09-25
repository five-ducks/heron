CHROME=/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome

all: up

# Start the containers in detached mode
up: 
	docker-compose up -d

docs:
	$(CHROME) --incognito http://localhost:8000/docs

admin:
	$(CHROME) --incognito http://localhost:8000/admin

open:
	open -a "Google Chrome" https://localhost:443

fclean:
	docker stop $$(docker ps -qa) 2>/dev/null || true; \
	docker rm $$(docker ps -qa) 2>/dev/null || true; \
	docker rmi -f $$(docker images -qa) 2>/dev/null || true; \
	docker volume rm $$(docker volume ls -q) 2>/dev/null || true; \
	docker network rm $$(docker network ls -q) 2>/dev/null || true

.PHONY: build up down clean logs