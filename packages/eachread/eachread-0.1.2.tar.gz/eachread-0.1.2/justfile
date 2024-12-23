set shell := ["bash", "-uec"]

shell_files := `find . \( -name .git -o -name node_modules -o -name .venv -o -name .ruff_cache \) -prune -o -name "*.sh" -print | tr '\n' ' ' `
py_files := `find . \( -name .git -o -name node_modules -o -name .venv -o -name .ruff_cache \) -prune -o -name "*.py" -print | tr '\n' ' ' `

[group('maint')]
default:
    @just --list

[group('maint')]
pre-commit:
    pre-commit sample-config >.pre-commit-config.yaml
    pre-commit install --config .pre-commit-config.yaml
    git add .pre-commit-config.yaml
    pre-commit run --all-files

[group('maint')]
fmt:
    test -z "{{ py_files }}" || { ruff format .; ruff check --fix; }
    test -z "{{ shell_files }}" || shfmt -w -s -i 4 {{ shell_files }}
    terraform fmt -recursive .
    prettier --ignore-path=.prettierignore --config=.prettierrc.json --write .
    just --unstable --fmt

[group('lint')]
lint:
    test -z "{{ shell_files }}" || shellcheck {{ shell_files }}
