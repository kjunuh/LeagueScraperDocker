DESTDIR=server
host_port=11000

all: start
	@echo "Done"

docker-all: docker-build docker-interactive
	@echo "DONE"

docker-build:
	@echo "building the image from docker file..."
	docker build -t e222/hello .
	@echo "image DONE"

docker-start:
	@echo "starting the NEW service in container..."
	docker run  -p 11000:8080 e222/hello

docker-interactive:
	@echo "Starting the container using volumes"
	docker run  -p ${host_port}:8080 -v $(shell pwd):/src -it e222/hello

service:
	@echo "creating the service..."
	pip install --upgrade pip
	pip install -r requirements.txt

start:
	@echo "starting the NEW service..."
	pip install --upgrade pip
	pip install -r requirements.txt
	python server.py

docker-stop:
	@echo "stoping the service..."
	docker stop $$(docker ps -alq)
	@echo "service stopped"

docker-remove:
	@echo "removing the image..."
	docker rmi -f e222/hello
	@echo "image removed"

docker-prune:
	docker system prune

docker-clean: docker-stop docker-remove docker-prune
	@echo "DONE"

clean:
	@echo "removing service files created"
	rm -rf $(CREATED)