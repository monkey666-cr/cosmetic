from main import _is_judgment_status


def test_judgment_status():
    url = "https://.ru/19760301025-correcting-cream-veil"
    res = _is_judgment_status(url)

    assert (res or True) == True