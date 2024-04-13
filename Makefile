SHELL = /bin/bash

PYVERSIONS ?= $(shell py3versions -i)
PYVERSIONSPATHS = $(shell for PV in $(PYVERSIONS); do which $$PV; done)

TESTLOGLEVEL ?= WARN

.PHONY: test examples testinstall all

PYTHONPATH=$(shell pwd)
export PYTHONPATH

HIYAPYCOVERSION=$(shell PYTHONPATH=$(PYTHONPATH)/hiyapyco:$(PYTHONPATH) python -c 'from version import VERSION; print(VERSION)')

export GPGKEY=C9B1F13E67CAB37AE6D132134C2B4A1677DE7FB4

# FIXME: why this hack! w/ -p
DPKGBUILDPKGVERSION = $(shell dpkg-buildpackage --version | sed '1!d;s/^.* //g;s/\.$//g')
DPKGBUILDPKGSIGNARG = $(shell dpkg --compare-versions $DPKGBUILDPKGVERSION lt 1.17.26 && echo "-p'gpg --use-agent'")

pypiupload: PYPIREPO := pypi
pypiupload: PYPIREPOURL := https://pypi.python.org/pypi/HiYaPyCo
pypiuploadtest: PYPIREPO := pypitest
pypiuploadtest: PYPIREPOURL := https://test.pypi.org/project/HiYaPyCo/

quicktest: pylint test examples
# FIXME: testinstallvirtualenv fails due to jinja2 2.8 error w/ python3.2 but works w/ python3.4 ... WTF
alltest: clean quicktest testreadme testinstall testinstallvirtualenv
	@echo "$@ passed"

printversions:
	@echo -e "HIYAPYCOVERSION:\t$(HIYAPYCOVERSION)"
	@echo -e "PYVERSIONS:\t\t$(PYVERSIONS)"
	@echo -e "PYVERSIONSPATHS:\t$(PYVERSIONSPATHS)"

pylint:
	pylint --disable=missing-module-docstring,unused-import,consider-using-with,unspecified-encoding,consider-using-f-string setup.py
	@# FIXME: logging-not-lazy global-statement invalid-name
	@# py3 only: raise-missing-from
	pylint --class-naming-style=any --disable=fixme,pointless-string-statement,missing-module-docstring,unnecessary-pass,logging-not-lazy,global-statement,invalid-name,raise-missing-from,consider-merging-isinstance,too-many-nested-blocks,consider-using-f-string,deprecated-module hiyapyco/__init__.py

testreadme:
	# requires python3-restructuredtext-lint
	rst-lint README.rst

test:
	@RET=0; \
		for p in $(PYVERSIONS); do \
			echo "python version $$p"; \
			for t in test/test_*.py; do \
				$$p -t $$t -l $(TESTLOGLEVEL); \
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
			python -c 'import sys; from hiyapyco import __version__ as HIYAPYCOVERSION; print ("hiyapyco %s" % HIYAPYCOVERSION); print (sys.version)'; \
			make test; \
			make examples; \
			deactivate; \
		done

clean: distclean

distclean:
	python setup.py clean
	rm -rf release dist build HiYaPyCo.egg-info
	find . -type f -name \*.pyc -exec rm -v {} \;

sdist:
	python setup.py sdist
	@echo "$@ done"

wheel:
	# requires a 'sudo pip install wheel'
	python setup.py bdist_wheel
	@echo "$@ done"

twinecheckdist:
	twine check dist/HiYaPyCo-*.tar.gz
	@echo "$@ done"

pypi: sdist wheel twinecheckdist
	@echo "$@ done"
pypiuploadtest: pypi pypiuploaddo
pypiupload: pypi pypiuploaddo
pypiuploaddo: pypi
	# set use-agent in ~/.gnupg/gpg.conf to use the agent
	rm -rf dist/HiYaPyCo-*.egg*
	twine upload --verbose -s -i $(GPGKEY) -r $(PYPIREPO) dist/*
	@echo "test the result at: $(PYPIREPOURL)"

gpg-agent:
	@gpg-agent; \
		RET=$$?; echo "gpg agent running: $$RET"; \
		if [ $$RET -gt 0  ]; then \
			gpg-agent; \
			echo 'please run eval "eval $$(gpg-agent --daemon)"'; \
			exit 1; \
			fi
	gpg-connect-agent 'keyinfo --list' /bye
dch-increment:
	@# use this to increment the deb release number for a existing release
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
debunsigned:
	rm -rf release/deb/build
	mkdir -p release/deb/build
	tar cv -Sp --exclude=dist --exclude=build --exclude='*/.git*' -f - . | ( cd release/deb/build && tar x -Sp -f - )
	cd release/deb/build && dpkg-buildpackage -b --no-sign
	rm -rf release/deb/build
	lintian release/deb/*.deb

deb: gpg-agent
	rm -rf release/deb/build
	mkdir -p release/deb/build
	tar cv -Sp --exclude=dist --exclude=build --exclude='*/.git*' -f - . | ( cd release/deb/build && tar x -Sp -f - )
	cd release/deb/build && dpkg-buildpackage -b -k$(GPGKEY) $(DPKGBUILDPKGSIGNARG)
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
		gpg --clearsign --default-key $(GPGKEY) --use-agent -o InRelease Release && \
		gpg -abs --default-key $(GPGKEY) --use-agent -o Release.gpg Release
	gpg --verify release/deb/Release.gpg release/deb/Release
	gpg --check-sigs InRelease Release

rpm: gpg-agent
	mkdir -p release/rpm/noarch
	python setup.py bdist_rpm --binary-only \
		--doc-files README.rst --requires python-yaml,python-jinja2 \
		-d release/rpm/noarch
	for f in release/rpm/noarch/*.rpm; do \
		echo "rpmsign $f ..."; \
		rm -f $$f.sig; \
		rpmsign \
			-D "%__gpg_sign_cmd  %{__gpg} gpg --batch  --no-armor --use-agent --no-secmem-warning -u '\%{_gpg_name}' -sbo \%{__signature_filename} \%{__plaintext_filename}" \
			-D "%__gpg_check_password_cmd  /bin/true" \
			--resign --key-id=$(GPGKEY) $$f; \
		rpm --checksig --verbose $$f | grep -i $(GPGKEY); \
		echo "rpmsign $f done"; \
		done

rpmrepo: rpm
	cd release/rpm; \
		rm -fv repodata/repomd.xml*; \
		createrepo_c . ; \
		gpg --default-key $(GPGKEY) --use-agent -a --detach-sign repodata/repomd.xml; \
		gpg -a --export $(KEY) > repodata/repomd.xml.key

tag:
	@git pull --rebase --ff-only
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "uncommited changes"; \
		git status --porcelain; \
		false; \
		fi
	@if [ -n "$$(git log --branches --source --not --remotes --no-walk --oneline | awk '{print $2}' | grep \"$$(git branch --show-current)\")" ]; then \
		echo "unpushed changes"; \
		git log --branches --source --not --remotes --no-walk --oneline; \
		false; \
		fi
	git tag -s "release-$(HIYAPYCOVERSION)" -m "version $(HIYAPYCOVERSION) released on $$(date -R)"

pushtag:
	git push origin "release-$(HIYAPYCOVERSION)"

repo: debrepo rpmrepo

upload: uploadrepo pypiupload

uploadrepo: repo
	scp -r release/* repo.zero-sys.net:/srv/www/repo.zero-sys.net/hiyapyco/

testversion: testdebversion testsetupversion
testsetupversion:
	@if $$(dpkg --compare-versions $$(python setup.py -V) lt $(HIYAPYCOVERSION)); then \
		echo "setup.py version must be incremented to HIYAPYCOVERSION $(HIYAPYCOVERSION)"; \
		false; \
		fi

testdebversion:
	@if $$(dpkg --compare-versions $$(dpkg-parsechangelog | sed '/^Version: /!d; s/^Version: \([.0-9]*\).*/\1/g') lt $(HIYAPYCOVERSION)); then \
		echo "debian version must be incremented to HIYAPYCOVERSION $(HIYAPYCOVERSION)"; \
		echo "run make dch --distribution stable --newversion $(HIYAPYCOVERSION)"; \
		false; \
		fi

releasetest: distclean alltest testversion repo pypi
	@echo "$@ done"
	@echo "you may like to run $(MAKE) pypiuploadtest after this ..."
release: distclean alltest testversion tag upload pushtag
	@echo "done $@ for version $(HIYAPYCOVERSION)"

all: releasetest release
	@echo "done $@ for version $(HIYAPYCOVERSION)"

