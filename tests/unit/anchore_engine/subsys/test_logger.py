import pytest
from anchore_engine.subsys import logger


class TestSafeFormatter:
    def test_no_args(self):
        result = logger.safe_formatter("message", ())
        assert result == "message"

    def test_multiple_empty_args(self):
        result = logger.safe_formatter("message %s %s", ("", ""))
        assert result == "message  "

    def test_args_to_format_mismatch(self, capsys):
        result = logger.safe_formatter("message %s", ("", ""))
        # exception logger will spit out the traceback, eating up the exception
        out, err = capsys.readouterr()
        assert "not all arguments converted during string formatting" in err
        assert result == "message %s"

    def test_actual_formatting(self):
        result = logger.safe_formatter("message %s, %s", ("first arg", "second arg"))
        assert result == "message first arg, second arg"


@pytest.fixture(scope="class")
def monkeyclass(request):
    """
    This is an unfortunate kludge needed to force the monkeypatch fixture to
    allow a specific scope. In this case we want to monkeypatch always for
    a all the test methods in a class. Without this, Pytest would raise an
    error explaining this is not possible.

    See: https://github.com/pytest-dev/pytest/issues/363

    If this ever stops working, then the `monkeypatch` needs to be done on
    every test method.
    """
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="class")
def log_to_stdout(monkeyclass):
    monkeyclass.setattr(logger, "_log_to_stdout", True)
    monkeyclass.setattr(logger, "log_level", 99)
