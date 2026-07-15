build:
	python -m build

test:
	pytest -q

publish-test:
	python -m twine upload --repository testpypi dist/*

publish:
	python -m twine upload dist/*
