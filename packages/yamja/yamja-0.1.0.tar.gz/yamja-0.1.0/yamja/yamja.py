import os

import yaml
import jinja2


class Config:
    def __init__(self, data: dict):
        loader = jinja2.DictLoader(data.get('templates', {}))
        self.jinja2_env = jinja2.Environment(loader=loader)
        self.data = data

    def __repr__(self):
        return f'Config({self.data})'

    def lookup(self, key, default=...):
        return lookup(self.data, key, default)

    def render(self, key, **kwargs):
        text = self.lookup('templates.'+key)
        if not text:
            raise KeyError(f'Template {key} not found or not a string')
        if 'macros' in self.data:
            macros_str = ''.join(self.data['macros'].values())
            self.data['templates']['macros'] = macros_str  # add macros to the loader
            header = "{% import 'macros' as macro %}"
            text = header + text
        template = self.jinja2_env.from_string(text)
        return template.render(**kwargs)


def load_config(path) -> Config:
    with open(path, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader) or {}
    cfg = handle_include(cfg, path)
    return Config(cfg)


def load_configs(paths: list[str]) -> Config:
    configs = [load_config(path) for path in paths if os.path.exists(path)]
    return merge_configs(configs)


def merge_configs(configs: list[Config]) -> Config:
    """Merge configs; later configs are overridden by earlier configs;
    top level dictionaries are merged, other values are overridden"""
    result = {}
    for config in reversed(configs):
        if config.data:
            for k, v in config.data.items():
                if isinstance(v, dict) and k in result and isinstance(result[k], dict):
                    result[k].update(v)
                else:
                    result[k] = v
    return Config(result)


def handle_include(cfg, path):
    if not isinstance(cfg, dict) or 'include' not in cfg:
        return cfg

    for include in cfg['include']:
        include_path = os.path.join(os.path.dirname(path), include)
        chunk = load_config(include_path).data
        if not isinstance(chunk, dict):
            continue
        # merge top level
        for k in cfg:
            # local values override included values
            if k != 'include':  # skip the include key itself
                if k not in chunk:
                    chunk[k] = cfg[k]
                elif isinstance(cfg[k], dict) and isinstance(chunk[k], dict):
                    # only update if both values are dictionaries
                    chunk[k].update(cfg[k])
                else:
                    # for non-dict values, local values override included values
                    chunk[k] = cfg[k]
        cfg = chunk

    if 'include' in cfg:
        del cfg['include']
    return cfg


def lookup(data, key, default=...):
    """Look up a value in nested data structures using dot notation."""
    current = data

    for part in key.split('.'):
        try:
            # Handle both positive and negative indices
            if part.lstrip('-').isdigit():
                current = current[int(part)]
            elif hasattr(current, '__getitem__'):
                current = current[part]
            else:
                current = getattr(current, part)
        except (KeyError, IndexError, AttributeError):
            if default is ...:
                raise KeyError(key)
            return default
    return current
