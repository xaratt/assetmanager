import datetime
import time
import assetmanager
from assetmanager import db


class Credit(db.EmbeddedDocument):
    role = db.StringField(max_length=255, required=True)
    value = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def to_export(self):
        data = dict(self.to_mongo())
        data["created_at"] = int(time.mktime(data["created_at"].timetuple()))
        return data

class Asset(db.Document):
    title = db.StringField(max_length=255, required=True, unique=True)
    description = db.StringField(required=True)
    published_at = db.DateTimeField()
    thumbnail = db.StringField(max_length=255, required=True)
    link = db.StringField(max_length=255)
    enclosure = db.StringField(max_length=255)
    media_content = db.StringField(max_length=255)
    credits = db.EmbeddedDocumentListField(Credit)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    def __unicode__(self):
        return self.title

    meta = {
        'indexes': ["title", "credits"],
        'ordering': ["title"]
    }

    def to_export(self):
        data = dict(self.to_mongo())
        data["_id"] = "%s" % data["_id"]
        data["created_at"] = int(time.mktime(data["created_at"].timetuple()))
        if (data.has_key("published_at")):
            data["published_at"] = int(time.mktime(data["published_at"].timetuple()))
        data["credits"] = [credit.to_export() for credit in self.credits]
        return data

