import paramiko
import openai
from flask import Flask, request, jsonify
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from requests import post

app = Flask(__name__)

# Information for connecting to the VPS
hostname = 'your_vps_ip_or_domain'
port = 22
username = 'your_vps_username'
password = 'your_vps_password'

# GPT-3 API key
openai.api_key = 'your_gpt3_api_key'

# Establish SSH connection
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname, port, username, password)

commands_history = []

def record_command(command):
    commands_history.append(command)

def execute_command(command):
    if command.startswith('http'):
        command = f'curl {command}'
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

@app.route('/command', methods=['POST'])
def receive_command():
    command = request.json['command']
    record_command(command)
    output, error = execute_command(command)
    return jsonify({'output': output, 'error': error})

@app.route('/telegram', methods=['POST'])
def receive_telegram_command():
    command = request.json['command']
    record_command(command)
    output, error = execute_command(command)
    return jsonify({'output': output, 'error': error})

@app.route('/chat', methods=['POST'])
def chat_with_gpt():
    user_input = request.json['input']
    response = generate_response(user_input)
    return jsonify({'response': response})

# Integration with Telegram
def start(update, context):
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id, text="Welcome!")

def receive_telegram_message(update, context):
    user_id = update.effective_user.id
    user_input = update.message.text

    # Send the user input to ChatGPT and get the response
    response = generate_response(user_input)

    # Execute the response as a command on the VPS
    output, error = execute_command(response)

    # Send the output and any error back to the user
    context.bot.send_message(chat_id=user_id, text=output)
    if error:
        context.bot.send_message(chat_id=user_id, text=f"Error: {error}")

if __name__ == '__main__':
    # Start the Flask server
    app.run(host='0.0.0.0', port=8000)

    # Start the Telegram bot
    telegram_token = 'your_telegram_api_token'
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text & ~Filters.command, receive_telegram_message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()
