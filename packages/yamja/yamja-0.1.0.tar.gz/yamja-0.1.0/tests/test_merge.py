import yamja


def test_merge_empty_configs():
    results = yamja.load_configs([])
    assert results.data == {}


def test_merge_single_config():
    results = yamja.load_configs(['tests/data/merge_first.yaml'])
    assert results.lookup('name') == 'first'
    assert results.lookup('id') == 11
    assert results.lookup('tags') == ['first', 'last']


def test_merge_first_overrides_second():
    """Test that when merging configs, the first config's values override the second's,
    except for nested dictionaries which are merged at the top level."""
    results = yamja.load_configs([
        'tests/data/merge_first.yaml',
        'tests/data/merge_second.yaml',
    ])
    # Simple values from first config override second
    assert results.lookup('name') == 'first'
    assert results.lookup('id') == 11

    # Nested dictionaries are merged
    assert results.lookup('other.name') == 'second_other'
    assert results.lookup('other.id') == 222

    # Lists are preserved from first config
    assert results.lookup('tags') == ['first', 'last']


def test_merge_second_overrides_first():
    """Test that when order is reversed, the second config's values are overridden by the first."""
    results = yamja.load_configs([
        'tests/data/merge_second.yaml',
        'tests/data/merge_first.yaml',
    ])
    # Simple values from first (now second.yaml) are overridden
    assert results.lookup('name') == 'second'
    assert results.lookup('id') == 22

    # Nested dictionaries are still merged
    assert results.lookup('other.name') == 'second_other'
    assert results.lookup('other.id') == 222

    # Lists from first config (now second.yaml) are overridden
    assert results.lookup('tags') == ['first', 'last']


def test_merge_nonexistent_file():
    """Test that nonexistent files are silently ignored during merge."""
    results = yamja.load_configs([
        'tests/data/nonexistent.yaml',
        'tests/data/merge_first.yaml'
    ])
    assert results.lookup('name') == 'first'
    assert results.lookup('id') == 11


def test_merge_macros():
    """Test that macros are properly merged and accessible in templates."""
    results = yamja.load_configs([
        'tests/data/merge_first.yaml',
        'tests/data/merge_macros.yaml'
    ])

    rendered = results.render('example_upper', name='FirsT')
    assert rendered == 'Hello FIRST'

    rendered = results.render('example_lower', name='FirsT')
    assert rendered == 'Hello first'
