from flask_script import Command, Option
import feedparser
import mongoengine
from dateutil import parser
from assetmanager.models import Asset, Credit


class RSS(Command):

    option_list = (
        Option("--url", "-u", help="RSS URL", dest="url", required=True),
    )

    def _parse_media_content(self, entry):
        try:
            media_content = entry["media_content"][0]["url"]
        except:
            media_content = None
        return media_content

    def _parse_links(self, entry):
        enclosure = None
        link = None
        for link_data in entry.get("links", []):
            if link_data.get("rel") == "enclosure":
                enclosure = link_data.get("url")
            if link_data.get("rel") == "alternate":
                link = link_data.get("url")
        return enclosure, link

    def _parse_credits(self, entry):
        credits = []
        for credit_data in entry.get("media_credit", []):
            credit = Credit(role=credit_data.get("role"), value=credit_data.get("content"))
            credits.append(credit)
        return credits

    def run(self, url):
        data = feedparser.parse(url)
        for entry in data["entries"]:
            thumbnails = [th.get("url") for th in entry.get("media_thumbnail", [])]
            enclosure, link = self._parse_links(entry)
            asset_data = {
                "title": entry.get("title"),
                "description": entry.get("summary"),
                "published_at": parser.parse(entry.get("published")),
                "thumbnail": thumbnails[0],
                "media_content": self._parse_media_content(entry),
                "enclosure": enclosure,
                "link": link
            }
            asset = Asset(**asset_data)
            asset.credits = self._parse_credits(entry)
            try:
                asset.save()
                print("Added asset %s" % asset)
            except mongoengine.errors.NotUniqueError:
                print("Asset %s already exists, skipped" % asset)
                continue
            except Exception as e:
                print(e.message)
                continue

