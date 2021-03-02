from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Video(id = {id}, name = {name}, views = {views}, like = {likes})"

# db.create_all() # run once to create database

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type = str, help = "Name of the video is required.", required = True)
video_put_args.add_argument("views", type = str, help = "Views of the video is required.", required = True)
video_put_args.add_argument("likes", type = str, help = "Likes on the video is required.", required = True)

video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument("name", type = str, help = "Name of the video is required.")
video_patch_args.add_argument("views", type = str, help = "Views of the video is required.")
video_patch_args.add_argument("likes", type = str, help = "Likes on the video is required.")


names = {
    "john": {"age": 22, "gender": "male"},
    "jim": {"age": 23, "gender": "male"}
         }

# videos = {}

# def abort_if_video_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, message = f"Video with video_id {video_id} is not valid...")
#     return None

# def abort_if_video_exists(video_id):
#     if video_id in videos:
#         abort(409, message = f"Video with video_id {video_id} already exists...")
#     return None

class HelloWorld(Resource):
    def get(self, name):
        return names[name]  #{"data":f"Hello {name}! Your number is {number}"}
    
    def post(self, name):
        return {"data":"This is a POST"}

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="There is no such video...")
        # abort_if_video_doesnt_exist(video_id)
        return result #videos[video_id]
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="There is no such video...")
        args = video_patch_args.parse_args()
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]

        db.session.commit()
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        # abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id already taken...")
        video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video)
        db.session.commit()
        #videos[video_id] = args
        # print(request.form["likes"])  # Using request module of Python
        return video, 201 #args, 201
    
    def delete(self, video_id):
        abort_if_video_doesnt_exist(video_id)
        videos.pop(video_id, 0)
        return video_id, 204
        
    
api.add_resource(HelloWorld, "/helloworld/<string:name>")  # /<int:number>/<boolean:active>
api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)