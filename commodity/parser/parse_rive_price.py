import re

from lxml import etree


class RiveParser:
    @staticmethod
    def get_product_id(element: etree.Element):
        try:
            product_id = element.xpath(
                "//div[contains(@class, 'product-code')]")[0].text
            if product_id is None:
                raise Exception("Product ID is None")
            product_id = product_id.split()[-1]
            return product_id
        except Exception as e:
            raise Exception(f"Get Product ID Failed: {str(e)}")

    @staticmethod
    def get_page_low_price(element: etree.Element):
        try:
            price = element.xpath("//div[@itemprop='price']")[0].get("content")
            if not price:
                raise Exception("Low Price is None")
            return price
        except Exception as e:
            raise Exception(f"Get Low Price Failed: {str(e)}")

    @staticmethod
    def get_page_price(element: etree.Element):
        try:
            price = element.xpath("//div[@itemprop='price']")[-1].get("content")
            if not price:
                raise Exception("Price is None")
            return price
        except Exception as e:
            raise Exception(f"Get Price Failed: {str(e)}")

    @staticmethod
    def get_product_status(element: etree.Element):
        try:
            class_attr = element.xpath(
                '//div[@class="links"]//a')[0].get("class")
            if "green" in class_attr:
                return True
            return False
        except Exception as e:
            raise Exception(f"Parse Product status Failed: {str(e)}")

    @staticmethod
    def get_product_name(element: etree.Element):
        try:
            product_name = element.xpath(
                '//h1[contains(@class, "product-name")]')[0]
            if product_name is None:
                raise Exception("Get Product Name is None")
            product_name = etree.tostring(product_name)
            product_name = str(product_name, encoding='utf-8')
            product_name = re.findall(r'/>(.*?)</h1>', product_name)[0].strip()
            return product_name
        except Exception as e:
            raise Exception(f"Get Product Name Failed: {str(e)}")
