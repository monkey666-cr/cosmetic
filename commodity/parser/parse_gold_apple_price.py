"""
解析页面
"""
import re
import json

from lxml import etree


def parse_price_page_by_json(url, text):
    if text is None:
        print(f"Gold Apple: Parse Price Page Failed, text type is None")
        return

    try:
        product_info = re.findall(r"product-form.*?config\": (.*?action.*?}),", text, re.S)[0]
        product_info = json.loads(product_info)
        target_sku = _parse_url_sku(url)
        sku_key = product_info["swatchConfig"]["preset_product_id"]  # product_id or sku_key
        if not target_sku:
            # 多个商品选择规格sku
            if "productSkus" in product_info["swatchConfig"]:
                target_sku = product_info["swatchConfig"]["productSkus"][sku_key]

        if "productSkus" in product_info["swatchConfig"]:
            product_sku = {value: key for key, value in product_info["swatchConfig"]["productSkus"].items()}
            sku_key = product_sku[target_sku]

        product_id = target_sku
        product_name = product_info["defaultImages"][0]["title"]
        price = product_info["swatchConfig"]["optionPrices"][sku_key]["oldPrice"]["amount"]
        low_price = product_info["swatchConfig"]["optionPrices"][sku_key]["finalPrice"]["amount"]
        status = True if sku_key in product_info["swatchConfig"]["salable_products"] else False

        result = {
            "website": "GoldApple",
            "product_id": product_id,
            "product_name": product_name,
            "low_price": low_price,
            "price": price,
            "status": status
        }
        return result

    except Exception as e:
        print(f"Get Gold Price By Json Error: {str(e)}")


def _parse_url_sku(url):
    # 获取目标商品的sku
    try:
        sku = re.findall(r"sku=(\d+)", url)[0]
    except IndexError:
        sku = None

    return sku


def parse_price_page(text):
    """解析商品页面"""
    if text is None:
        print(f"Gold Apple: Parse Price Page Failed, text type is None")
        return
    root = etree.HTML(text)

    try:
        product_id = _get_product_id(root)
        product_name = _get_product_name(root)
        price = _get_product_price(root, product_id)
        old_price = _get_product_old_price(root, product_id)
        status = _get_product_status(root)

        result = {
            "website": "GoldApple",
            "product_id": product_id,
            "product_name": product_name,
            "low_price": price,
            "price": old_price,
            "status": status
        }
        return result
    except Exception as e:
        print(str(e))


def _get_product_id(element: etree.Element):
    """获取商品ID"""
    try:
        product_id = element.xpath("//form[@class='pdp-form pdp__form']/input[@name='product']")[0].get("value")
        if product_id is None:
            raise Exception("Product ID is None")
        return product_id
    except Exception as e:
        raise Exception(f"Gold Apple Get Product ID Failed: {str(e)}")


def _get_product_name(element: etree.Element):
    try:
        product_name = element.xpath('//*[@class="pdp-title__name"]')[0].text
        if product_name is None:
            raise Exception("Product Name is None")
        return product_name
    except Exception as e:
        raise Exception(f"Get Product Name Failed: {str(e)}")


def _get_product_price(element: etree.Element, product_id: str):
    """获取商品价格"""
    try:
        price = element.xpath(f"//form[@class='pdp-form pdp__form']//span[@id='product-price-{product_id}']")[0] \
            .get("data-price-amount")
        if price is None:
            raise Exception("Product Price is None")
        return price
    except Exception as e:
        raise Exception(f"Get Product Price Failed: {str(e)}")


def _get_product_old_price(element: etree.Element, product_id: str):
    """获取商品历史价格"""
    try:
        old_price = element.xpath(f"//form[@class='pdp-form pdp__form']//span[@id='old-price-{product_id}']")[0] \
            .get("data-price-amount")
        if old_price is None:
            raise Exception("Product Price is None")
        return old_price
    except Exception as e:
        raise Exception(f"Get Product Price Failed: {str(e)}")


def _get_product_status(element: etree.Element):
    """获取商品状态，是否有货"""
    status_map = {
        "": False,
        "add-to-cart-button": True
    }
    try:
        product_status = element.xpath("//form[@class='pdp-form pdp__form']//button[@type='submit']")[0] \
            .get("data-role", "")
        if product_status is None:
            raise Exception("Product Status is None")
        return status_map[product_status]
    except Exception as e:
        raise Exception(f"Get Product Price Failed: {str(e)}")


if __name__ == '__main__':
    from commodity.fetch.fetch_price import get_gold_apple_price_page

    url = "https://goldapple.ru/10009-15050100043-abeille-royale#sku=15050100043"
    # url = "https://goldapple.ru/15160100021-la-mousse"
    res = parse_price_page_by_json(get_gold_apple_price_page(url))
    print(res)
