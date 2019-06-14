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

MONGODB_ARGS:=--username $(DB_USERNAME) --password $(DB_HOST) --host $(DB_HOST) --port $(DB_PORT)

.PHONY: connect_db
connect_db:
	$(VERBOSE) mongodb $(MONGODB_ARGS)
.PHONY: smoke
smoke:
	$(VERBOSE) nosetests ./
.PHONY: run
run:
	$(VERBOSE) source venv/bin/activate
	$(VERBOSE) python datapath_report_api.py
