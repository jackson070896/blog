from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.posts.models import Posts


class PostsDAO(BaseDAO):
    model = Posts

    @classmethod
    async def find_all_with_author(cls, session):
        query = (
            select(Posts)
            .options(selectinload(Posts.author))
            .order_by(Posts.created_at.desc())
        )
        result = await session.execute(query)
        return result.scalars().all()
