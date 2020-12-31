from commodity.fetch.fetch_price import GetRiveGaucheInfo
# from commodity.parser.parse_rive_price import RiveParser


def test_rive_req(rive_url_01):
    rive = GetRiveGaucheInfo(rive_url_01)
    rive()


def test_rive_parse(rive_url_01):
    pass
