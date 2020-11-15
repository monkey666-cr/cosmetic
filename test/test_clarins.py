from commodity.fetch.fetch_clarins import Clarins


def test_clarins_fetch():
    url = "https://www.clarins.ru/nabor-sredstv-uhoda--osvezhayushchih-cvet-lica-80072404.html"
    clarins = Clarins(url)
    clarins()


if __name__ == '__main__':
    test_clarins_fetch()
