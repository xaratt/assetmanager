import datetime
import assetmanager
from assetmanager import db


class Credit(db.EmbeddedDocument):
    role = db.StringField(max_length=255, required=True)
    value = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

class Asset(db.Document):
    title = db.StringField(max_length=255, required=True)
    description = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    thumbnail = db.StringField(max_length=255, required=True)
    credits = db.ListField(db.EmbeddedDocumentField("Credit"))

    def __unicode__(self):
        return self.title

    meta = {
        'indexes': ["title", "credits"],
        'ordering': ["title"]
    }
