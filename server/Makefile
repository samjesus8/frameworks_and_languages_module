.PHONY: help
.DEFAULT_GOAL:=help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2 } END{print ""}' $(MAKEFILE_LIST)


DOCKER_IMAGE:=restapi

run: build  ## Run server in container
	docker run --rm -it --publish 8000:8000 ${DOCKER_IMAGE}
run_shell: build
	docker run --rm -it --publish 8000:8000 --volume ${PWD}:/app/:ro --entrypoint /bin/sh ${DOCKER_IMAGE}
build:
	docker build --tag ${DOCKER_IMAGE} .


run_local: node_modules
	node server.js
node_modules:
	npm install
vue.js:
	curl https://unpkg.com/vue@next -L -o vue.js

clean:
	rm -rf \
		node_modules \
		package-lock.json \
		vue.js 
