from typing import List, Optional

from flask import jsonify, Response

from blog_app.database import Post


def convert_posts_to_json(posts: Optional[List[Post]]) -> Response:
    if (posts is None) or (len(posts) == 0):
        return jsonify([])

    return jsonify([{
        'id': post.id,
        'content': post.content,
        'created_at': post.created_at.isoformat()
    } for post in posts])


def convert_post_to_json(post) -> Response:
    return jsonify({
        'id': post.id,
        'content': post.content,
        'created_at': post.created_at.isoformat()
    })
