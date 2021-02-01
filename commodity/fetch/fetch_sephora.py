import requests

from . import REQUEST_TIMEOUT, REQUEST_TRY


def fetch_sephora(url):
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image'
                  '/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    error_msg = ""
    for _ in range(REQUEST_TRY):
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

            return response.text
        except Exception as e:
            error_msg = str(e)
    else:
        raise Exception(f"sephora: fetch {url} error: {error_msg}")


if __name__ == '__main__':
    test_url = "https://sephora.ru/care/face/moisturizer/lancome-absolue-prod6hxx/"
    fetch_sephora(test_url)