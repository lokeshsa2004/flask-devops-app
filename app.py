# -*- coding: utf-8 -*-

from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask App Deployment On Ubuntu vm using AWS</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
            color: #ffffff;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 85%;
            margin: auto;
            padding: 40px 0;
        }
        h1, h2 {
            color: #ffd369;
        }
        .card {
            background: rgba(255,255,255,0.08);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 25px;
        }
        ul {
            line-height: 1.7;
        }
        footer {
            text-align: center;
            margin-top: 40px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        .badge {
            display: inline-block;
            background: #00adb5;
            padding: 6px 12px;
            border-radius: 20px;
            margin-right: 8px;
            font-size: 0.85em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Flask App Deployment on Ubuntu VM using AWS</h1>

        <div class="card">
            <h2>Project Goal</h2>
            <ul>
                <li>Deploy a Flask application on an Ubuntu virtual machine</li>
                <li>Use Gunicorn as a production-grade application server</li>
                <li>Use Nginx as a reverse proxy</li>
                <li>Ensure ip based acess and reboot persistence</li>
            </ul>
        </div>

        <div class="card">
            <h2>Architecture</h2>
            <p>
                <span class="badge">Browser</span> ->
                <span class="badge">IP</span> ->
                <span class="badge">Nginx (Port 80)</span> ->
                <span class="badge">Gunicorn (127.0.0.1:8000)</span> ->
                <span class="badge">Flask App</span>
            </p>
        </div>

        <div class="card">
            <h2>Key Implementation Steps</h2>
            <ul>
                <li>Ubuntu VM setup and system updates</li>
                <li>Python virtual environment creation</li>
                <li>Flask application development</li>
                <li>Gunicorn integration with systemd service</li>
                <li>Nginx reverse proxy configuration</li>
            </ul>
        </div>

        <div class="card">
            <h2>Results</h2>
            <ul>
                <li>Application accessible via public IP and domain</li>
                <li>Only Nginx exposed to the internet</li>
                <li>Gunicorn running securely on localhost</li>
                <li>Application survives VM reboot</li>
                <li>Accessible from desktop and mobile browsers</li>
            </ul>
        </div>

        <div class="card">
            <h2>Verification</h2>
            <ul>
                <li>systemd confirms Gunicorn and Nginx are running</li>
                <li>curl tests validate internal and external routing</li>
                <li>Browser tests confirm real-world access</li>
            </ul>
        </div>

        <footer>
            <p>Deployed by Lokesh S | Flask - Gunicorn - Nginx - Linux</p>
        </footer>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)
