# Makefile
# Set the default Python version to 3.9
PYTHON_VERSION ?= 3.9

# The default target of this Makefile is 'install-poetry'
.PHONY: install-poetry
install-poetry:
	@./scripts/installations/setup.sh $(PYTHON_VERSION) install


