from flask import Flask, jsonify, request, abort
from flask_restplus import Namespace, Resource, fields
from youtubeapi.models import YoutubeVideo
import http.client


api_namespace = Namespace('api', description='API operations')


#Put argument parser
video_put_args = api_namespace.parser()

video_put_args.add_argument("name", type=str, help="Name of Video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of Video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on Video is required",required=True)

#Patch argument parser
video_update_args = api_namespace.parser()
video_update_args.add_argument("name", type=str, help="Name of Video")
video_update_args.add_argument("views", type=int, help="Views of Video")
video_update_args.add_argument("likes", type=int, help="Likes on Video")



#serializer
model = {
    'id': fields.String(),
    'name': fields.String(),
    'views': fields.Integer(),
    'likes': fields.Integer(),
}

video_model = api_namespace.model('youtubevideo', model)


@api_namespace.route("/v1/videos")
class Videos(Resource):
    @api_namespace.doc('list_videos')
    @api_namespace.marshal_with(video_model)
    def get(self):
        '''
        Retrieves all the videos created by admin
        '''
        videos = YoutubeVideo.objects()
        if not videos:
            abort(404,'No Video in the database')
        return list(videos), 200


@api_namespace.route("/v1/videos/<int:video_id>")
class Video(Resource):
    @api_namespace.doc('create_video')
    @api_namespace.marshal_with(video_model)
    def post(self,video_id):
        '''
        Create a new video
        '''
        args = video_put_args.parse_args()
        video = YoutubeVideo.objects().first()
        if video:
            abort(409, f'Video {video_id} already exists')
            return '', http.client.CONFLICT
        else:
            if args:
                new_video = YoutubeVideo(
                id = video_id,
                name = args['name'],
                likes = args['likes'],
                views =args['views'],).save()
            else:
                return '', http.client.NO_CONTENT
    
        result = api_namespace.marshal(new_video, video_model)
        return args, http.client.CREATED

    @api_namespace.doc('get_video')
    @api_namespace.marshal_with(video_model)
    def get(self, video_id):
        video = YoutubeVideo.objects(id=video_id).first()
        if not video:
            abort(404, f'Video {video_id} not found')
        return video, http.client.OK
        
    @api_namespace.doc('put_video')
    @api_namespace.marshal_with(video_model, code=http.client.OK)    
    def put(self, video_id):
        ''''
        Update a video
        '''
        args = video_put_args.parse_args()
        
        video = YoutubeVideo.objects(id=video_id).first()

        if not video:
            return '', http.client.NOT_FOUND

        video.name = args['name']
        video.likes = args['likes']
        video.views = args['views']

        video.save()
        
        return video, http.client.ACCEPTED

    @api_namespace.doc('delete_video')
    @api_namespace.marshal_with(video_model) 
    def delete(self, video_id):
        video = YoutubeVideo.objects(id=video_id).first()
        if not video:
            abort(404, f'Video {video_id} doesnt exist in the database')
        video.delete()
        return '', http.client.GONE


