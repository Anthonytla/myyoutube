from flask_restplus import Namespace, Resource, abort
from flask import request
from core.models import User, Token, Video, Comment
from core.extensions import bcrypt, db
from datetime import datetime
from sqlalchemy import exc
from core.schemas import CommentSchema, UserSchema, UserListSchema, CommentListSchema
from marshmallow import ValidationError
from core.auth_utils import token_required

api = Namespace('comment', description='Comment related operations')

@api.route('/video/<int:video_id>/comment')
class CommentResource(Resource):
    @token_required
    def post(self, video_id):
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Not found")
        data = request.get_json()
        comment_input_schema = CommentSchema(only=['body'])
        try:
            comment_data = comment_input_schema.load(data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        if "body" in data:
            body = comment_data["body"]
        else:
            body = ""
        token=Token.query.filter_by(code=request.headers['Authorization']).first()
        comment = Comment(body=body, user_id=token.user_id, video_id=video_id)
        db.session.add(comment)
        db.session.commit()
        comment_output_schema = CommentSchema()
        result = comment_output_schema.dump(comment)
        return {
            "message":"Ok",
            "data": result
        }, 201

@api.route('/video/<int:video_id>/comments')
class CommentListResource(Resource):
    def get(self, video_id):
        video = Video.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Not found")
        data = request.args
        comment_input_schema = CommentListSchema()
        try:
            comment_data = comment_input_schema.load(data)
        except ValidationError as err:
            return {
                "message":"Bad Request",
                "code":400,
                "data":err.messages,
            }, 400
        page, perPage = comment_data['page'], comment_data['perPage']
        comments = Comment.query.filter_by(video_id=video_id).order_by(Comment.id.desc()).paginate(page=page, per_page=perPage, error_out=False)
        
        db.session.commit()
        if not comments.items and page == 1:
            return {
                "message":"Ok",
                "data":[]
            }, 200
        if page > comments.pages:
            abort(400, message="Bad Request")
        comment_output_schema = CommentSchema()
        result = comment_output_schema.dump(comments.items, many=True)
        return {
            "message":"Ok",
            "data":result,
            "pager":{
                "current":page,
                "total":comments.pages
            }
        }, 200
        