# run commands with poetry run make to use the correct configuration
run:
	streamlit run $(ST_FILE)

CODE_PATH = ./d4f_emissions
	
check: black-check isort-check mypy flake8 test

format:
	black $(CODE_PATH)
	isort $(CODE_PATH)

black: 
	black $(CODE_PATH)

black-check:
	black --check $(CODE_PATH)

isort:
	isort $(CODE_PATH)

isort-check:
	isort --check $(CODE_PATH)

mypy:
	mypy $(CODE_PATH)

flake8:
	# Options not configurable in pyproject.toml
	flake8 --statistics --extend-ignore=E203,W503 --max-line-length=80 $(CODE_PATH)

test:
	# pytest $(CODE_PATH)