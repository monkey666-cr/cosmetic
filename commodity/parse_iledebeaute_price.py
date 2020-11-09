import re
import json


def parse_price_page(url, text):
    """解析商品页面"""
    if text is None:
        print("Parse Price Page Failed, text type is None")
        return

    try:
        product_info = re.findall(r"var TMPCounter = (.*?) \|", text)[0]
        product_info = json.loads(product_info)["product"][0]

        sku = _parse_product_sku(url)
        if sku:
            product_info_offer = product_info['offer_list'][sku]
        else:
            product_info_offer = list(product_info['offer_list'].values())[0]
        product_id = product_info_offer.get("id", 0)
        product_name = product_info_offer.get("name", "")
        low_price = product_info_offer.get("price_vip", 0)
        price = product_info_offer.get("price", 0)
        status = _get_product_status(product_info)

        result = {
            "website": "iledebeaute",
            "product_id": product_id,
            "product_name": product_name,
            "low_price": low_price,
            "price": price,
            "status": status
        }
        return result
    except Exception as e:
        print(str(e))


def _parse_product_sku(url):
    sku = re.findall(r"store_(\d+)", url)
    if sku:
        return sku[0]


def _get_product_status(product_info):
    """获取商品状态，是否有货"""
    product_status = product_info.get("s_available")
    if product_status.lower() == "available":
        return True
    return False


if __name__ == '__main__':
    from commodity.fetch_price import get_iledebeaute_price_page

    # url = "https://iledebeaute.ru/shop/care/face/anti-age/guerlain-abeille-royale-double-r-prod6d5e/#store_290624"
    url = "https://iledebeaute.ru/shop/care/face/clearning/estee-lauder-revitalizing-supreme-prod7ttn/"
    res = parse_price_page(url, get_iledebeaute_price_page(url))
    print(res)
