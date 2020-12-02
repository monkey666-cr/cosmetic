
def test_load_settings():
    from conf.settings import CLARINS_ACCOUNT, CLARINS_PASSWORD

    assert CLARINS_PASSWORD != ""
    assert CLARINS_PASSWORD != ""