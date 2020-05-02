# Makefile adapted from https://github.com/anand-bala/probabilistic-timed-automata




.PHONY: clean
clean:
	@echo "Cleaning Python package artifacts"
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +


.PHONY: format
format: clean
	poetry run black robust_approx_rl/ tests/
	poetry run autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports --recursive robust_approx_rl/

.PHONY: check
check:
	poetry run mypy -p robust_approx_rl
	poetry run flake8 robust_approx_rl
