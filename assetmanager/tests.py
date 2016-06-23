import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import json
import unittest
from mongoengine import connect
from mongoengine.connection import _get_connection
from flask_testing import TestCase
from assetmanager import create_app
from models import Asset


# also we could use mongomock here
DB_NAME = "assetmanager_testing_%d" % time.time()
CONTENT_TYPE = "application/json"


class AssetTestCase(TestCase):

    def create_app(self):
        config = {
            "MONGODB_SETTINGS": {"DB": DB_NAME},
            "TESTING": True
        }
        return create_app(**config)

    def setUp(self):
        self.client = self.app.test_client()
        Asset.drop_collection()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        super(AssetTestCase, cls).setUpClass()
        connect(DB_NAME)
        _get_connection().drop_database(DB_NAME)

    def test_assets(self):
        resp = self.client.get("/asset")
        # empty list
        self.assertEqual(resp._status_code, 200)
        self.assertEqual(resp.json, [])

        # create 2 assets
        asset_data1 = {
            "title": "asset1",
            "description": "desc 1"
        }
        # try to create asset without required field
        resp = self.client.post("/asset", data=json.dumps(asset_data1),
            content_type = CONTENT_TYPE)
        self.assertEqual(resp._status_code, 422)
        # create first asset
        asset_data1["thumbnail"] = "http://i.telegraph.co.uk/multimedia/archive/02830/cat_2830677b.jpg"
        resp = self.client.post("/asset", data=json.dumps(asset_data1),
            content_type = CONTENT_TYPE)
        self.assertEqual(resp._status_code, 201)
        self.assertEqual(resp.json["title"], asset_data1["title"])
        self.assertEqual(resp.json["description"], asset_data1["description"])
        self.assertEqual(resp.json["thumbnail"], asset_data1["thumbnail"])
        # create second asset
        asset_data2 = {
            "title": "asset2",
            "description": "desc 2",
            "thumbnail": "https://pbs.twimg.com/profile_images/562466745340817408/_nIu8KHX.jpeg"
        }
        resp = self.client.post("/asset", data=json.dumps(asset_data2),
            content_type = CONTENT_TYPE)
        self.assertEqual(resp._status_code, 201)
        self.assertEqual(resp.json["title"], asset_data2["title"])
        # check list size
        resp = self.client.get("/asset")
        self.assertEqual(len(resp.json), 2)
        resp = self.client.get("/asset?limit=1")
        self.assertEqual(len(resp.json), 1)
        # check list order
        resp = self.client.get("/asset?order=asc")
        self.assertEqual(resp.json[0]["title"], asset_data1["title"])
        resp = self.client.get("/asset?order=desc")
        self.assertEqual(resp.json[0]["title"], asset_data2["title"])
        # get asset
        resp = self.client.get("/asset/asset1")
        self.assertEqual(resp._status_code, 200)
        self.assertEqual(resp.json["title"], "asset1")
        #update asset
        resp = self.client.put("/asset/asset1", data=json.dumps({"title":"asset11"}),
            content_type = CONTENT_TYPE)
        self.assertEqual(resp._status_code, 200)
        self.assertEqual(resp.json["title"], "asset11")
        #delete asset and check list
        self.client.delete("/asset/asset11")
        resp = self.client.get("/asset")
        self.assertEqual(len(resp.json), 1)

    def test_credits(self):
        asset_data1 = {
            "title": "asset1",
            "description": "desc 1",
            "thumbnail": "http://i.telegraph.co.uk/multimedia/archive/02830/cat_2830677b.jpg"
        }
        resp = self.client.post("/asset", data=json.dumps(asset_data1),
            content_type = CONTENT_TYPE)
        resp = self.client.get("/credit/asset1")
        # empty credits list
        self.assertEqual(resp._status_code, 200)
        self.assertEqual(resp.json, [])
        # add credits
        credit_data1 = {
            "role": "producer",
            "value": "Producer1"
        }
        resp = self.client.post("/credit/asset1", data=json.dumps(credit_data1),
            content_type = CONTENT_TYPE)
        self.assertEqual(resp._status_code, 201)
        credit_data2 = {
            "role": "director",
            "value": "Director2"
        }
        resp = self.client.post("/credit/asset1", data=json.dumps(credit_data2),
            content_type = CONTENT_TYPE)
        self.assertEqual(resp._status_code, 201)
        # check list
        resp = self.client.get("/credit/asset1")
        self.assertEqual(len(resp.json), 2)
        # update credit
        resp = self.client.put("/credit/asset1/producer", data=json.dumps({"value":"Producer2"}),
            content_type = CONTENT_TYPE)
        self.assertEqual(resp._status_code, 200)
        resp = self.client.get("/credit/asset1/producer")
        self.assertEqual(resp.json["value"], "Producer2")
        # delete credit
        resp = self.client.delete("/credit/asset1/producer")
        self.assertEqual(resp._status_code, 204)
        resp = self.client.get("/credit/asset1")
        self.assertEqual(len(resp.json), 1)

if __name__ == '__main__':
    unittest.main()

