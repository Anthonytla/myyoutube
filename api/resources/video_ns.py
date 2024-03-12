from genericpath import isfile

from urllib.error import HTTPError
from core.schemas import VideoPatchSchema, VideoSchema
from core.auth_utils import token_required
from core.schemas import VideoSchema, VideoListSchema, VideoUpdateSchema
from werkzeug.utils import secure_filename
from flask import request, current_app, jsonify, make_response
from datetime import datetime
from core.extensions import db
from core.models import Video, Token, VideoFormat, User
from uuid import uuid4
from flask_restplus import Namespace, Resource, abort
from core.auth_utils import token_required
from sqlalchemy import exc
from marshmallow import ValidationError
from shutil import copyfile
from pprint import pprint
import requests
import os
import os.path

api = Namespace('video', description='Video related operations')
ALLOWED_EXTENSIONS = {'mp4'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_unique(string):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{string}"

# def with_opencv(filename):
#     import cv2
#     video = cv2.VideoCapture(filename)
#     fps = video.get(cv2.CAP_PROP_FPS)
#     #duration = video.get(cv2.CAP_PROP_POS_MSEC)
#     frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
#     duration = frame_count // fps
#     print(duration // 60, frame_count)
#     return duration, frame_count
def parse_meta_data(filename):
    import ffmpeg
    probe = ffmpeg.probe(filename)
    video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
    time = video_streams[0]['duration']   
    return time, video_streams[0]['height']


@api.route('/user/<int:user_id>/video')
class VideoResource(Resource):
    @token_required
    def post(self, user_id):
        token_code = request.headers['Authorization']
        if "Bearer" in token_code:
            token_code = token_code.split(' ')[1]
        token = Token.query.filter_by(code=token_code).first()
        if token.user_id != user_id:
            abort(401, message="Unauthorized")
        if 'source' not in request.files:
            abort(400, message="Bad Request")
        file = request.files['source']
        if file.filename == '':
            abort(400, message="Not a video")
        if file and allowed_file(file.filename):
            filename = secure_filename(make_unique(file.filename))
            #filePath = os.path.join('/home/laanthony/myYoutube/api/static', filename)
            filePath = os.path.join('/static', filename)
            print(filePath)
            file.save(filePath)
            parse_meta_data(filePath)
            if "name" not in request.form:
                name = "Untitled"
            else:
                name = request.form['name']
            data = {}
            data['name'], data['source'] = name, filePath
            video_validation_schema = VideoSchema(only=('name', 'source'))
            try:
                result = video_validation_schema.load(data)
            except ValidationError as err:
                return {
                    "message":"Bad Request",
                    "code":400,
                    "data":err.messages,
                }, 400
            #time = datetime.strptime(parse_meta_data(filePath)[0], '%H:%M:%S')
            duration = parse_meta_data(filePath)[0]
            #duration = time.second + time.minute * 60 + time.hour * 3600
            video = Video(name=name, user_id=user_id, source=filePath, created_at=datetime.now(), duration=duration, view=0, enabled=1)
            db.session.add(video)
            db.session.commit()
            #-------------------------------------------------------------------------------------#
            # Update elasticsearch data with new user
            elasticsearch_uri = f"http://es01:9200/my_youtube_videos/_create/{video.id}"
            print(elasticsearch_uri)
            try:
                user = User.query.filter_by(id=user_id).first()
                video_es_schema = VideoSchema(exclude=['name', 'user', 'user_id'])
                video_es = video_es_schema.dump(video)
                pprint(video_es)
                #video_es['created_at'] = video_es['created_at'].replace('T', ' ')
                video_es['title'] = video.name
                if video_es['enabled'] == 1:
                    video_es['enabled'] = True
                else:
                    video_es['enabled'] = False
                video_es['user'] = {}
                video_es['user']['id'] = user_id
                video_es['user']['username'] = user.username
                pprint(video_es)
                response = requests.put(elasticsearch_uri, json=video_es)
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                 print(f'Other error occurred: {err}')
            else:
                 print('Success!')
            #------------------------------------------------------------------------#
            video_output_schema = VideoSchema(exclude=['name', 'user_id'])
            result = video_output_schema.dump(video)
            formats = video.video_formats
            format_paths = {format.code: format.uri for format in formats}
            result['formats'] = format_paths
            video = Video.query.filter_by(source=filePath).first()
            pprint(video)
            user = User.query.filter_by(id=user_id).first()
            print("Before")
            return requests.post("http://encodage:8080/myapi/encode", json={"source": filePath, "format": parse_meta_data(filePath)[1], "video_id": video.id, "email": user.email }).text
            #print("after")
            return {
                "message":"Ok",
                "data": result,
            }, 201
        return abort(400, message="Bad Request")

@api.route('/user/<int:user_id>/videos')
class VideoUserListResource(Resource):
    def get(self, user_id):
        input_data = request.args
        input_schema = VideoListSchema(only=["page", "perPage"])
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="Not found")
        try:
            input_data = input_schema.load(input_data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        page, perPage = input_data['page'], input_data['perPage']
        videos = Video.query.filter_by(user_id=user_id).order_by(Video.id.desc()).paginate(page=page, per_page=perPage, error_out=False)
        if not videos.items and page == 1:
            return {
                "message":"Ok",
                "data":[]
            }, 200
        if page > videos.pages:
            abort(400, message="Bad Request")
        video_output_schema = VideoSchema(exclude=['user_id'])
        result = video_output_schema.dump(videos.items, many=True)
        for vid in result:
            formats = VideoFormat.query.filter_by(video_id=vid['id']).all()
            format_paths = {format.code: format.uri for format in formats}
            vid['formats'] = format_paths
        return {
            "message":"Ok",
            "data":result,
            "pager":{
                "current":page,
                "total":videos.pages
            }
        }, 200

@api.route('/videos')
class VideoListResource(Resource):
    def get(self):
        data = request.args
        name, user_id, duration, page, perPage = data.get('name'), data.get('user'), data.get('duration'), request.args.get('page', default=1, type=int), request.args.get('perPage', default=5, type=int)
        videos_input_schema = VideoListSchema()
        try:
            data = videos_input_schema.load(data, partial=True)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        conds = []
        if name:
            conds.append(Video.name == name)
        if user_id:
            conds.append(Video.user_id == user_id)
        if duration:
            conds.append(Video.duration == duration)
        if conds:
            videos = Video.query.filter(*conds).paginate(page=page, per_page=perPage, error_out=False)
        else:
            videos = Video.query.paginate(page=page, per_page=perPage, error_out=False)
        if not videos.items and page == 1:
            return {
                "message":"Ok",
                "data":[]
            }, 200
        if page > videos.pages:
            abort(400, message="Bad Request")
        videos_output_schema = VideoSchema(exclude=['user_id'])
        result = videos_output_schema.dump(videos.items, many=True)
        for vid in result:
            formats = VideoFormat.query.filter_by(video_id=vid['id']).all()
            format_paths = {format.code: format.uri for format in formats}
            vid['formats'] = format_paths
        
        return {
            "message":"Ok",
            "data":result,
            "pager":{
                "current":page,
                "total":videos.pages
            }
        }, 200

@api.route('/video/<int:video_id>')
class VideoPatchResource(Resource):
    def patch(self, video_id):
        data = request.get_json()
        video_input_schema = VideoPatchSchema()
        try:
            data = video_input_schema.load(data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video not found")
        if not os.path.isfile(video.source):
            abort(404, message="Not found")
        meta_datas=parse_meta_data(video.source)
        if "format" not in data:
            resolutions = [1080, 720, 480, 360, 240, 144]
        else :
            resolutions = [data['format']]
        for res in resolutions:
            if res > meta_datas[1]:
                continue
            file_path=os.path.join(current_app.config['UPLOAD_FOLDER'], str(res))
            try:
                os.mkdir(file_path)
            except OSError as error:
                print(error)
            if "file" not in data:
                data['file'] = 'Untitled'
            filename = os.path.join(file_path, make_unique(data['file']))
            
            copyfile(video.source, filename)
            encoded = VideoFormat(code=str(res), uri=filename, video_id=video.id)
            db.session.add(encoded)
            db.session.commit()
        formats = video.video_formats
        format_paths = {format.code: format.uri for format in formats}
        video_output_schema = VideoSchema(exclude=['name', 'user_id'])
        result = video_output_schema.dump(video)
        result['formats'] = format_paths
        return {
                "message":"Ok",
                "data": {
                    "Video": result,
                }
            }, 201

    @token_required
    def put(self, video_id):
        token_code = request.headers['Authorization']
        token = Token.query.filter_by(code=token_code).first()

        data = request.get_json()
        video_input_schema = VideoUpdateSchema()
        try:
            data = video_input_schema.load(data, partial=True)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message='Not found')
        if video.user_id != token.user_id:
            abort(401, message="Unauthorized")
       
        if "name" in data:
            video.name = data['name']
        if "user" in data:
            video.user_id = data['user']
        db.session.commit()
        video_output_schema = VideoSchema(exclude=['name', 'user_id'])
        result = video_output_schema.dump(video)
        return {
                "message":"Ok",
                "data": {
                    "Video": result,
                }
            }, 201

    @token_required
    def delete(self, video_id):
        token_code = request.headers['Authorization']
        if "Bearer" in token_code:
            token_code = token_code.split(' ')[1]
        token = Token.query.filter_by(code=token_code).first()
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Not found")
        if video.user_id != token.user_id:
            abort(401, message="Unauthorized")
        try:
            for format in video.video_formats:
                if not os.path.isfile(format.uri):
                    continue
                video_format = VideoFormat.query.filter_by(uri=format.uri).first()
                os.remove(format.uri)
                db.session.delete(video_format)
                db.session.commit()
        except exc.OperationalError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data": err.orig.args
            }, 400
        if os.path.isfile(video.source):
            os.remove(video.source)
        try:
            db.session.delete(video)
            db.session.commit()
            elasticsearch_uri = f"http://es01:9200/my_youtube_videos/_doc/{video.id}"
            print(elasticsearch_uri)
            try:
                response = requests.delete(elasticsearch_uri)
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                 print(f'Other error occurred: {err}')
            else:
                 print('Success!')
            
        # handles errors related to database unique constraints
        except exc.OperationalError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data": err.orig.args
            }, 400
        return {}, 204

    def get(self, video_id):
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video not found")
        if not os.path.isfile(video.source):
            abort(404, message="Not found")
        formats = video.video_formats
        format_paths = {format.code: format.uri for format in formats}
        video_output_schema = VideoSchema(exclude=['user_id'])
        result = video_output_schema.dump(video)
        result['formats'] = format_paths
        return {
                "message":"Ok",
                "data": {
                    "Video": result,
                }
            }, 200
@api.route("/format/<int:video_id>")
class FormatUpdateResource(Resource):
    def put(self, video_id):
        
        format_data = request.get_json(force=True)
        pprint(format_data)
        video_format = VideoFormat(code=format_data["code"], uri=format_data["uri"], video_id=video_id)
        try:
            db.session.add(video_format)
            db.session.commit()
        # handles errors related to database unique constraints
        except exc.IntegrityError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data": err.orig.args
            }, 400
        
        # if token.user_id != user.id:
        #     user_output_schema = UserSchema(exclude=['password', 'email'])
        return {
            "message":"Ok",
        }, 200