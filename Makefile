coverage-html: test
	coverage html

coverage-report: test
	coverage report

requirements:
	pip install -r requirements.txt

run:
	python src/main.py

test:
	coverage run --source=src -m pytest tests
