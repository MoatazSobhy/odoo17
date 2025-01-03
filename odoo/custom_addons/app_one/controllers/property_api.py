from odoo import http
from odoo.http import request
import json

class PropertyApi(http.Controller):
    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()  # get the json body
        vals = json.loads(args)                   # convert json to dictionary
        if not vals.get('name'):
            return request.make_json_response({
                "message": "Name is required",
            }, status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "Property created successfully",
                    "id": res.id,
                    "name": res.name
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)

    # this is not the best case
    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()  # get the json body
        vals = json.loads(args)  # convert json to dictionary
        res = request.env['property'].sudo().create(vals)
        if res:
            return ({
                "message": "Property created successfully",
            })

