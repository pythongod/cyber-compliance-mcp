.PHONY: setup test run

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -e . pytest

test:
	. .venv/bin/activate && pytest -q

run:
	. .venv/bin/activate && cyber-compliance-mcp
