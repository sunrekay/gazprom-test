from datetime import date

text_body: str = ""


def email_subject(recipients: list[str], current_date: date) -> str:
    if not recipients:
        return ""

    if len(recipients) == 1:
        return f"Сегодня({current_date}) у вашего друга день рождение!"

    if len(recipients) > 1:
        return f"Сегодня({current_date}) у нескольких ваших друзей день рождения!"


def email_text(recipients: list[str], current_date: date) -> str:
    if not recipients:
        return ""
    return (
        f"Сегодня({current_date}) у нескольких ваших друзей день рождения:\n"
        + "\n".join(
            list(
                map(
                    lambda x: f"{recipients.index(x)+1}) {x}",
                    recipients,
                )
            )
        )
    )
