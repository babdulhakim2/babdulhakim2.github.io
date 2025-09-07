# Makefile for Jekyll e-Portfolio Site

.PHONY: help install start build clean serve test

# Default target
.DEFAULT_GOAL := help

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	@echo "Installing Ruby gems..."
	bundle install

start:  ## Start the development server (alias for serve)
	@echo "Starting Jekyll development server..."
	bundle exec jekyll serve --livereload --host 0.0.0.0 --port 4000

serve:  ## Start the Jekyll development server
	@echo "Starting Jekyll development server..."
	bundle exec jekyll serve --livereload --host 0.0.0.0 --port 4000

build:  ## Build the site for production
	@echo "Building Jekyll site..."
	bundle exec jekyll build

clean:  ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	bundle exec jekyll clean

test:  ## Test the built site
	@echo "Testing site build..."
	bundle exec jekyll build --verbose

update:  ## Update dependencies
	@echo "Updating Ruby gems..."
	bundle update

draft:  ## Start server with drafts enabled
	@echo "Starting Jekyll with drafts enabled..."
	bundle exec jekyll serve --drafts --livereload --host 0.0.0.0 --port 4000

production-build:  ## Build for production with environment
	@echo "Building for production..."
	JEKYLL_ENV=production bundle exec jekyll build

check-links:  ## Check for broken links (requires htmlproofer gem)
	@echo "Checking for broken links..."
	@if command -v htmlproofer >/dev/null 2>&1; then \
		htmlproofer ./_site --check-html --check-opengraph --report-missing-names --log-level :debug --assume-extension; \
	else \
		echo "htmlproofer not installed. Install with: gem install html-proofer"; \
	fi

open:  ## Open the site in browser (after starting server)
	@echo "Opening site in browser..."
	@sleep 2 && open http://localhost:4000

dev:  ## Start development environment (start + open)
	@echo "Starting development environment..."
	@make start & make open