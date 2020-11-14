import time

from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from utils.send_email import send_email
from conf.settings import GOLD_GROUP, RIVE_GROUP, INTERVAL, LETU_GROUP, ILEDEBEAUTE_GROUP, MAX_WORKS
from commodity.parser.parse_letu_price import parse_letu_price, get_letu_product_status
from commodity.parser.parse_gold_apple_price import parse_price_page_by_json as parse_gold
from commodity.parser.parse_iledebeaute_price import parse_price_page as parse_iledebeaute_price_page
from commodity.fetch.fetch_price import get_gold_apple_price_page, GetRiveGaucheInfo, GetLetuPriceInfo, \
    get_iledebeaute_price_page

executor = ThreadPoolExecutor(max_workers=MAX_WORKS)
SUCCESS = []  # 获取商品成功发送成功的URL


def _send_email(url, content=None):
    if send_email(url, content):
        SUCCESS.append(url)


def start_wrapper(func):
    def inner(url, *args, **kwargs):
        print(f"Crawl URL: {url}")
        result = func(url, *args, **kwargs)
        print(result)

        low_price = kwargs.get("min", 0)
        max_price = kwargs.get("max", 0)
        if result and result.get("status") and low_price <= float(result.get("low_price", -1)) <= max_price:
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

        wait(all_tasks, return_when=ALL_COMPLETED)

        print("=" * 30 + " Run Over " + "=" * 30)

        time.sleep(INTERVAL)
