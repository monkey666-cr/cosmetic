import requests

from . import REQUEST_TIMEOUT, REQUEST_TRY


def fetch_lancome(url: str) -> str:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    error_msg = ""
    for _ in range(REQUEST_TRY):
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            return response.text
        except Exception as e:
            error_msg = f"Clarins: Fetch Price Page Failed: {str(e)}"
            print(error_msg)
    else:
        raise Exception(error_msg)
