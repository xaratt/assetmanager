from flask_restful import reqparse, Resource, Api
from models import Asset, Credit

parser = reqparse.RequestParser()


class AssetResource(Resource):

    def get(self, title):
        asset = Asset.objects.get_or_404(title=title)
        return asset

    def put(self, title):
        asset = Asset.objects.get_or_404(title=title)
        args = parser.parse_args()
        for field_name, field_value in args.items():
            setattr(asset, field_name, field_value)
        asset.save()
        return asset, 201

    def delete(self, title):
        asset = Asset.objects.get_or_404(title=title)
        asset.delete()
        return "", 204


class AssetListResource(Resource):

    def get(self):
        args = parser.parse_args()
        order_by = args.get("order", "asc")
        order_by_field = "title"
        if "desc" == order_by:
            order_by_field = "-" + order_by_field
        assets = Asset.objects.order_by(order_by_field).all()
        return assets

    def post(self):
        args = parser.parse_args()
        asset = Asset(**args)
        asset.save()
        return asset
