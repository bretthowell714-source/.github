.PHONY: help build scrape nmap-inventory nmap-deep shell-scrape shell-recon

help:
	@echo "Targets:"
	@echo "  make build"
	@echo "  make scrape URL=https://example.com ALLOW_HOSTS=example.com"
	@echo "  make nmap-inventory TARGETS=targets/targets.txt"
	@echo "  make nmap-deep TARGETS=targets/targets.txt"
	@echo "  make shell-scrape"
	@echo "  make shell-recon"

build:
	docker compose build

scrape:
	@if [ -z "$(URL)" ]; then echo "ERROR: URL is required. Example: make scrape URL=https://example.com ALLOW_HOSTS=example.com"; exit 2; fi
	docker compose run --rm -e "URL=$(URL)" -e "ALLOW_HOSTS=$(ALLOW_HOSTS)" -e "RENDER=$(RENDER)" scrape

nmap-inventory:
	@if [ -z "$(TARGETS)" ]; then echo "ERROR: TARGETS is required. Example: make nmap-inventory TARGETS=targets/targets.txt"; exit 2; fi
	docker compose run --rm -e "MODE=inventory" -e "TARGETS=$(TARGETS)" recon

nmap-deep:
	@if [ -z "$(TARGETS)" ]; then echo "ERROR: TARGETS is required. Example: make nmap-deep TARGETS=targets/targets.txt"; exit 2; fi
	docker compose run --rm -e "MODE=deep" -e "TARGETS=$(TARGETS)" recon

shell-scrape:
	docker compose run --rm scrape /bin/bash

shell-recon:
	docker compose run --rm recon /bin/bash
