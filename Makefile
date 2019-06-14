################################################################################
# Makefile for datapath api persist report entity copyrighted
################################################################################

# Prefer bash shell
export SHELL=/bin/bash

## Define repositories dependencies paths

## Make sure of current python path
export PYTHONPATH=$(pwd):./

self := $(abspath $(lastword $(MAKEFILE_LIST)))
parent := $(dir $(self))

ifneq (,$(VERBOSE))
    override VERBOSE:=
else
    override VERBOSE:=@
endif

.PHONY: connect_db
connect_db:
	$(VERBOSE) mongodb $(MONGODB_ARGS) $(DB_NAME)
.PHONY: test
test:
	$(VERBOSE) nosetests ./
.PHONY: smoke
smoke:
	$(VERBOSE) nosetests ./