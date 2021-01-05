from commodity.fetch.fetch_price import GetLetuPriceInfo
from commodity.parser.parse_letu_price import parse_letu_price, get_letu_product_status


def test_clarins_fetch():
    url = "https://www.letu.ru/product/clarins-regeneriruyushchaya-omolazhivayushchaya-syvorotka-dlya-kozhi-vokrug-glaz-extra-firming-yeux/73700067"
    letu = GetLetuPriceInfo(url)
    result = parse_letu_price(url, letu.get_letu_price_page())
    result["status"] = get_letu_product_status(letu)
    print(result)