from commodity.fetch.fetch_clarins import Clarins


def test_clarins_fetch():
    # url = "https://www.clarins.ru/nabor-sredstv-uhoda--osvezhayushchih-cvet-lica-80072404.html"
    url = "https://www.clarins.ru/regeneriruyushchij-dnevnoj-krem-protiv-morshchin-dlya-suhoj-kozhi-80033511.html"
    clarins = Clarins(url)
    result = clarins()
    print(result)


if __name__ == '__main__':
    test_clarins_fetch()
