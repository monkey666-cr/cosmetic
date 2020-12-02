"""
1, 请求首页获取 session
2, 用session提交商品， 数量为3
3, 进入购物车查看商品总价，计算平均价格，即为商品单价
"""
import copy

import requests

from commodity.parser.parse_clarins import ClarinsParser
from commodity.fetch import REQUEST_TRY, REQUEST_TIMEOUT


class Clarins:
    __website__ = "Clarins"

    def __init__(self, url):
        self.index_url = url
        self.headers = {
            'authority': 'www.clarins.ru',
            'sec-ch-ua': '"Chromium";v="86", ""Not\\A;Brand";v="99", "Google Chrome";v="86"',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.183 Safari/537.36',
        }
        self.session = requests.session()
        self.result = dict(website=self.__website__)

    def login(self):
        login_form = ClarinsParser.parse_login_params(
            self._fetch_login_index_page())
        login_url = login_form.pop("url")

        headers = {
            'authority': 'www.clarins.ru',
            'sec-ch-ua': '"Chromium";v="86", ""Not\\A;Brand";v="99", "Google Chrome";v="86"',
            'origin': 'https://www.clarins.ru',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://www.clarins.ru/akkaunt',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        error_msg = ""
        for _ in range(REQUEST_TRY):
            try:
                response = self.session.post(
                    login_url, headers=headers, data=login_form, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response.text
                raise Exception(
                    "Clarins Login Failed: Response Status is not 200")
            except Exception as e:
                error_msg = str(e)
        raise Exception(error_msg)

    def _fetch_login_index_page(self):
        """
        获取登陆的form参数
        """
        login_index_url = "https://www.clarins.ru/akkaunt"

        error_msg = ""
        for _ in range(REQUEST_TRY):
            try:
                response = self.session.get(
                    login_index_url, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response.text
                raise Exception(
                    f"{self.__website__}: Fetch Login Index Page Response Is Not 200")
            except Exception as e:
                error_msg = f"{self.__website__}: Fetch Login index page failed: {str(e)}"
                print(error_msg)

        raise Exception(error_msg)

    def fetch_index_page(self):
        # 访问商品首页
        error_msg = ""
        for _ in range(REQUEST_TRY):
            try:
                response = self.session.get(
                    self.index_url, headers=self.headers, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response.text
                raise Exception(
                    f"{self.__website__}: Fetch Index Page Response Is Not 200")
            except Exception as e:
                error_msg = f"{self.__website__}: Fetch index page failed: {str(e)}"
                print(error_msg)

        raise Exception(error_msg)

    def parse_base_info(self, index_page):
        """
        解析基本信息
        :param index_page:
        :return:
        """
        product_info = ClarinsParser.parse_product_info(index_page)
        product_id = ClarinsParser.parse_product_id(product_info)
        product_sku_code = ClarinsParser.parse_product_sku(product_info)
        product_name = ClarinsParser.parse_product_name(product_info)
        # status = ClarinsParser.parse_product_status(product_info)
        self.result["product_id"] = product_sku_code
        self.result["product_name"] = product_name
        self.result["price"] = product_info.get("unit_price")
        self.result["low_price"] = product_info.get("unit_sale_price")
        self.result["status"] = True if product_info.get("ispackage") == "yes" else False
        return {
            "pid": product_sku_code,
            "pname": product_name,
            "recentlyViewedProductID": product_id,
            "cartAction": "add",
            "Quantity": "3",
            "csrf_token": ClarinsParser.parse_csrf_token(index_page)
        }

    def fetch_add_product_to_cart(self, params):
        # 添加商品到购物车
        url = "https://www.clarins.ru/on/demandware.store/Sites-clarinsru-Site/ru_RU/Cart-AddProduct?format=ajax"
        headers = copy.deepcopy(self.headers)
        headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"

        error_msg = ""
        for _ in range(REQUEST_TRY):
            try:
                response = self.session.post(
                    url, headers=headers, data=params, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response.text
                raise Exception("Response Is Not 200")
            except Exception as e:
                error_msg = f"{self.__website__}: Add Cart Failed: {str(e)}"
        raise Exception(error_msg)

    def fetch_cart(self):
        # 查看购物车
        url = "https://www.clarins.ru/cart"

        error_msg = ""
        for _ in range(REQUEST_TRY):
            try:
                response = self.session.get(
                    url, headers=self.headers, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response.text
                raise Exception("Response Is Not 200")
            except Exception as e:
                error_msg = f"{self.__website__}: Fetch Cart Info Failed: {str(e)}"

        raise Exception(error_msg)

    def parse_price(self, cart_page):
        price = ClarinsParser.parse_price_avg(cart_page)

        self.result["price"] = price
        self.result["low_price"] = price

    def __call__(self, *args, **kwargs):
        try:
            self.login()
            index_page = self.fetch_index_page()
            # 解析基本信息
            add_cart_params = self.parse_base_info(index_page)

            # if not self.result.get("status"):
            #     self.result["price"] = "0"
            #     self.result["low_price"] = "0"
            #     return self.result

            # # 添加购物车
            # self.fetch_add_product_to_cart(add_cart_params)
            # # 查询购物车页面
            # cart_page = self.fetch_cart()
            # # 解析购物车页面，获取价格以及状态
            # self.parse_price(cart_page)

            return self.result
        except Exception as e:
            pass
