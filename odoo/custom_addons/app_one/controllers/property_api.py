from odoo import http
from odoo.http import request
import json

class PropertyApi(http.Controller):
    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()  # get the json body
        vals = json.loads(args)                   # convert json to dictionary
        res = request.env['property'].sudo().create(vals)
        if res:
            return request.make_json_response({
                "message": "Property created successfully"
            }, status=200)