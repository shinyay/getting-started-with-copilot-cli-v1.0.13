# Project Scaffolder — Level 9
# Available targets for workshop exercises

.PHONY: list create info clean help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

list:  ## List available templates
	python3 -m scaffolder.cli list

create:  ## Create a project (NAME=myproject TEMPLATE=python)
	python3 -m scaffolder.cli create --name $(NAME) --template $(TEMPLATE)

info:  ## Show template info (TEMPLATE=python)
	python3 -m scaffolder.cli info $(TEMPLATE)

clean:  ## Remove generated output
	rm -rf output/
	rm -f context_summary_*.md

test:  ## Run scaffolder smoke test
	python3 -c "from scaffolder.templates import list_templates; print('Templates:', list_templates())"
