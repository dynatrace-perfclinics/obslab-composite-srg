.PHONY: all format

# Get the current directory
CURRENT_DIR := $(shell pwd)

all: format

format:
	poetry run black $(CURRENT_DIR) --line-length=120
	poetry run isort $(CURRENT_DIR) --profile black --line-length 120
