from flask import render_template, make_response, redirect, request, flash, url_for, jsonify, escape
import pathlib
import time
import datetime
from dataclasses import dataclass
from app import app
import humanize

token = pathlib.Path('.token').read_text().strip()

@dataclass
class State:
    hostname: str
    ip: str = ""
    ssid: str = ""
    timestamp: int = 0
    stay_alive: int = 310

    def reset(self) -> None:
        self.ip = ""
        self.ssid = ""
        self.timestamp = 0

    def last_seen(self) -> str:
        if not self.timestamp or not self.ip:
            return ""
        delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(self.timestamp)
        if delta.total_seconds() < self.stay_alive:
            return f"Online ({humanize.naturaltime(delta)})"
        return "Offline (last seen {humanize.naturaltime(delta)})"

    def emoji(self) -> str:
        if not self.timestamp or not self.ip:
            return "⚪"
        delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(self.timestamp)
        if delta.total_seconds() < self.stay_alive:
            return f"🟢"
        return "🔴"

    def color(self) -> str:
        if not self.timestamp or not self.ip:
            return "#FFFFFF"
        delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(self.timestamp)
        if delta.total_seconds() < self.stay_alive:
            return f"#90EE90"
        return "#FFCCCB"

    def network_info(self) -> str:
        if not self.ip:
            return f"{self.emoji()}    Pi-Connect is online, but no Pi has connected to it"
        return f"{self.emoji()}    {self.hostname} is connected to '{self.ssid}' and has the IP address {self.ip}"

state = State("Raspberry Pi")

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", network_info=state.network_info(), last_seen=state.last_seen(), background_color=state.color())

@app.route("/reset", methods=["GET", "POST"])
def reset():
    state.reset()
    return redirect(url_for('index'), 200)

@app.route("/", methods=['POST'])
def update_site():
    headers = request.headers
    auth = headers.get("Authorization")
    if auth != token:
        return make_response(jsonify({"success": False}), 401)

    data = request.get_json(force=True)
    if data:
        state.hostname = data.get('hostname')
        state.ip = data.get('ip')
        state.ssid = data.get('ssid')
        state.timestamp = int(time.time())
        return make_response(jsonify({"success": True}), 200)
    return make_response(jsonify({"success": False}), 400)

@app.route("/ping", methods=['POST'])
def ping():
    global storage
    headers = request.headers
    auth = headers.get("Authorization")
    if auth != token:
        return make_response(jsonify({"success": False}), 401)

    state.timestamp = int(time.time())
    return make_response(jsonify({"success": True}), 200)


@app.route("/connect")
def connect():
    if state.ip:
        return redirect(f"http://{state.ip}")
    else:
        return redirect(url_for('index'), 503)
