import asyncio
from datetime import date

from sqlalchemy import select, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src import Subscribe
from src.database import database
from src.mail import service as mail_service
from src.mail import utils as mail_utils
from src.users.models import User


async def birthdays(session: AsyncSession):
    current_date = date.today()
    mailing: dict = {}

    users = await session.scalars(
        select(User).where(
            and_(
                extract("day", User.birthday) == current_date.day,
                extract("month", User.birthday) == current_date.month,
            )
        )
    )
    users = users.all()

    for user in users:
        subscribes = await session.scalars(
            select(Subscribe)
            .where(Subscribe.following_id == user.id)
            .options(selectinload(Subscribe.follower))
        )
        subscribes = subscribes.all()
        mailing[user.email] = list(map(lambda x: x.follower.email, subscribes))
    await session.close()

    for key, value in mailing.items():
        mail_server = mail_service.get_mail_server()
        mail_service.send_email(
            mail_server=mail_server,
            recipients=value,
            subject=mail_utils.email_subject(
                recipients=key,
                current_date=current_date,
            ),
            text=mail_utils.email_text(
                recipients=key,
                current_date=current_date,
            ),
        )
        mail_service.mail_server_quit(mail_server=mail_server)


if __name__ == "__main__":
    asyncio.run(
        birthdays(
            session=database.get_scoped_session(),
        )
    )
