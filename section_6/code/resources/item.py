from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item Deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data["price"])
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})
        connection.close()

        return {"items": items}