# Yamja

WARNING: This is pre-release software.

Yamja is an opinionated library for handling yaml configuration files and jinja2 templates - designed for configuration driven development.

It was created after I've realized that I'm repeating the same pattern in many projects. It's not big (100 lines of code) but it offers a consistent and ergonomic way to handle configuration files.

example usage:
```python
cfg = yamja.load_config("./game_v1.yaml")
character = cfg.lookup('characters.marcus')
game_prompt = cfg.render('game_prompt', character=character)
```


## Features

- Load and merge YAML configuration files
- Use Jinja2 templates within your configuration
- Support for nested configuration lookups using dot notation
- Support for jinja2 macros

## Installation

```bash
pip install yamja
```

## Usage

### Basic Configuration Loading

```python
from yamja import load_config

# Load a single configuration file
config = load_config('config.yaml')

# Access values using dot notation
value = config.lookup('section.subsection.key')

# Access with default value
value = config.lookup('section.subsection.key', default='fallback')
```

### Template Rendering

```yaml
# config.yaml
templates:
  greeting: "Hello {{ name }}!"
```

```python
# Render a template with variables
greeting = config.render('greeting', name='World')
```

### Multiple Configurations

```python
from yamja import load_configs

# Load multiple config files and merge them
configs = load_configs(['config.yaml', 'default.yaml'])
```

### Including Other Config Files

```yaml
# main.yaml
include:
  - common.yaml
  - specific.yaml

additional_settings:
  key: value
```

## Requirements

- Python >= 3.12
- Jinja2 >= 3.1.4
- PyYAML >= 6.0.2

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [GitHub Repository](https://github.com/mobarski/yamja)

