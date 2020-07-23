
init:
	pip install pytest

test:
	pytest

env-init:
	(\
		python3 -m venv ./env; \
		source "./env/bin/activate"; \
		pip3 install --upgrade pip \
		pip3 install -r "./requirements.txt" \
	)

.PHONY: init test