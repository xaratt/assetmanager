from flask import Flask
from flask_mongoengine import MongoEngine
from assetmanager import views


app = Flask(__name__)
app.config.from_config("assetmanager.config")

db = MongoEngine(app)

api.add_resource(views.AssetResource, '/asset/<string:title>')
api.add_resource(views.AssetListResource, '/asset')
api.add_resource(views.CreditResource, '/credit/<string:title>')
api.add_resource(views.CreditListResource, '/credit')

if __name__ == '__main__':
    app.run()

