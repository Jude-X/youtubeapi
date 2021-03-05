from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource, reqparse
from models import YoutubeVideo

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of Video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of Video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on Video is required",required=True)

app = Flask(__name__)
api = Api(app)



class Videos(Resource):
    def get(self):
        videos = YoutubeVideo.objects()
        if not videos:
            abort(404,'No Video in the database')
        video = []
        for v in videos: 
            video_data = {v.id: {"name": v.name, "likes": v.likes, "views": v.views}}
            video.append(video_data)
        return jsonify(video)

class Video(Resource):
    def get(self, video_id):
        video = YoutubeVideo.objects(id=video_id).get()

        if not video:
            abort(404, f'Video {video_id} not found')

        video_data = {video.id: {"name": video.name, "likes": video.likes, "views": video.views}}
        return jsonify(video_data)
        
    def put(self, video_id):
        args = video_put_args.parse_args()
        try:
            YoutubeVideo(id =  video_id, name = args['name'], likes = args['likes'], views = args['views']).save()
        except:
            abort(409, f'Video {video_id} already exists')
        else:
            return args, 201

    def delete(self, video_id):
        video = YoutubeVideo.objects(id=video_id).first()
        if not video:
            abort(404, f'Video {video_id} doesnt exist in the database')
        video.delete()
        return '', 204

        


        

api.add_resource(Video, "/api/v1/videos/<int:video_id>")

api.add_resource(Videos, "/api/v1/videos")









if __name__ == "__main__":
    app.run(debug=True)


#class HelloWorld(Resource):
#    def get(self, name, test):
#        return jsonify(names[name])
#    
#    def post(self):
#        return jsonify("posted")

#names = {"tim": {"age": 24, "sex": "male"},
#"kaba": {"age": 27, "sex": "male"},
#"bullock": {"age": 29, "sex": "female"}}