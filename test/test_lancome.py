from commodity.fetch.fetch_lancome import fetch_lancome
from commodity.parser.parse_lancome import parse_lancome_price_page


def test_fetch_lancome():
    url = "https://lancome.ru/absolue-signature-set-x20.html"
    print(fetch_lancome(url))


def test_parse_lancome():
    url = "https://lancome.ru/absolue-setx20.html"
    print(parse_lancome_price_page(fetch_lancome(url)))


if __name__ == '__main__':
    test_parse_lancome()
