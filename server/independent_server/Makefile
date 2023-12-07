DOCKER_IMAGE_NAME:=falcon-server

build:
	docker build -t ${DOCKER_IMAGE_NAME} .
run:
	docker run -p 8000:8000 ${DOCKER_IMAGE_NAME}
run_local:
	python server.py