from commodity.fetch.fetch_sephora import fetch_sephora
from commodity.parser.parse_sephora import parse_sephora


def test_sephora():
    test_url_list = [
        "https://sephora.ru/care/face/anti-age/clarins-double-serum-kompleksnaya-prod5dpq/#store_365449"
    ]
    for test_url in test_url_list:
        page = fetch_sephora(test_url)
        res = parse_sephora(page, test_url)
        print(res)
