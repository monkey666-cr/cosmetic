import re
import json


def parse_price_page(text):
    """解析商品页面"""
    if text is None:
        print("Parse Price Page Failed, text type is None")
        return

    try:
        product_info = re.findall(r"var TMPCounter = (.*?) \|", text)[0]
        product_info = json.loads(product_info)["product"][0]

        product_id = product_info.get("id", 0)
        product_name = product_info.get("product_name", "")
        low_price = product_info.get("price_vip", 0)
        price = product_info.get("price", 0)
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


def _get_product_status(product_info):
    """获取商品状态，是否有货"""
    product_status = product_info.get("s_available")
    if product_status.lower() == "available":
        return True
    return False


if __name__ == '__main__':
    from commodity.fetch_price import get_iledebeaute_price_page

    url = "https://iledebeaute.ru/shop/care/face/anti-age/helena-rubinstein-re-plasty-age-prodfmb/"
    res = parse_price_page(get_iledebeaute_price_page(url))
    print(res)
