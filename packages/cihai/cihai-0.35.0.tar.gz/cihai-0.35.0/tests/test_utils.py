"""Test utilities for cihai."""

import pytest

from cihai import exc, utils
from unihan_etl.util import merge_dict


def test_merge_dict() -> None:
    """Test merge_dict() utility function combines dictionaries recursively."""
    dict1: dict[str, object] = {"hi world": 1, "innerdict": {"hey": 1}}
    dict2: dict[str, object] = {"innerdict": {"welcome": 2}}

    expected = {"hi world": 1, "innerdict": {"hey": 1, "welcome": 2}}

    assert merge_dict(dict1, dict2) == expected


def test_import_string() -> None:
    """Test import_string() resolves strings to modules."""
    utils.import_string("cihai")

    with pytest.raises((ImportError, exc.CihaiException, exc.ImportStringError)):
        utils.import_string("cihai.core.nonexistingimport")

    with pytest.raises((ImportError, exc.CihaiException, exc.ImportStringError)):
        utils.import_string("cihai2")
