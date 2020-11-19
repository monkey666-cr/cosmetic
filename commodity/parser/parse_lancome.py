from lxml import etree


def parse_lancome_price_page(text):
    try:
        root = etree.HTML(text)
        product_id = _parse_product_id(root)
        product_name = _parse_product_name(root)
        low_price = _parse_low_price(root)
        price = _parse_price(root)
        status = _parse_product_status(root)

        result = {
            "website": "lancome",
            "product_id": product_id,
            "product_name": product_name,
            "low_price": low_price,
            "price": price,
            "status": status
        }

        return result
    except Exception:
        pass


def _parse_price(element: etree.Element):
    # data-price-amount
    xpath = "//span[contains(@class, 'normal-price')]//span[contains(@id, 'product-price')]"
    try:
        price = element.xpath(xpath)[0].get("data-price-amount")
        price = round(float(price), 2)
        return price
    except Exception as e:
        raise Exception(f"lancome: Parse Price Failed: {str(e)}")


def _parse_low_price(element: etree.Element):
    # attr: data-price-amount
    xpath = "//span[contains(@class, 'group-prices')]//span[contains(@id, 'group-price')]"
    try:
        price = element.xpath(xpath)[0].get("data-price-amount")
        price = round(float(price), 2)
        return price
    except Exception as e:
        raise Exception(f"lancome: Parse Low Price Failed: {str(e)}")


def _parse_product_status(element: etree.Element):
    # attr: class, contains: disabled
    xpath = "//button[contains(@class, 'action primary tocart')]"
    try:
        status = element.xpath(xpath)[0].get("class")
        if "disabled" in status:
            return False
        return True
    except Exception as e:
        raise Exception(f"lancome: Parse Price Failed: {str(e)}")


def _parse_product_id(element: etree.Element):
    # attr: data-product-id
    xpath = "//div[@class='price-box price-final_price']"
    try:
        product_id = element.xpath(xpath)[0].get("data-product-id")
        return product_id
    except Exception as e:
        raise Exception(f"lancome: Parse Price Failed: {str(e)}")


def _parse_product_name(element: etree.Element):
    # attr: text
    xpath = "//h1[@class='page-title']/span"
    try:
        name = element.xpath(xpath)[0].text
        return name
    except Exception as e:
        raise Exception(f"lancome: Parse Price Failed: {str(e)}")
