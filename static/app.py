from flask import Flask, render_template_string, request, redirect
from datetime import datetime
import sqlite3
con = sqlite3.connect("colorgenlogin.db")
app = Flask(__name__)

