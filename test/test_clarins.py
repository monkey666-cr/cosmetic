from commodity.fetch.fetch_clarins import Clarins


def test_clarins_fetch():
    # url = "https://www.clarins.ru/nabor-sredstv-uhoda--osvezhayushchih-cvet-lica-80072404.html"
    url = "https://www.clarins.ru/creme-solaire-corps-solntsezashchitnyj-krem-dlya-tela-spf-30-80050651.html"
    clarins = Clarins(url)
    result = clarins()
    print(result)


if __name__ == '__main__':
    test_clarins_fetch()
