import re
import json

from lxml import etree

from conf.settings import CLARINS_PASSWORD, CLARINS_ACCOUNT


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
            root = etree.HTML(text)
            price = root.xpath("//li[@data-auto-id='summary-order-total']//span[@class='value']")[0].text
            price = price.strip().replace(".", "").split(",")[0]
            price = round(float(price) / 3, 2)
            return price
        except Exception as e:
            raise Exception(f"Clarins: Parse Product Price Failed, {str(e)}")

    @staticmethod
    def parse_product_status(product_info: dict):
        """解析商品状态"""
        try:
            status = True if product_info.get("stock", 0) > 0 else False
            return status
        except Exception as e:
            raise Exception(f"Clarins: Parse Product Status Failed, {str(e)}")

    @staticmethod
    def parse_product_status_by_page(product_page: str):
        """解析商品状态"""
        try:
            root = etree.HTML(product_page)
            status_text = root.xpath('//div[contains(@class, "information-section__button-position")]/button')[0].text
            if "Нет в наличии" == status_text.strip():
                return False
            return True
        except Exception as e:
            raise Exception(f"Clarins: Parse Product Status Failed, {str(e)}")

    @staticmethod
    def parse_login_params(login_index_page: str):
        """解析登陆首页的参数"""
        res = dict()
        try:
            root = etree.HTML(login_index_page)
            form = root.xpath('//form[@id="dwfrm_login"]')[0]
            res['url'] = form.get('action')
            res['dwfrm_login_securekey'] = form.xpath('.//input[@name="dwfrm_login_securekey"]')[0].get("value")
            # res[form.xpath('.//input[contains(@name, "dwfrm_login_username")]')[0].get("name")] = CLARINS_ACCOUNT
            res["dwfrm_login_username_d0loteumpbsa"] = CLARINS_ACCOUNT
            res["dwfrm_login_password"] = CLARINS_PASSWORD
            res["dwfrm_login_login"] = "Войти"
            res["dwfrm_login_rememberme"] = "true"
            res["comingfrom"] = "null"
        except Exception as e:
            raise Exception(f"Clarins: Parse Login Index Failed, {str(e)}")

        return res