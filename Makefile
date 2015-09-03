SHELL = /bin/bash

PYVERSIONS = $(shell pyversions -i; py3versions -i)
PYVERSIONSPATHS = $(shell for PV in $(PYVERSIONS); do which $$PV; done)

.PHONY: test examples testinstall all

PYTHONPATH=$(shell pwd)
export PYTHONPATH

HIYAPYCOVERSION=$(shell PYTHONPATH=$(PYTHONPATH)/hiyapyco:$(PYTHONPATH) python -c 'from version import VERSION; print VERSION')

export GPGKEY=ED7D414C

pypiupload: PYPIREPO := pypi
pypiuploadtest: PYPIREPO := pypitest

quicktest: test examples
alltest: clean quicktest testinstall
# FIXME: testinstallvirtualenv fails due to jinja2 2.8 error w/ python3.2
#alltest: clean quicktest testinstall testinstallvirtualenv

printversions:
	@echo -e "HIYAPYCOVERSION:\t$(HIYAPYCOVERSION)"
	@echo -e "PYVERSIONS:\t\t$(PYVERSIONS)"
	@echo -e "PYVERSIONSPATHS:\t$(PYVERSIONSPATHS)"

test:
	@RET=0; \
		for p in $(PYVERSIONS); do \
			echo "python version $$p"; \
			for t in test/test_*.py; do \
				$$p -t $$t; \
				RET=$$?; \
				if [ $$RET -gt 0 ]; then break 2; fi; \
			done; \
			echo ""; \
		done; \
		exit $$RET

examples:
	@RET=0; \
		for p in $(PYVERSIONS); do \
			echo "python version $$p"; \
			for t in examples/*.py; do \
				[ "$$t" = "examples/hiyapyco_example.py" ] && continue; \
				echo "$$p -t $$t ..."; \
				$$p -t $$t > /dev/null 2>&1; \
				RET=$$?; \
				if [ $$RET -gt 0 ]; then $$p -t $$t; break 2; fi; \
			done; \
			echo ""; \
		done; \
		exit $$RET

testinstall:
	@set -e; \
		for p in $(PYVERSIONS); do \
			rm -rf /tmp/hiyapyco; \
			echo ""; \
			echo "$@ w/ python version $$p ..."; \
			echo ""; \
			$$p setup.py install --root=/tmp/hiyapyco; \
			echo ""; \
			echo "$@ w/ python version $$p : OK"; \
			echo ""; \
		done

testinstallvirtualenv:
	@set -e; \
		BASETMP=/tmp/hiyapyco; \
		rm -rf $$BASETMP; \
		for p in $(PYVERSIONSPATHS); do \
			VENV=$$BASETMP/$$(basename $$p); \
			mkdir -p $$VENV; \
			echo "$@ w/ python version $$(basename $$p) in $$VENV ..."; \
			virtualenv -p $$p $$VENV; \
			source $$VENV/bin/activate; \
			which python; \
			python --version; \
			python setup.py install; \
			echo ""; \
			echo " ... test install ..."; \
			python -c 'import sys; from hiyapyco import __version__ as hiyapycoversion; print ("hiyapyco %s" % hiyapycoversion); print (sys.version)'; \
			deactivate; \
		done

clean: distclean

distclean:
	python setup.py clean
	rm -rf release dist build HiYaPyCo.egg-info README.txt
	find . -type f -name \*.pyc -exec rm -v {} \;

sdist:
	python setup.py sdist

wheel:
	# requires a 'sudo pip install wheel'
	python setup.py bdist_wheel

pypi: sdist wheel
pypiuploadtest: pypi pypiuploaddo
pypiupload: pypi pypiuploaddo
pypiuploaddo:
	# set use-agent in ~/.gnupg/gpg.conf to use the agent
	pandoc -f markdown -t rst README.md > README.txt
	python setup.py sdist bdist_wheel upload -r $(PYPIREPO) -s -i $(GPGKEY)
	rm -rf README.txt
	@echo "test the result at: https://$(PYPIREPO).python.org/pypi/HiYaPyCo"

gpg-agent:
	gpg-agent; \
		RET=$$?; echo "gpg agent running: $$RET"; \
		if [ $$RET -gt 0  ]; then \
			gpg-agent; \
			echo 'please run eval "eval $$(gpg-agent --daemon)"'; \
			exit 1; \
			fi
dch-increment:
	@# use this to increment the deb relese number for a existing release
	@DEBEMAIL=$$(git config --local --get user.email) \
		 DEBFULLNAME="Klaus Zerwes zero-sys.net" \
		 dch -i "new debian release"
	@git diff debian/changelog
dch-version:
	@# use this after updating hiyapyco/version.py
	@if $$(dpkg --compare-versions $$(dpkg-parsechangelog | sed '/^Version: /!d; s/^Version: \([.0-9]*\).*/\1/g') lt $(HIYAPYCOVERSION)); then \
		DEBEMAIL=$$(git config --local --get user.email) \
			DEBFULLNAME="Klaus Zerwes zero-sys.net" \
			dch -v $(HIYAPYCOVERSION)-1 -D stable "release version $(HIYAPYCOVERSION)"; \
			git diff debian/changelog; \
		else \
			echo "nothing to do"; \
		fi

deb: gpg-agent
	rm -rf release/deb/build
	mkdir -p release/deb/build
	tar cv -Sp --exclude=dist --exclude=build --exclude='*/.git*' -f - . | ( cd release/deb/build && tar x -Sp -f - )
	cd release/deb/build && dpkg-buildpackage -b -k$(GPGKEY) -p'gpg --use-agent'
	gpg --verify release/deb/hiyapyco_*.changes
	rm -rf release/deb/build
	lintian release/deb/*.deb

debrepo: deb
	cd release/deb && \
		apt-ftparchive packages . > Packages && \
		gzip -c Packages > Packages.gz && \
		bzip2 -c Packages > Packages.bz2 && \
		lzma -c Packages > Packages.lsma
	echo "Suite: stable testing" >> release/deb/Release
	echo "Origin: Klaus Zerwes zero-sys.net" >> release/deb/Release
	echo "Label: hiyapyco" >> release/deb/Release
	echo "Architectures: all" >> release/deb/Release
	echo "Description: HiYaPyCo Debian Repository" >> release/deb/Release
	cd release/deb && apt-ftparchive release . >> Release
	cd release/deb && \
		gpg -abs --default-key $(GPGKEY) --use-agent -o Release.gpg Release
	gpg --verify release/deb/Release.gpg release/deb/Release

rpm: gpg-agent
	mkdir -p release/rpm/noarch
	python setup.py bdist_rpm --binary-only \
		--doc-files README.md --requires python-yaml,python-jinja2 \
		-d release/rpm/noarch
	for f in release/rpm/noarch/*.rpm; do \
		expect -c "spawn rpmsign \
				-D \"%__gpg_sign_cmd  %{__gpg} gpg --batch  --no-armor --use-agent --no-secmem-warning -u '\%{_gpg_name}' -sbo \%{__signature_filename} \%{__plaintext_filename}\" \
				-D \"%__gpg_check_password_cmd  /bin/true\" \
			--resign --key-id=$(GPGKEY) $$f; \
			expect \"Enter pass phrase: \"; \
			send -- \"FuckRPM\r\n\"; expect eof"; \
		rpm --checksig --verbose $$f | grep -i $(GPGKEY); \
		done

rpmrepo: rpm
	cd release/rpm; \
		rm -fv repodata/repomd.xml*; \
		createrepo . ; \
		gpg --default-key $(GPGKEY) --use-agent -a --detach-sign repodata/repomd.xml; \
		gpg -a --export $(KEY) > repodata/repomd.xml.key

tag:
	@git pull
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "uncommited changes"; \
		git status --porcelain; \
		false; \
		fi
	@if [ -n "$$(git log --oneline --branches --not --remotes)" ]; then \
		echo "unpushed changes"; \
		git log --oneline --branches --not --remotes ; \
		false; \
		fi
	git tag -a "release-$(HIYAPYCOVERSION)" -m "version $(HIYAPYCOVERSION) released on $$(date -R)"

pushtag:
	git push origin "release-$(HIYAPYCOVERSION)"

repo: debrepo rpmrepo

upload: uploadrepo pypiupload

uploadrepo: repo
	scp -r release/* repo.zero-sys.net:/srv/www/repo.zero-sys.net/hiyapyco/

testdebversion:
	@if $$(dpkg --compare-versions $$(dpkg-parsechangelog | sed '/^Version: /!d; s/^Version: \([.0-9]*\).*/\1/g') lt $(HIYAPYCOVERSION)); then \
		echo "debian version must be incremented to HIYAPYCOVERSION $(HIYAPYCOVERSION)"; \
		echo "run make dch-version"; \
		false; \
		fi

releasetest: distclean alltest repo pypi
	@echo "$@ done"
	@echo "you may like to run $(MAKE) pypiuploadtest after this ..."
release: distclean alltest testdebversion tag upload pushtag
	@echo "done $@ for version $(HIYAPYCOVERSION)"

all: releasetest pypiuploadtest release
	@echo "done $@ for version $(HIYAPYCOVERSION)"

