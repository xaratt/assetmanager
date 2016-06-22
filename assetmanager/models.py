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
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    thumbnail = db.StringField(max_length=255, required=True)
    credits = db.EmbeddedDocumentListField(Credit)
    #credits = db.ListField(db.EmbeddedDocumentField("Credit"))
    media = db.ListField(db.StringField(max_length=255))

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
        return data
