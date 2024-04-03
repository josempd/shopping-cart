.PHONY: up up-detached down destroy test help

# Run docker-compose up and start the containers.
up:
	@docker-compose up -d

# Run docker-compose up in detached mode.
up-attached:
	@docker-compose up

# Stop and remove the containers.
down:
	@docker-compose down

# Stop and remove the containers and volumes.
destroy:
	@docker-compose down -v

# Run tests with pytest.
test:
	@pytest tests/

# Show help.
help:
	@echo "Makefile commands:"
	@echo "up          Start the containers using docker-compose.  (containers run in the background)"
	@echo "up-attached Start the containers in attached mode."
	@echo "down        Stop and remove the containers."
	@echo "destroy     Stop and remove the containers and volumes."
	@echo "test        Run tests with pytest."
	@echo "help        Display this help message."
