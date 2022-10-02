from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import requests

# Inspired by Video: https://www.youtube.com/watch?v=GMppyAPbLYk&ab_channel=TechWithTim

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
BASE = "http://127.0.0.1:5000/"

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    page_count = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    progress = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Book(name = {self.name}, type = {self.type}, author = {self.author}, page_count = {self.page_count}, genre = {self.genre}, progress = {self.progress})"


# db.create_all()

book_put_args = reqparse.RequestParser()
book_put_args.add_argument("name", type=str, help="Add book name", required=True)
book_put_args.add_argument("type", type=str, help="Add book type", required=True)
book_put_args.add_argument("author", type=str, help="Add the author's name", required=True)
book_put_args.add_argument("page_count", type=int, help="Add number of pages", required=True)
book_put_args.add_argument("genre", type=str, help="Add the genre", required=True)
book_put_args.add_argument("progress", type=str, help="Add current progress", required=True)

book_patch_args = reqparse.RequestParser()
book_patch_args.add_argument("name", type=str, help="Add book name", required=True)
book_patch_args.add_argument("type", type=str, help="Add book type", required=True)
book_patch_args.add_argument("author", type=str, help="Add the author's name", required=True)
book_patch_args.add_argument("page_count", type=int, help="Add number of pages", required=True)
book_patch_args.add_argument("genre", type=str, help="Add the genre", required=True)
book_patch_args.add_argument("progress", type=str, help="Add current progress", required=True)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String,
    'author': fields.String,
    'page_count': fields.Integer,
    'genre': fields.String,
    'progress': fields.String,
}


class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Unable to locate book with that id")
        return result, 200

    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_put_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if result:
            abort(409, message="book id already in use")

        book = BookModel(id=book_id, name=args['name'], type=args['type'],
                         author=args['author'], page_count=args['page_count'],
                         genre=args['genre'], progress=args['progress'])
        db.session.add(book)
        db.session.commit()
        return book, 201

    @marshal_with(resource_fields)
    def patch(self, book_id):
        args = book_patch_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="book is not in database")

        if args['name']:
            result.name = args['name']
        if args['type']:
            result.type = args['type']
        if args['author']:
            result.author = args['author']
        if args['page_count']:
            result.page_count = args['page_count']
        if args['genre']:
            result.genre = args['genre']
        if args['progress']:
            result.progress = args['progress']

        db.session.commit()

        return result, 202

    def delete(self, book_id):
        book_to_delete = BookModel.query.filter_by(id=book_id).first()
        if not book_to_delete:
            abort(404, message="book id not found...")

        db.session.delete(book_to_delete)
        db.session.commit()
        return 200


def excel_to_db():
    excel_file_path = "data.xlsx"
    df = pd.read_excel(excel_file_path)
    BASE = "http://127.0.0.1:5000/"
    for i in range(len(df.values)):
        data = {"name": df.values[i][1],
                "type": df.values[i][2],
                "author": df.values[i][3],
                "page_count": df.values[i][4],
                "genre": df.values[i][5],
                "progress": df.values[i][6]
                }

        response = requests.put(BASE + "book/" + str(i), data)
        print(response.json())


def create(id, data):
    response = requests.put(BASE + "book/" + id, data)
    return response


def read(id):
    response = requests.get(BASE + "book/" + id)
    return response


def update(id, data):
    response = requests.patch(BASE + "book/" + id, data)
    return response


def delete_(id):
    response = requests.delete(BASE + "book/" + str(id))
    return response


def delete_range(start_id, end_id):
    for i in range(start_id, end_id + 1):
        requests.delete(BASE + "book/" + str(i))


def create_test_case(id):
    data = {"name": "test", "type": "test", "author": "test test", "page_count": 1, "genre": "test",
            "progress": "test"}
    response = requests.put(BASE + "book/" + str(id), data)

# USING CRUD COMMANDS TO MANIPULATE DATABASE
########################################################################################################################

# import requests
#
# BASE = "http://127.0.0.1:5000/"
#
# response = requests.put/patch(BASE + "book/i", data)
# or
# response = requests.get/delete(BASE + "book/i")

# print(response.json())

########################################################################################################################

api.add_resource(Book, "/book/<int:book_id>")

if __name__ == "__main__":
    app.run(debug=True)
