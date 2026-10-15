PYTHON ?= python3
UV ?= uv

.PHONY: install run build debug clean lint lint-strict

install:
	$(UV) sync

run:
	$(UV) run $(PYTHON) pac-man.py config.json

build:
	$(UV) run pyinstaller --onefile --noconfirm --name pac-man \
		--add-data "assets:assets" \
		--add-data "config.json:." \
		pac-man.py

debug:
	$(UV) run $(PYTHON) -m pdb -m pac-man.py config.json

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .mypy_cache -prune -exec rm -rf {} +
	rm -rf build dist
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f pac-man.spec

lint:
	$(UV) run flake8 . --exclude .venv
	$(UV) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude .venv

lint-strict:
	$(UV) run flake8 . --exclude .venv
	$(UV) run mypy . --strict --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude .venv