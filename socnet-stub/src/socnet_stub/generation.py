from .entities import Base, User, Post, Follow, Like, Comment

from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import logging
import secrets
from random import choices, choice
from collections.abc import Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SocialNetworkStub")


def generate_random_user(_: Engine) -> User:
    token = secrets.token_hex(4)
    return User(
        username=f"user_{token}",
        email=f"user_{token}@example.com",
        nickname=f"User {token}",
        bio=f"Generated test account {token}",
        location="Warsaw",
        website=None,
    )


def generate_random_post(engine: Engine) -> Post | None:
    with Session(engine) as session:
        user_id = session.scalar(select(User.id).order_by(func.random()).limit(1))

    if user_id is None:
        logger.warning("Could not generate a post because no users exist")
        return None

    return Post(
        user_id=user_id,
        content=f"Generated post {secrets.token_urlsafe(16)}",
    )


def generate_random_follow(engine: Engine) -> Follow | None:
    with Session(engine) as session:
        user_pair = session.scalars(
            select(User.id).order_by(func.random()).limit(2)
        ).all()

    if len(user_pair) < 2:
        logger.warning("Could not generate a follow because not enough users exist")
        return None

    return Follow(follower_id=user_pair[0], following_id=user_pair[1])


def generate_random_like(engine: Engine) -> Like | None:
    with Session(engine) as session:
        user_id = session.scalar(select(User.id).order_by(func.random()).limit(1))
        post_id = session.scalar(select(Post.id).order_by(func.random()).limit(1))

    if user_id is None or post_id is None:
        logger.warning("Could not generate a like with no users nor posts")
        return None

    return Like(user_id=user_id, post_id=post_id)


def generate_random_comment(engine: Engine) -> Comment | None:
    with Session(engine) as session:
        user_id = session.scalar(select(User.id).order_by(func.random()).limit(1))
        post_id = session.scalar(select(Post.id).order_by(func.random()).limit(1))

        parent_comment_id = None
        if choice([True, False, False]):
            session.scalar(
                select(Comment.id)
                .where(Comment.post_id == post_id)
                .order_by(func.random())
                .limit(1)
            )

    if user_id is None or post_id is None:
        logger.warning("Could not generate a comment with no users nor posts")
        return None

    return Comment(
        user_id=user_id,
        post_id=post_id,
        parent_comment_id=parent_comment_id,
        content=f"Generated comment {secrets.token_urlsafe(16)}",
    )


__generator_weights = [
    (generate_random_user, 50),
    (generate_random_post, 50),
    (generate_random_follow, 50),
    (generate_random_like, 50),
    (generate_random_comment, 50),
]


def random_generator_dispatch() -> Callable[[Engine], Base | None]:
    return choices(
        population=[g[0] for g in __generator_weights],
        weights=[g[1] for g in __generator_weights],
        k=1,
    )[0]


def insert_entity(engine: Engine, entity: Base) -> None:
    with Session(engine) as session:
        try:
            session.add(entity)
            session.commit()
            session.refresh(entity)
        except IntegrityError as ie:
            logger.warning(
                "Tried adding a row to `%s` which violated table's constraints (%s)",
                entity.__tablename__,
                str(ie.args[0]).partition("\n")[-1],
            )
        else:
            logger.info(
                "Added a row to `%s` with id=%s", entity.__tablename__, entity.id
            )
