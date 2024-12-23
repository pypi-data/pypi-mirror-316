# eachread

A Python tool for exploring WordNet synsets with a focus on animals and adjectives.

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# Or on Windows:
# .venv\Scripts\activate

# Install dependencies
pip install .
```

## Commands

### wordnet

Analyzes direct animal and physical adjective synsets. This provides first-level hyponyms of "animal" and "physical" synsets.

```bash
eachread wordnet [--limit N]
```

Example output:

```
Found 145 total animal synsets

Example animals:
Words with underscores:
- domestic_cat (domestic cat): small domesticated carnivorous mammal with soft fur
- wild_dog (wild dog): wild member of the dog family Canidae

Single word animals:
- bear: massive plantigrade carnivorous or omnivorous mammals
- lion: large gregarious predatory feline of Africa and India

Found 89 total physical adjective synsets

Example physical adjectives:
- muscular: having a robust muscular body-build characterized by predominance of structures (bone and muscle) developed from the embryonic mesodermal layer
```

### wordnet-deep

Recursively analyzes all animal and physical adjective synsets, going beyond first-level hyponyms to include all descendants.

```bash
eachread wordnet-deep [--limit N]
```

### adjectives

Lists and defines random adjective synsets from WordNet.

```bash
eachread adjectives [--limit N]
```

Example output:

```
Found 21435 total adjective synsets

Example adjectives:
- content: satisfied or showing satisfaction with things as they are
- bright: characterized by quickness and ease in learning
- flexible: capable of being changed or adjusted to meet circumstances
```

### adj-animal

Generates random combinations of adjectives and animals. This can be useful for creative writing, generating character names, or just for fun.

```bash
eachread adj-animal [--limit N]
```

Example output:

```
Generating 5 adjective-animal combinations:
- valiant tiger
- sleepy koala
- mysterious owl
- playful dolphin
- elegant swan
```

#### Special Features

- Use `--limit 0` with `adj-animal` to generate an infinite stream of combinations (press Ctrl+C to stop)
- Filter combinations: `eachread adj-animal --limit 0 | grep -w coot`

## Options

All commands support the following option:

- `--limit N`: Number of examples to show (default: 5)
  - Set to 0 for unlimited examples
  - For `adj-animal`, 0 means infinite generation mode

## Development

The project uses several development tools:

- ruff for Python formatting and linting
- pre-commit for git hooks
- just for command running
- prettier for formatting other file types

To set up the development environment:

```bash
just pre-commit  # Sets up pre-commit hooks
just fmt         # Formats all files
just lint        # Runs linters
```

## Requirements

- Python 3.12.0
- NLTK (WordNet data will be downloaded automatically on first run)
