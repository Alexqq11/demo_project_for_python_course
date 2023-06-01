import logging
import requests
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TELEGRAM_TOKEN = "6057583176:AAE1tbvoX0ID5_1R8SMZT9dafwzpqZ9tXUY"
API_URL = "http://45.131.40.79:5000"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_employees():
    response = requests.get(f"{API_URL}/employees")
    if response:
        employees = response.json()
        return "\n".join([f"{employee['name']}, {employee['position']}" for employee in employees])


def get_employee(id):
    url = f"{API_URL}/delete_employee/{id}"
    response = requests.get(url)
    if response:
        employee = response.json()
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


def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
