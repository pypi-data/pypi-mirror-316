import yamja


def test_load_first():
    results = yamja.load_config('tests/data/merge_first.yaml')
    assert results.lookup('name') == 'first'
    assert results.lookup('id') == 11
    assert results.lookup('tags') == ['first', 'last']


def test_load_second():
    results = yamja.load_config('tests/data/merge_second.yaml')
    assert results.lookup('name') == 'second'
    assert results.lookup('id') == 22
    assert results.lookup('other.name') == 'second_other'
    assert results.lookup('other.id') == 222
