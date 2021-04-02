import re

from commodity.fetch.fetch_price import GetLetuPriceInfo


def parse_letu_price(url, content):
    # 解析json数据
    if content is None:
        print("Parse letu Price Page Failed: Content is None")
        return

    try:
        product_content = content["contents"][0]["mainContent"][0]["contents"][0]["productContent"][0]
        try:
            _, repository_id = GetLetuPriceInfo.parse_id(url)
        except Exception:
            repository_id = GetLetuPriceInfo.get_catalog_ref_ids(
                product_content)

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
    return sku_list[0]
    # raise Exception("Not Match Target Product")


def get_letu_product_status(letu: GetLetuPriceInfo):
    letu.set_session_id()
    letu.add_product_to_cart()
    return _get_product_status(letu)


def _get_product_status(letu: GetLetuPriceInfo):
    res = letu.get_product_status()
    try:
        status = res["result"]['shippingGroupInfosMap']['courier']['available']
        return status
    except KeyError:
        raise Exception("Get Letu Product Status Failed")


if __name__ == '__main__':
    url_list = [
        "https://www.letu.ru/product/guerlain-ukreplyayushchii-loson-dlya-litsa-s-matochnym-molochkom-abeille-royale/91300028/sku/102700310",
        "https://www.letu.ru/product/guerlain-syvorotka-dvoinogo-deistviya-abeille-royale-double-r-renew-repair/64500087/sku/79900014",
        "https://www.letu.ru/product/guerlain-lyogkoe-maslo-syvorotka-dlya-litsa-abeille-royale/89700060/sku/100100320",
        "https://www.letu.ru/product/lancome-krem-dlya-kozhi-vokrug-glaz-s-effektom-vosstanovleniya-absolue/68700001/sku/83300003",
        "https://www.letu.ru/product/lancome-intensivnyi-krem-dlya-kozhi-litsa-s-effektom-vosstanovleniya-absolue/68700003",
        "https://www.letu.ru/product/lancome-intensivnyi-krem-dlya-kozhi-litsa-s-effektom-vosstanovleniya-absolue/68700003",
        "https://www.letu.ru/product/lancome-nezhnyi-krem-dlya-kozhi-litsa-s-effektom-vosstanovleniya-absolue/68700004/sku/83300006",
        "https://www.letu.ru/product/clarins-kompleksnaya-omolazhivayushchaya-dvoinaya-syvorotka-intensivnogo-deistviya-double-serum/56700001/sku/70600002",
        "https://www.letu.ru/product/shiseido-nabor-s-lifting-kremom-povyshayushchim-uprugost-kozhi-vokrug-glaz-vital-perfection/91000004/sku/105400004",

    ]
    for url in url_list:
        letu = GetLetuPriceInfo(url)
        result = parse_letu_price(url, letu.get_letu_price_page())
        result["status"] = get_letu_product_status(letu)
        print(result)
