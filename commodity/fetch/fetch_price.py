"""
请求获取商品价格
"""
import copy
import json
import re
import time

import requests

from lxml import etree

from commodity.parser.parse_rive_price import RiveParser

REQUEST_TIMEOUT = 40
REQUEST_TRY = 3


def get_gold_apple_price_page(url):
    """获取商品价格"""

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/85.0.4183.121 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }

    for _ in range(REQUEST_TRY):
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                print("response status is 200")
                return response.text
        except Exception as e:
            print(f"Get Gold Apple Price Page Failed: {str(e)}")
            print("Try Again...")


class GetRiveGaucheInfo:
    __website__ = "Rive"

    def __init__(self, start_url):
        self.session = requests.session()
        self.start_url = start_url

        self.headers = {
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

    def get_rive_gauche_price_page(self):
        # 获取价格页面
        print(f"Get Rive Price Page ......")
        for _ in range(REQUEST_TRY):
            try:
                response = self.session.get(self.start_url, headers=self.headers, timeout=REQUEST_TIMEOUT + 40)
                if response.status_code == 200:
                    return response.text
            except Exception as e:
                print(f"Get Rive Gauche Price Page Failed: {str(e)}")
                print("Try Again...")

    def _add_cart(self, product_id):
        # 增加购物车
        print("Rive Add Cart ......")

        url = "https://shop.rivegauche.ru/cart/add"

        data = {
            "productCodePost": product_id,
            "CSRFToken": "ae09a3e6-9be1-4237-9870-822f4c1ca4c3"
        }
        headers = copy.deepcopy(self.headers)
        headers["Referer"] = self.start_url
        headers["Content-Type"] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers["X-Requested-With"] = 'XMLHttpRequest'

        try:
            self.session.post(url, headers=headers, data=data, timeout=REQUEST_TIMEOUT)
        except Exception as e:
            raise Exception(f"Fetch /cart/add Failed: {str(e)}")

    def _product_status(self):
        # 商品状态
        print("Rive Checkout Product status ......")
        url = f"https://shop.rivegauche.ru/cart/rollover/RgMiniCart?_={str(int(time.time() * 1000))}"

        headers = copy.deepcopy(self.headers)
        headers["Referer"] = self.start_url
        headers["X-Requested-With"] = 'XMLHttpRequest'

        try:
            response = self.session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code != 200:
                raise Exception("Fetch product status Response is not 200")
            return response.text
        except Exception as e:
            raise Exception(f"Fetch product status Failed: {str(e)}")

    def __call__(self, *args, **kwargs):
        try:
            price_page = self.get_rive_gauche_price_page()
            if price_page is None:
                raise Exception(f"{self.__website__}: Parse Price Page Failed, text type is None")

            root = etree.HTML(price_page)
            product_id = RiveParser.get_product_id(root)
            product_name = RiveParser.get_product_name(root)
            low_price = RiveParser.get_page_low_price(root)
            price = RiveParser.get_page_price(root)

            result = {
                "website": "Rive",
                "product_id": product_id,
                "product_name": product_name,
                "low_price": low_price,
                "price": price
            }

            # 提交商品至购物车
            self._add_cart(product_id)
            # 检测商品是否可购买
            cart_page = self._product_status()
            status = RiveParser.get_product_status(etree.HTML(cart_page))

            result["status"] = status

            return result
        except Exception as e:
            print(str(e))


class GetLetuPriceInfo:
    def __init__(self, url):
        self.index_url = url

        self.session = requests.session()
        self.session_id = None

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

    def get_index(self):
        """访问首页。获取session id"""
        for _ in range(REQUEST_TRY):
            try:
                response = self.session.get(self.index_url, headers=self.headers, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response.text
                raise Exception(f"Response Is Not 200")
            except Exception as e:
                print(f"Get Letu Index Page (session id) Failed: {str(e)}")

    def get_letu_price_page(self):
        headers = copy.deepcopy(self.headers)
        headers["accept"] = 'application/json, text/javascript, */*; q=0.01'

        for _ in range(REQUEST_TRY):
            try:
                response = self.session.get(self.index_url, headers=headers, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return response.json()
                raise Exception("Get letu Price Response is None")
            except Exception as e:
                print(f"Get letu Price Error: {str(e)}")

    @staticmethod
    def parse_id(url):
        try:
            id_info = re.findall(r"(\d+)/sku/(\d+)", url)[0]
            return id_info[0], id_info[1]
        except IndexError as e:
            raise Exception(f"Parse ID Error: {str(e)}")

    def add_product_to_cart(self):
        """添加商品到购物车"""
        # 1, 从url中解析出 catalogRefIds 和 productId
        product_id, catalog_ref_ids = self.parse_id(self.index_url)

        url = "https://www.letu.ru/rest/model/atg/commerce/order/purchase/CartModifierActor/addItemToOrder"
        headers = copy.deepcopy(self.headers)
        headers["content-type"] = 'application/json; charset=UTF-8'
        data = {
            "catalogRefIds": catalog_ref_ids,
            "productId": product_id,
            "quantity": 1,
            "pushSite": "storeMobileRU",
            "_dynSessConf": self.session_id
        }
        try:
            response = self.session.post(url, headers=headers, data=json.dumps(data), timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            raise Exception(f"Letu Add Product Failed: Response is Not 200")
        except Exception as e:
            print(f"Letu Add Product Error: {str(e)}")

    def get_product_status(self):
        url = "https://www.letu.ru/rest/model/ru/letu/delivery/service/rest/DeliveryInformationActor/orderDelivery-v2"

        data = {"cityId": "8113", "pushSite": "storeMobileRU", "_dynSessConf": self.session_id}
        headers = {
            'authority': 'www.letu.ru',
            'content-type': 'application/json; charset=UTF-8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.183 Safari/537.36',
            'origin': 'https://www.letu.ru',
            'sec-fetch-mode': 'cors',
        }

        for _ in range(REQUEST_TRY):
            try:
                response = self.session.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    return response.json()
                raise Exception("Get Letu Product Status Response Status is Not 200!")
            except Exception as e:
                print(f"Get Letu Product Status Failed: {str(e)}")


def get_iledebeaute_price_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.111 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://iledebeaute.ru/'
    }

    for _ in range(REQUEST_TRY):
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.text
            raise Exception(f"Get iledebeaute Price Page Response is not 200")
        except Exception as e:
            print(f"Get iledebeaute Price Page Failed: {str(e)}")


if __name__ == '__main__':
    url = "https://goldapple.ru/10015-15020300026-double-serum"
    get_gold_apple_price_page(url)
    # url = "https://shop.rivegauche.ru/cart/rollover/RgMiniCart?_=1603801556307"
    # url = "https://shop.rivegauche.ru/product/guerlain-abeille-royale-oil-set-1"
    # url = "https://shop.rivegauche.ru/product/helena-rubinstein-powercell-skinmunity-serum-50"
    # rive = GetRiveGaucheInfo(url)
    # res = rive()
    # print(res)

    # url = "https://www.letu.ru/product/cle-de-peau-beaute-prozrachnaya-rassypchataya-pudra/66500081/sku/80900190?format=json&_=1604065253152"
    # get_letu_price_page(url)

    # url = "https://iledebeaute.ru/shop/care/face/clearning/givenchy-2-clean-to-be-true-prodvhz/"
    # get_iledebeaute_price_page(url)
