PACKAGE_NAME := powerhub
clean:
	@rm -rf build __pycache__ *.egg-info docs/_build .docvenv .tox dist $(PACKAGE_NAME)/*.egg-info $(PACKAGE_NAME)/__pycache__

docs:
	@find .docvenv -maxdepth 0 -type d || python3 -m venv .docvenv ; \
	. .docvenv/bin/activate ; \
	cd docs ; \
	python3 -m pip install -r requirements.txt ; \
	sphinx-build . _build

test:
	tox

# \n in sed only works in GNU sed
release:
	@read -p "Enter version string (Format: x.y.z): " version; \
	echo "Version Bump: $$version"; \
	date=$$(date +%F); \
	sed -i "s/^version = \".*\"/version = \"$$version\"/" pyproject.toml && \
	sed -i "s/^release = \".*\"/release = \"$$version\"/" docs/conf.py && \
	sed -i "s/^## \[Unreleased\]/## [Unreleased]\n\n## [$$version] - $$date/" CHANGELOG.md && \
	git add CHANGELOG.md pyproject.toml docs/conf.py && \
	git commit -m "Version bump: $$version" && \
	git tag $$version && \
	read -p "Committed and tagged. Do you want push the new version? [y/n] " ans && \
	if [ $$ans = 'y' ] ; then git push && git push --tags && echo "Pushed." ; else echo "Push it yourself then." ; fi

build:
	python -m build

test-publish:
	@file=$$(ls -1t dist/$(PACKAGE_NAME)-*.tar.gz | head -n1); \
	read -p "[TEST] Ready to upload $$file? Type yes: " ans; \
	if [ $$ans = 'yes' ] ; then twine upload -r testpypi $$file ; fi


publish:
	@file=$$(ls -1t dist/$(PACKAGE_NAME)-*.tar.gz | head -n1); \
	read -p "Ready to upload $$file? Type yes: " ans; \
	if [ $$ans = 'yes' ] ; then twine upload $$file ; fi


.PHONY: clean docs test release build publish test-publish
