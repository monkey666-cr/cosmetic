from lxml import etree


class RiveParser:
    @staticmethod
    def get_product_id(element: etree.Element):
        try:
            product_id = element.xpath(
                '//input[@name="productCodePost"]')[0].get("value")
            if product_id is None:
                raise Exception("Product ID is None")
            return product_id
        except Exception as e:
            raise Exception(f"Get Product ID Failed: {str(e)}")

    @staticmethod
    def get_page_low_price(element: etree.Element):
        try:
            price = element.xpath(
                '//*[@itemprop="lowPrice"] | //*[contains(@class, "discount-gold_price")]')[0].get("content")
            if not price:
                raise Exception("Low Price is None")
            return price
        except Exception as e:
            raise Exception(f"Get Low Price Failed: {str(e)}")

    @staticmethod
    def get_page_price(element: etree.Element):
        try:
            price = element.xpath('//*[@itemprop="price"]')[-1].get("content")
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
            product_name = element.xpath('//h1')[0].text
            if product_name is None:
                raise Exception("Get Product Name is None")
            return product_name
        except Exception as e:
            raise Exception(f"Get Product Name Failed: {str(e)}")
