import pytest

from commodity.fetch.fetch_price import get_gold_apple_price_page
from commodity.parser.parse_gold_apple_price import parse_price_page_by_json


def test_clarins_fetch():

    url = "https://goldapple.ru/19760321926-genefique-prestige"
    res = parse_price_page_by_json(url, get_gold_apple_price_page(url))
    print(res)
