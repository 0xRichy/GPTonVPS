import paramiko
import openai
from flask import Flask, request, jsonify

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
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    return output, error

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Vous pouvez choisir le moteur GPT-3 approprié
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

@app.route('/command', methods=['POST'])
def receive_command():
    command = request.json['command']
    record_command(command)
    output, error = execute_command(command)
    return jsonify({'output': output, 'error': error})

@app.route('/chat', methods=['POST'])
def chat_with_gpt():
    user_input = request.json['input']
    response = generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
