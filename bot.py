import logging
import requests
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = "6057583176:AAE1tbvoX0ID5_1R8SMZT9dafwzpqZ9tXUY"
API_URL = "http://45.131.40.79:5000"

#logging.basicConfig(
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#    level=logging.INFO
#)


def get_employees():
    response = requests.get(f"{API_URL}/employees")
    if response:
        employees = response.json()
        return "\n".join([f"{employee['id']}, {employee['name']}, {employee['position']}" for employee in employees])


def get_employee(id):
    url = f"{API_URL}/get_employee/{id}"
    response = requests.get(url)
    if response:
        employee = response.json()
        if not "error" in employee:
            return f"{employee['name']}, {employee['position']}"


def add_employee(name, position):
    response = requests.post(f"{API_URL}/add_employee", json={'name': name, 'position': position})
    return response


def update_employee(id, name=None, position=None):
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


async def handle_employees(update, context, args):
    message_body = get_employees()
    if message_body:
        await context.bot.send_message(chat_id=update.message.chat.id, text=message_body)
    else:
        await context.bot.send_message(chat_id=update.message.chat.id,
                                       text='Sorry, something went wrong. Please try again later.')


async def handle_get_employee(update, context, args):
    if len(args) == 1:
        id = args[0]
        msg = get_employee(id)
        if msg:
            await context.bot.send_message(chat_id=update.message.chat.id, text=msg)
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                           text='Sorry, something went wrong. Please try again later.')



async def handle_add_employees(update, context, args):
    if len(args) == 2:
        name, position = args
        if add_employee(name, position):
            await context.bot.send_message(chat_id=update.message.chat.id, text='Employee added successfully.')
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                         text='Sorry, something went wrong. Please try again later.')
    else:
        await context.bot.send_message(chat_id=update.message.chat.id, text='Invalid number of arguments.')


async def handle_update_employees(update, context, args):
    if len(args) == 3:
        id, name, position = args
        if update_employee(id, name, position):
            await context.bot.send_message(chat_id=update.message.chat.id, text='Employee updated successfully.')
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                           text='Sorry, something went wrong. Please try again later.')
    else:
        await context.bot.send_message(chat_id=update.message.chat.id, text='Invalid number of arguments.')


async def handle_delete_employees(update, context, args):
    if len(args) == 1:
        id = args[0]
        if delete_employee(id):
            await context.bot.send_message(chat_id=update.message.chat.id, text='Employee deleted successfully.')
        else:
            await context.bot.send_message(chat_id=update.message.chat.id,
                                           text='Sorry, something went wrong. Please try again later.')

async def handle_request(update, context):
        text = update.message.text.lower().split(' ')
        command, args = text[0], text[1:]

        if command == '/employees':
            await handle_employees(update, context, args)
            pass
        elif command == '/get_employee':
            await handle_get_employee(update, context, args)
            pass
        elif command == '/add_employee':
            await handle_add_employees(update, context, args)
            pass
        elif command == '/update_employee':
            await handle_update_employees(update, context, args)
            pass
        elif command == '/delete_employee':
            await handle_delete_employees(update, context, args)
            pass
        else:
            await context.bot.send_message(chat_id=update.message.chat.id, text='Invalid command.')






def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    api_handler = MessageHandler(filters.TEXT, handle_request)
    application.add_handler(api_handler)


    application.run_polling()

if __name__ == '__main__':
    main()
