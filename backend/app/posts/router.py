from fastapi import APIRouter, HTTPException, status

from app.dependencies import CurrentUser, DBSession
from app.posts.dao import PostsDAO
from app.posts.schemas import PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", response_model=list[PostResponse])
async def list_posts(session: DBSession):
    return await PostsDAO.find_all(session)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, session: DBSession):
    post = await PostsDAO.find_one_or_none_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@router.post("/create", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(data: PostCreate, user: CurrentUser, session: DBSession):
    return await PostsDAO.add(
        session, title=data.title, content=data.content, author_id=user.id
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user: CurrentUser, session: DBSession):
    post = await PostsDAO.find_one_or_none_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    if post.author_id != user.id:
        raise HTTPException(status_code=403, detail="Удалять можно только свои посты")
    await session.delete(post)
    await session.commit()
