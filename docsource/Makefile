# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = MereLinux
SOURCEDIR     = .
BUILDDIR      = .build
FINALDIR      = ../docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	python generate_from_templates.py
	@chmod +x development/bootstrapping/temptools/mere_temptools_scripts/*.sh
	tar -C development/bootstrapping/temptools -czf \
		development/bootstrapping/temptools/mere_temptools_scripts.tar.gz \
		mere_temptools_scripts
	@$(SPHINXBUILD) -a -W -b $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@rm -rf "$(FINALDIR)"
	@rm -rf "$(BUILDDIR)/.doctrees"
	@rm -rf "$(BUILDDIR)/.buildinfo"
	@mv "$(BUILDDIR)" "$(FINALDIR)"
