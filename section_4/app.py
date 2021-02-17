from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "someSecretKeyThatIsNotMeantToDisplayHere"
api = Api(app)

jwt = JWT(app, authenticate, identity)
# it create a new route /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be blank"
    )

    # for the purpose of practice, only the get route require authentication
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        # filter takes two arguements, a function and an iterables
        # eventually filter() returns a filter object, which is an iterable

        # if items are not duplicated, there should only be one object or None in this filter object
        # so, we can use next() to get the item inside the filter object
        # in case there's no object that match the filter and cause the error, we need a argument for the case that
        # nothing match the filter, which is None

        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": f"An item with name {name} already exists"}, 400

        data = Item.parser.parse_args()

        # arguments in get_json method
        # 1. force=True means you don't need to specify the header as content/json
        # 2. silent=True means it doesn't give error, it just five None

        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(debug=True)
