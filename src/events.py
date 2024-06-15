import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import database
from src.mail import notification as mail_notification


async def birthday_notification_job(session: AsyncSession):
    await mail_notification.birthdays(session=session)


def birthday_notification():
    scheduler = AsyncIOScheduler()
    session: AsyncSession = database.get_scoped_session()
    scheduler.add_job(
        lambda: asyncio.create_task(
            birthday_notification_job(
                session=session,
            )
        ),
        "cron",
        hour=9,
        minute=0,
    )
    scheduler.start()


if __name__ == "__main__":
    birthday_notification()
