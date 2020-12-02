import pytest
import logging

from commodity.fetch.fetch_clarins import Clarins
from commodity.parser.parse_clarins import ClarinsParser


def test_clarins_fetch():
    # url = "https://www.clarins.ru/nabor-sredstv-uhoda--osvezhayushchih-cvet-lica-80072404.html"
    # url = "https://www.clarins.ru/double-serum-kompleksnaya-omolazhivayushchaya-dvojnaya-syvorotka-30ml-80025862.html"
    url = "https://www.clarins.ru/nabor-sredstv-uhoda--osvezhayushchih-cvet-lica-80072404.html"
    clarins = Clarins(url)
    result = clarins()

    print(result)

    assert result.get("website") == "Clarins"
    assert result.get("low_price") == 7650


def test_clarins_parse_login_index_page():
    url = "https://www.clarins.ru/regeneriruyushchij-dnevnoj-krem-protiv-morshchin-dlya-suhoj-kozhi-80033511.html"
    clarins = Clarins(url)
    login_index_page = clarins._fetch_login_index_page()

    assert "Мой профиль" in login_index_page

    login_form = ClarinsParser.parse_login_params(login_index_page)

    assert "dwfrm_login_securekey" in login_form
    assert "url" in login_form
    assert "https://www.clarins.ru/akkaunt?dwcont" in login_form.get("url", "")
    assert "dwfrm_login_password" in login_form
    assert "dwfrm_login_login" in login_form
    assert "dwfrm_login_rememberme" in login_form


def test_clarins_login():
    url = "https://www.clarins.ru/regeneriruyushchij-dnevnoj-krem-protiv-morshchin-dlya-suhoj-kozhi-80033511.html"
    clarins = Clarins(url)
    login_index_page = clarins.login()

    assert "monkey" in login_index_page