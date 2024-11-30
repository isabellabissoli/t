from typing import List
from app.repositories.models import Comment


def get_user_comments(user_id: int) -> List[Comment]:
    return (
        Comment.query
        .order_by(Comment.created_at.desc())
        .filter_by(user_id=user_id)
        .all()
    )