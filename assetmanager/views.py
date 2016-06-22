from flask_restful import reqparse, Resource, Api, request
from models import Asset, Credit
import json


class AssetResource(Resource):

    def get(self, title):
        asset = Asset.objects.get_or_404(title=title)
        return asset.to_export(), 200

    def put(self, title):
        asset = Asset.objects.get_or_404(title=title)
        data = request.get_json()
        try:
            for field_name, field_value in data.items():
                setattr(asset, field_name, field_value)
            asset.save()
        except Exception as e:
            return {"error": e.message}, 422
        return asset.to_export(), 201

    def delete(self, title):
        asset = Asset.objects.get_or_404(title=title)
        asset.delete()
        return "", 204


class AssetListResource(Resource):

    def get(self):
        order_by = request.args.get("order", "asc")
        order_by_field = "title"
        if "desc" == order_by:
            order_by_field = "-" + order_by_field
        assets_q = Asset.objects.order_by(order_by_field)

        limit = request.args.get("limit", None)
        if limit:
            try:
                limit = int(limit)
            except:
                limit = None

        if limit:
            assets = assets_q.limit(limit)
        else:
            assets = assets_q.all()
        return [asset.to_export() for asset in assets]

    def post(self):
        try:
            asset = Asset(**request.get_json())
            asset.save()
        except Exception as e:
            return {"error": e.message}, 422
        return asset.to_export()


class CreditResource(Resource):

    def get(self, asset_title, role):
        credit = Asset.objects.get_or_404(title=asset_title).credits.filter(role=role)
        if not credit:
            return {"error": "Credit not found"}, 404
        return credit.to_export(), 200

    def put(self, asset_title, role):
        asset = Asset.objects.get_or_404(title=asset_title)
        credit = asset.credits.filter(role=role)[0]
        if not credit:
            return {"error": "Credit not found"}, 404
        data = request.get_json()
        try:
            for field_name, field_value in data.items():
                setattr(credit, field_name, field_value)
            asset.save()
        except Exception as e:
            return {"error": e.message}, 422
        return credit.to_export(), 201

    def delete(self, asset_title, role):
        asset = Asset.objects.get_or_404(title=asset_title)
        credit = asset.credits.filter(role=role)
        if not credit:
            return {"error": "Credit not found"}, 404
        print("XXX", Asset.objects(title=asset_title).update_one(pull__credits__role=role))
        return "", 204


class CreditListResource(Resource):

    def get(self, asset_title):
        asset = Asset.objects.get_or_404(title=asset_title)
        return [credit.to_export() for credit in asset.credits], 200

    def post(self, asset_title):
        asset = Asset.objects.get_or_404(title=asset_title)
        credit = Credit(**request.get_json())
        asset.credits.append(credit)
        try:
            asset.save()
        except Exception as e:
            return {"error": e.message}, 422
        return credit.to_export(), 201

