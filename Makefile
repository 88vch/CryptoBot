# Makefile for running scraper.py
SRCDIR = src
RESDIR = res

# Define the Python interpreter and script
PYTHON = python3
SCRIPT = scraper.py

.PHONY: run clean

# Default target to run the scraper
run:
	@mkdir -p $(RESDIR)
	$(PYTHON) $(SCRIPT)

# Target to install dependencies (if you have a requirements.txt)
install:
	venv/bin/pip install -r requirements.txt

# Target to clean up (if needed)
clean:
	@rm -rf $(RESDIR)
	rm -rf __pycache__ venv

# Phony targets
.PHONY: run venv install clean
