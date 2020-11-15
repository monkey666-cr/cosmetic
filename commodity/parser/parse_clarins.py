import re
import json


class ClarinsParser:

    @staticmethod
    def parse_product_info(text) -> dict:
        try:
            product_info_str = re.findall(r"window.universal_variable.product=(.*?)\r\n", text, re.S)[0]
            product_info = json.loads(product_info_str)
            return product_info
        except Exception as e:
            raise Exception(f"Clarins: Parse Product Info Failed: {str(e)}")

    @staticmethod
    def parse_product_id(product_info: dict):
        try:
            product_id = product_info["id"]
            return product_id
        except Exception as e:
            raise Exception(f"Clarins: Parse Product ID Failed: {str(e)}")

    @staticmethod
    def parse_product_name(product_info: dict):
        try:
            name = product_info["name"]
            return name
        except Exception as e:
            raise Exception(f"Clarins: Parse Product Name Failed: {str(e)}")

    @staticmethod
    def parse_product_sku(product_info: dict):
        try:
            sku_code = product_info["sku_code"]
            return sku_code
        except Exception as e:
            raise Exception(f"Clarins: Parse Product Name Failed: {str(e)}")

    @staticmethod
    def parse_csrf_token(text):
        try:
            csrf_token = re.findall(r"CSRFTokenValue\":\"(.*?)\"", text)[0]
            return csrf_token
        except Exception as e:
            raise Exception(f"Clarins: Parse Csrf Token Failed: {str(e)}")

    @staticmethod
    def parse_price_avg(text):
        """解析单价"""
        try:
            pass
        except Exception as e:
            pass

    @staticmethod
    def parse_product_status(text):
        """解析商品状态"""
        try:
            pass
        except Exception as e:
            pass
