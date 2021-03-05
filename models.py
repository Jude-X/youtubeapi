from mongoengine import *

connect("project2")

class YoutubeVideo(Document):
    id = IntField(primary_key=True)
    name = StringField(unique=True, required=True)
    likes = IntField()
    views = IntField()