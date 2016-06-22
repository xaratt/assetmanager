from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine


db = MongoEngine()

def create_app(**config):
    from assetmanager import views
    app = Flask(__name__)
    app.config.from_object("assetmanager.config.Config")
    app.config.update(config)

    api = Api(app)
    api.add_resource(views.AssetListResource, '/asset')
    api.add_resource(views.AssetResource, '/asset/<string:title>')
    api.add_resource(views.CreditListResource, '/credit/<string:asset_title>')
    api.add_resource(views.CreditResource, '/credit/<string:asset_title>/<string:role>')

    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()

