import logging
import os

import requests
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

#TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
#API_URL = os.getenv('API_URL')
TELEGRAM_TOKEN = ""
API_URL = "http://45.131.40.79:5000"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_employees():
    """Get a list of all employees"""
    response = requests.get(f"{API_URL}/employees")
    if response.status_code == 200:
        employees = response.json()
        message_body = 'EMPLOYEES:\n'
        for employee in employees:
            message_body += f"{employee['name']}, {employee['position']}\n"
        return message_body


def add_employee(name, position):
    """Add a new employee"""
    response = requests.post(f"{API_URL}/add_employee", json={'name': name, 'position': position})
    return response


def update_employee(id, name=None, position=None):
    """Update an existing employee"""
    url = f"{API_URL}/update_employee/{id}"
    data = {}
    if name:
        data['name'] = name
    if position:
        data['position'] = position
    response = requests.put(url, json=data)
    return response


def delete_employee(id):
    """Delete an employee"""
    url = f"{API_URL}/delete_employee/{id}"
    response = requests.delete(url)
    return response


async def start(update, context):
    await context.bot.send_message(chat_id=update.message.chat.id,
                             text='Welcome to Employee Bot! Use /employees to get a list of all employees.')


async def handle_request(update, context):
    """Parse a request and route it to the appropriate function"""
    text = update.message.text.lower().split(' ')
    command, args = text[0], text[1:]
    if command == '/employees':
        message_body = get_employees()
        if message_body:
            await context.bot.send_message(chat_id=update.message.chat.id, text=message_body)
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                     text='Sorry, something went wrong. Please try again later.')

    elif command == '/add_employee':
        if len(args) == 2:
            name, position = args
            logging.log(logging.INFO, f"called add_employee {name} {position}")
            if add_employee(name, position):
                await context.bot.send_message(chat_id=update.message.chat.id, text='Employee added successfully.')
            else:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                         text='Sorry, something went wrong. Please try again later.')
        else:
            await context.bot.send_message(chat_id=update.message.chat.id, text='Invalid number of arguments.')
    elif command == '/update_employee':
        if len(args) == 3:
            id, name, position = args
            if update_employee(id, name, position):
                await context.bot.send_message(chat_id=update.message.chat.id, text='Employee updated successfully.')
            else:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                         text='Sorry, something went wrong. Please try again later.')
        else:
            await context.bot.send_message(chat_id=update.message.chat.id, text='Invalid number of arguments.')
    elif command == '/delete_employee':
        if len(args) == 1:
            id = args[0]
            if delete_employee(id):
                await context.bot.send_message(chat_id=update.message.chat.id, text='Employee deleted successfully.')
            else:
                await context.bot.send_message(chat_id=update.message.chat.id,
                                         text='Sorry, something went wrong. Please try again later.')
        else:
            await context.bot.send_message(chat_id=update.message.chat.id, text='Invalid number of arguments.')
    else:
        await context.bot.send_message(chat_id=update.message.chat.id, text='Invalid command.')


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT, handle_request))

    application.run_polling()


if __name__ == '__main__':
    main()
