from ..ticket_client import pad, line, header


def test_pad():
    assert pad("123", 5) == "123  "
    assert pad("This is too long", 5) == "T... "


def test_line():
    assert line("1", "Hello", "Is it me?", "1/1/19", "00:05:20") == \
           "1       Hello                           Is it me?     " \
           "      1/1/19    00:05:20  "


def test_header():
    assert header() == "ID      SUBJECT                         USER" \
                       "                DATE      TIME      "


def test_get_tickets():
    pass


def test_tickets():
    pass


def test_display_ticket():
    pass


def test_integration():
    pass
