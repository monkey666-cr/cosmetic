import time

from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from commodity.fetch.fetch_sephora import fetch_sephora
from commodity.parser.parse_sephora import parse_sephora
from utils.send_email import send_email
from conf.settings import GOLD_GROUP, RIVE_GROUP, INTERVAL, LETU_GROUP, ILEDEBEAUTE_GROUP, MAX_WORKS, LANCOME_GROUP, \
    CLARINS_GROUP, SEPHORA_GROUP
from commodity.parser.parse_letu_price import parse_letu_price, get_letu_product_status
from commodity.parser.parse_gold_apple_price import parse_price_page_by_json as parse_gold
from commodity.parser.parse_iledebeaute_price import parse_price_page as parse_iledebeaute_price_page
from commodity.fetch.fetch_price import get_gold_apple_price_page, GetRiveGaucheInfo, GetLetuPriceInfo, \
    get_iledebeaute_price_page
from commodity.fetch.fetch_lancome import fetch_lancome
from commodity.parser.parse_lancome import parse_lancome_price_page
from commodity.fetch.fetch_clarins import Clarins

executor = ThreadPoolExecutor(max_workers=MAX_WORKS)
SUCCESS = []  # 获取商品成功发送成功的URL


def _send_email(url, content=None):
    if send_email(url, content):
        SUCCESS.append(url)


def _is_judgment_status(url):
    # 过滤不需要判断status的网站
    no_judgment_status_website = ["www.letu.ru", "shop.rivegauche.ru", "goldapple.ru"]
    for item in no_judgment_status_website:
        if item in url:
            return True
    return False


def start_wrapper(func):
    def inner(url, *args, **kwargs):
        print(f"Crawl URL: {url}")
        result = func(url, *args, **kwargs)
        print(result)

        low_price = kwargs.get("min", 0)
        max_price = kwargs.get("max", 0)
        # 增加判断是否判断库存
        if result and result.get("status") and low_price <= float(
                result.get("low_price", -1)) <= max_price:
            print(f"Product ID: {result.get('product_id')} 可购买，发送邮件。。。。。。")
            _send_email(url, result)

        return result

    return inner


@start_wrapper
def gold_start(url, **kwargs):
    result = parse_gold(url, get_gold_apple_price_page(url))
    return result


@start_wrapper
def rive_start(url, **kwargs):
    rive = GetRiveGaucheInfo(url)
    result = rive()
    return result


@start_wrapper
def letu_start(url, **kwargs):
    letu = GetLetuPriceInfo(url)
    result = parse_letu_price(url, letu.get_letu_price_page())
    result["status"] = get_letu_product_status(letu)
    return result


@start_wrapper
def iledebeaute_start(url, **kwargs):
    return parse_iledebeaute_price_page(url, get_iledebeaute_price_page(url))


@start_wrapper
def lancome_start(url, **kwargs):
    return parse_lancome_price_page(fetch_lancome(url))


@start_wrapper
def clarins_start(url, **kwargs):
    return Clarins()(url)


@start_wrapper
def sephora_start(url, **kwargs):
    try:
        return parse_sephora(fetch_sephora(url), url)
    except Exception as e:
        print(f"sephora: unknown error: {e}")


if __name__ == '__main__':
    while 1:
        all_tasks = [
            executor.submit(gold_start, url, **value) for url, value in GOLD_GROUP.items()
            if url not in SUCCESS
        ]

        all_tasks.extend([
            executor.submit(rive_start, url, **value) for url, value in RIVE_GROUP.items()
            if url not in SUCCESS]
        )

        all_tasks.extend([
            executor.submit(letu_start, url, **value) for url, value in LETU_GROUP.items()
            if url not in SUCCESS]
        )

        all_tasks.extend([
            executor.submit(iledebeaute_start, url, **value) for url, value in ILEDEBEAUTE_GROUP.items()
            if url not in SUCCESS]
        )

        all_tasks.extend([
            executor.submit(lancome_start, url, **value) for url, value in LANCOME_GROUP.items()
            if url not in SUCCESS]
        )

        all_tasks.extend([
            executor.submit(clarins_start, url, **value) for url, value in CLARINS_GROUP.items()
            if url not in SUCCESS]
        )

        all_tasks.extend([
            executor.submit(sephora_start, url, **value) for url, value in SEPHORA_GROUP.items()
            if url not in SUCCESS]
        )

        wait(all_tasks, return_when=ALL_COMPLETED)

        print("=" * 30 + " Run Over " + "=" * 30)

        time.sleep(INTERVAL)
