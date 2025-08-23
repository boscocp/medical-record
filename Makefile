setup:
	@echo "Creating and Activating Virtual Environment..." && \
	python3 -m venv .venv && source .venv/bin/activate
	@echo "Installing dependencies..."  && \
	pip install -r requirements.txt

	