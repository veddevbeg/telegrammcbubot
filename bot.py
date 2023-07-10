import requests
from bs4 import BeautifulSoup
import telebot

# Telegram Bot API token
bot_token = '6101439029:AAHY8tK-HL4WGWGUCKpiZ05VEtDT6WUBFiQ'
# URL of the result page
result_url = 'https://mcbu.ac.in/print_ugmarksheet.php'

# Create a Telegram bot instance
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Send a welcome message to the user
    welcome_message = "Welcome to the Result Bot! Please enter your roll number."
    bot.reply_to(message, welcome_message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    roll_number = message.text.strip()

    # Form data
    form_data = {
        'rtpe': 'Regular',
        'exam_session': 'MAR-2023',
        'exam_name': 'B.COM.FINAL YEAR',
        'rollno': roll_number
    }

    # Send a POST request to the result page
    response = requests.post(result_url, data=form_data)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the student name
    student_name_element = soup.find('td', string='Student Name')
    student_name = student_name_element.find_next('td').b.text.strip()

    # Find the total marks obtained
    marks_obtained_element = soup.find('td', string='Marks Obtained')
    total_marks_obtained = marks_obtained_element.find_next('td').b.text

    # Find the result
    result_element = soup.find('td', string='Result')
    result = result_element.find_next('td').b.text

    # Construct the response message
    response_message = f"Student Name: {student_name}\nTotal Marks Obtained: {total_marks_obtained}\nResult: {result}"

    # Send the response to the user
    bot.reply_to(message, response_message)

# Start the bot
bot.polling()
