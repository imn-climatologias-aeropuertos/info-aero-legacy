SOURCE_FILES=$(shell find . -path "./app/*.py")
TEST_FILES=$(shell find . -path "./test/*.py")
SOURCES_FOLDER=app
TESTS_FOLDER=test

BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

check_no_main:
ifeq ($(BRANCH),main)
	echo "You are good to go!"
else
	$(error You are not in the main branch)
endif

patch: check_no_main
	bumpversion patch --verbose
	git push --follow-tags

minor: check_no_main
	bumpversion minor --verbose
	git push --follow-tags

major: check_no_main
	bumpversion major --verbose
	git push --follow-tags

style:
	isort $(SOURCES_FOLDER)
	isort $(TESTS_FOLDER)
	black $(SOURCE_FILES)
	black $(TEST_FILES)

lint:
	isort $(SOURCES_FOLDER) --check-only
	isort $(TESTS_FOLDER) --check-only
	black $(SOURCE_FILES) --check
	black $(TEST_FILES) --check

tests:
	PYTHONPATH=. $(POETRY_RUN) pytest -vv test

run:
	python aeroinformes.py

# Windows build
win-build:
	del .\build\
	del .\dist\
	del *.spec
	python .\build.py
	copy .\assets\fonts\*.ttf .\dist\assets\fonts
	copy .\assets\icons\plane.* .\dist\assets\icons
	copy .\assets\img\*.png .\dist\assets\img
	copy .\README.md .\dist