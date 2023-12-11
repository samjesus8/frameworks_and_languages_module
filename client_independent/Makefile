DOCKER_IMAGE_NAME:=react-app

build:
	docker build --tag ${DOCKER_IMAGE_NAME} .

run:
	docker run --rm -it --publish 8001:8001 ${DOCKER_IMAGE_NAME}