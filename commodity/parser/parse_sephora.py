import re
import json

from commodity.fetch.fetch_sephora import fetch_sephora


def parse_sephora(html, url):
    product_info = _parse_product_json(html)
    product = product_info["product"][0]

    target_id = _parse_target_id_from_url(url)
    if not target_id:
        target_id = product["offer_id_used"]

    product_id = product["id"]
    product_name = product["product_name"]
    low_price = product["offer_list"][target_id]["price_vip"]
    price = product["offer_list"][target_id]["price_single"]
    status = False if product["offer_list"][target_id]["b_available"] == 0 else True

    return {
        "website": "sephora",
        "product_id": product_id,
        "product_name": product_name,
        "low_price": low_price,
        "price": price,
        "status": status
    }


def _parse_target_id_from_url(url):
    id_list = re.findall(r"store_(\d+)", url)
    if id_list:
        return id_list[0]


def _parse_product_json(html):
    """提取html文本中的json数据"""
    res = re.findall(r"var TMPCounter.*?;.*?\((.*?)\)", html, re.S)
    if not res:
        raise Exception("sephora: get product json info error")
    return json.loads(res[0])


if __name__ == '__main__':
    test_url_list = [
        "https://sephora.ru/care/face/anti-age/helena-rubinstein-re-plasty-age-prodfmb/#store_20244",
        "https://sephora.ru/care/face/anti-age/lancome-absolue-prod6i3k/#store_296865",
        "https://sephora.ru/care/face/anti-age/guerlain-abeille-royale-prod5c52/#store_235769",
        "https://sephora.ru/care/face/moisturizer/guerlain-abeille-royale-prod7nqx/",
    ]
    for test_url in test_url_list:
        page = fetch_sephora(test_url)
        res = parse_sephora(page, test_url)
        print(res)
