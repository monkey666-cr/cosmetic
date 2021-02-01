import re
import json

from commodity.fetch.fetch_sephora import fetch_sephora


def parse_sephora(html):
    product_info = _parse_product_json(html)
    product = product_info["product"][0]

    product_id = product["id"]
    product_name = product["product_name"]
    low_price = product["price_show"]
    price = product["price_old_show"]
    status = False if product["s_available"] == "notAvailable" else True

    return {
        "website": "sephora",
        "product_id": product_id,
        "product_name": product_name,
        "low_price": low_price,
        "price": price,
        "status": status
    }


def _parse_product_json(html):
    """提取html文本中的json数据"""
    res = re.findall(r"var TMPCounter.*?;.*?\((.*?)\)", html, re.S)
    if not res:
        raise Exception("sephora: get product json info error")
    return json.loads(res[0])


if __name__ == '__main__':
    test_url = "https://sephora.ru/care/face/moisturizer/lancome-absolue-prod6hxx/"
    page = fetch_sephora(test_url)
    res = parse_sephora(page)
    print(res)
