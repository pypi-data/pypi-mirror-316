"""Unit-tests for the pprint module."""

from textwrap import dedent

import pytest

from prettyalgo.pprint import PrettyListPrinter


def test_pformat_empty():
    lst = []
    pprint = PrettyListPrinter()
    assert isinstance(pprint.pformat(lst), str)


def test_pformat_wrong_format():
    lst = dict(a="b")
    pprint = PrettyListPrinter()

    with pytest.raises(TypeError):
        pprint.pformat(lst)


def test_pformat_basic_list():
    expected_fragment = dedent(
        """
    +---------------+
    | 0 | 1 | 1 | 3 |
    +---------------+
    """
    )
    lst = [0, 1, 1, 3]
    pprint = PrettyListPrinter()

    ret = pprint.pformat(lst)

    assert isinstance(ret, str)
    assert expected_fragment in ret


def test_pformat_basic_tuple():
    expected_fragment = dedent(
        """
    +---------------+
    | 0 | 1 | 1 | 3 |
    +---------------+
    """
    )
    lst = (0, 1, 1, 3)
    pprint = PrettyListPrinter()

    ret = pprint.pformat(lst)

    assert isinstance(ret, str)
    assert expected_fragment in ret


def test_pformat_basic_str():
    expected_fragment = dedent(
        """
    +---------------+
    | a | b | c | 5 |
    +---------------+
    """
    )
    lst = "abc5"
    pprint = PrettyListPrinter()

    ret = pprint.pformat(lst)

    assert isinstance(ret, str)
    assert expected_fragment in ret


def test_pformat_with_formatting_options():
    expected_fragment = dedent(
        """
    +-----------------------+
    |     |     |     |     |
    |  0  |  1  |  1  |  3  |
    |     |     |     |     |
    +-----------------------+
    """
    )
    lst = [0, 1, 1, 3]
    pprint = PrettyListPrinter(padding=2, v_padding=1, caption="Formatted")

    ret = pprint.pformat(lst)

    assert isinstance(ret, str)
    assert expected_fragment in ret


def test_pformat_with_ptrs_and_vars(capsys):
    expected_fragment = dedent(
        """
    +---------------+
    | 0 | 1 | 1 | 3 |
    +---------------+
    """
    )
    lst = [0, 1, 1, 3]
    pprint = PrettyListPrinter()

    ret = pprint.pformat(
        lst, ptrs=dict(i=0, j=-1), context=dict(count=0, other="thing")
    )

    assert isinstance(ret, str)
    assert expected_fragment in ret


def test_pprint_with_ptrs_and_vars(capsys):
    expected_fragment = dedent(
        """
    +---------------+
    | 0 | 1 | 1 | 3 |
    +---------------+
    """
    )
    lst = [0, 1, 1, 3]
    pprint = PrettyListPrinter()

    pprint.pprint(lst, ptrs=dict(i=0, j=-1), context=dict(count=0, other="thing"))
    captured = capsys.readouterr()

    assert expected_fragment in captured.out
