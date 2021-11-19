from flask import Flask, request
from flask_restful import Api, Resource, abort, marshal_with, reqparse, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///sample.db'
db = SQLAlchemy(app)


class VideoModel(db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    views= db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

db.create_all()


video_args = reqparse.RequestParser()
video_args.add_argument("name", type=str, help="Name of Movie", required=True)
video_args.add_argument("views", type=int, help="Views of the Video", required=True)
video_args.add_argument("likes", type=int, help="Likes on the Video", required=True)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of Movie", required=True)
video_update_args.add_argument("views", type=int, help="Views of the Video", required=True)
video_update_args.add_argument("likes", type=int, help="Likes on the Video", required=True)



resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes':fields.Integer

}

class Video(Resource):
    @marshal_with(resource_fields )
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404,message="Video Not Found")
        return result, 200

    def put(self, video_id):
        args = video_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message="Video Id Taken")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return  video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not  result:
            abort(409,message="Video Not Found ")
        if  args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]
        
        db.session.add(result)
        db.session.commit()
        return result, 200


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)


