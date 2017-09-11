setup:
	python3 -m venv ~/.spot-price-ml

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. && pytest -vv --cov=paws --cov=spot-price-ml tests/*.py

lint:
	pylint --disable=R,C paws spot-price-ml

all: install lint test