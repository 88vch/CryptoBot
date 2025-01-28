# Makefile for running scraper.py

# Define the Python interpreter and script
PYTHON = python3
SCRIPT = scraper.py

# Default target to run the scraper
run:
	$(PYTHON) $(SCRIPT)

# # Target to create a virtual environment
# venv:
# 	python -m venv venv

# Target to install dependencies (if you have a requirements.txt)
install:
	venv/bin/pip install -r requirements.txt

# Target to clean up (if needed)
clean:
	rm -rf __pycache__ venv

# Phony targets
.PHONY: run venv install clean
