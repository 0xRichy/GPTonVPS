import paramiko
import openai
from flask import Flask, request, jsonify
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from requests import post

app = Flask(__name__)

# Informations de connexion au VPS
hostname = 'adresse_ip_ou_nom_de_domaine'
port = 22
username = 'votre_utilisateur'
password = 'votre_mot_de_passe'

# Clé API GPT-3
openai.api_key = 'votre_cle_api_gpt3'

# Établir la connexion SSH
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

# Intégration avec Telegram
def start(update, context):
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id, text="Bienvenue !")

def receive_telegram_message(update, context):
    user_input = update.message.text
    response = generate_response(user_input)
    context.bot.send_message(chat_id=update.effective_user.id, text=response)
    
    # Envoyer la commande à notre serveur Flask pour l'exécuter sur le VPS
    post('http://localhost:8000/telegram', json={'command': user_input})

if __name__ == '__main__':
    # Démarrer le serveur Flask
    app.run(host='0.0.0.0', port=8000)

    # Démarrer le bot Telegram
    telegram_token = 'VOTRE_CLE_API_TELEGRAM'
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    message_handler = MessageHandler(Filters.text & ~Filters.command, receive_telegram_message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()
