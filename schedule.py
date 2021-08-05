from datetime import datetime

import aioschedule as schedule

from utils import push_message, get_first_message
from proj.tasks import push_message_at_day


def do_every_seconds(second: int, chat_id):
    schedule.every(second).seconds.do(push_message,
                                      chat=chat_id).tag(str(chat_id))


def do_every_minutes(minute, chat_id):
    schedule.every(minute).minutes.do(push_message,
                                      chat=chat_id).tag(str(chat_id))


def do_every_hours(hour, chat_id):
    schedule.every(hour).hours.do(push_message,
                                  chat=chat_id).tag(str(chat_id))


async def set_frequency_posting(chat_id: int, type_frequency: str, frequency: str):
    schedule.clear(chat_id)
    if type_frequency == 'by_period':
        frequency_list = frequency.split(":")
        frequency_dict = {
            'секунда': do_every_seconds,
            'минута': do_every_minutes,
            'час': do_every_hours
        }
        try:
            frequency_dict[frequency_list[1]](int(frequency_list[0]), chat_id)
        except KeyError:
            return 'Неправильный формат число:тип (без пробелов)'
    if type_frequency == 'by_day':
        if 7 < int(frequency) < 1:
            return "Введенное число должно быть в диапазоне от 1 до 7"
        frequency_dict = {
            '1': schedule.every().monday.do(push_message,
                                            chat=chat_id).tag(str(chat_id)),
            '2': schedule.every().tuesday.do(push_message,
                                             chat=chat_id).tag(str(chat_id)),
            '3': schedule.every().wednesday.do(push_message,
                                               chat=chat_id).tag(str(chat_id)),
            '4': schedule.every().thursday.do(push_message,
                                              chat=chat_id).tag(str(chat_id)),
            '5': schedule.every().friday.do(push_message,
                                            chat=chat_id).tag(str(chat_id)),
            '6': schedule.every().saturday.do(push_message,
                                              chat=chat_id).tag(str(chat_id)),
            '7': schedule.every().sunday.do(push_message,
                                            chat=chat_id).tag(str(chat_id)),
        }
        frequency_dict[frequency]
    if type_frequency == 'by_date':
        try:
            push_message_at_day.apply_async((chat_id, await get_first_message(chat_id)),
                                            eta=datetime.today().replace(month=int(frequency)))
            schedule.every().day.at(frequency).do(push_message,
                                                  chat=chat_id).tag(str(chat_id))
        except ValueError:
            return "День должен быть в диапазоне от 1 до 31"
    return "Постинг настроен"
