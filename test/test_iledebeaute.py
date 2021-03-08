from commodity.fetch.fetch_price import get_iledebeaute_price_page
from commodity.parser.parse_iledebeaute_price import parse_price_page


def test_iledebeaute():
    url = "https://iledebeaute.ru/shop/care/face/anti-age/clarins-double-serum-kompleksnaya-prod5dpq/#store_369305"
    res = parse_price_page(url, get_iledebeaute_price_page(url))
    print(res)
