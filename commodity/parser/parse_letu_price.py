import re

from commodity.fetch.fetch_price import GetLetuPriceInfo


def parse_letu_price(url, content):
    # 解析json数据
    if content is None:
        print("Parse letu Price Page Failed: Content is None")
        return

    try:
        _, repository_id = GetLetuPriceInfo.parse_id(url)
        product_content = content["contents"][0]["mainContent"][0]["contents"][0]["productContent"][0]
        sku_info = _select_product(product_content["skuList"], repository_id)
        product = product_content["product"]

        product_id = sku_info["repositoryId"]
        product_name = product["displayName"]
        low_price = sku_info["priceWithMaxDCard"]["amount"]
        price = sku_info["priceWithMaxDCard"]["rawTotalPrice"]
        # status = sku_info["inStock"]
    except KeyError as e:
        raise Exception(f"Letu Json Error: {str(e)}")

    result = {
        "website": "Letu.ru",
        "product_id": product_id,
        "product_name": product_name,
        "low_price": low_price,
        "price": price,
        # "status": status
    }
    return result


def _select_product(sku_list, repository_id):
    """选择商品规格"""
    for item in sku_list:
        if item['repositoryId'] == repository_id:
            return item
    raise Exception("Not Match Target Product")


def get_letu_product_status(letu: GetLetuPriceInfo):
    _get_session_id(letu)
    letu.add_product_to_cart()
    return _get_product_status(letu)


def _get_product_status(letu: GetLetuPriceInfo):
    res = letu.get_product_status()
    try:
        status = res["result"]['shippingGroupInfosMap']['courier']['available']
        return status
    except KeyError:
        raise Exception("Get Letu Product Status Failed")


def _get_session_id(letu: GetLetuPriceInfo):
    res = letu.get_index()
    try:
        session_id = re.findall(r"_dynSessConf.*?(-{0,1}\d+)", res)[0]
        letu.session_id = session_id
    except IndexError as e:
        raise Exception(f"Get Letu Session ID Failed: {str(e)}")


if __name__ == '__main__':
    # url = "https://www.letu.ru/product/lancome-krem-dlya-kozhi-vokrug-glaz-s-effektom-vosstanovleniya-absolue/68700001/sku/83300003"
    # url = "https://www.letu.ru/product/clarins-regeneriruyushchaya-omolazhivayushchaya-syvorotka-dlya-kozhi-vokrug-glaz-extra-firming-yeux/73700067/sku/88200133"
    # url = "https://www.letu.ru/product/ysl-libre/78300050/sku/92600267"
    url = "https://www.letu.ru/product/clarins-kompleksnaya-omolazhivayushchaya-dvoinaya-syvorotka-intensivnogo-deistviya-double-serum/56700001/sku/70600002"
    letu = GetLetuPriceInfo(url)
    content = letu.get_letu_price_page()
    res = parse_letu_price(url, content)
    res["status"] = get_letu_product_status(letu)
    print(res)
