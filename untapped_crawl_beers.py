#!/usr/bin/python
import argparse
import json
import requests

from lxml import html


USER_AGENT = "Mozilla/5.0 (Windows NT 12.0; WOW64) AppleWebKit/" + \
    "537.46 (KHTML, like Gecko) Chrome/47.0.2454.88 Safari/537.46"
HEADERS = {"User-Agent": USER_AGENT}


class UntappdScrapperBeer():
    """UntappdScrapperBeer - get beer stats"""

    def __init__(self, args):
        self._args = args

    def fetch_beer_data(self):
        _beer_stats = []
        for beer_id in self._args.beer_ids:
            _beer_stats.append(
                self._get_beer_stats(beer_id))
        return _beer_stats

    def _get_web_page_from_untapped(self, url):
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print("Error from Untappd: {}".format(str(e)))

    def _get_beer_stats(self, beer_id):
        url = "https://untappd.com/beer/{}".format(beer_id)
        page = self._get_web_page_from_untapped(url)
        return self._parse_beer_stats_page(page, beer_id)

    def _parse_beer_stats_page(self, page, beer_id):
        tree = html.fromstring(page)
        beer_stats = dict(
            id=beer_id,
            abv=tree.find_class("abv")[0].text_content(),
            name=tree.find_class("name")[0].xpath("./h1")[0].text_content(),
            brewery=tree.find_class("brewery")[0].xpath("./a")[0].text_content(),
            descrption=tree.find_class(
                "beer-descrption-read-less")[0].text_content(),
            ibu=tree.find_class("ibu")[0].text_content(),
            rating=tree.find_class("rating")[0].find_class(
                "num")[0].text_content(),
            raters=tree.find_class("raters")[0].text_content(),
            date=tree.find_class("date")[0].text_content(),
        )
        stats_div = tree.find_class("stats")
        for stat in stats_div[0].iterchildren():
            title = stat.find_class("stat")[0].text_content()
            value = stat.find_class("count")[0].text_content()
            beer_stats[title] = value
        return beer_stats


if __name__ == "__main__":
    _parser = argparse.ArgumentParser(description="Untappd beer stats")
    _parser.add_argument("-b", "--beer_ids", required=True,
                         nargs='+', help="Array of beer ids from untappd")
    _parser.add_argument("-o", "--output_file", default=None, help="Output beer data to a json file")
    _args = _parser.parse_args()
    _untappdScrapper = UntappdScrapperBeer(_args)
    beer_data = _untappdScrapper.fetch_beer_data()
    print(beer_data)
    with open(_args.output_file, "w+") as f:
        f.write(json.dumps(beer_data))
