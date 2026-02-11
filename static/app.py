from flask import Flask, render_template_string, request, redirect, sqlite3
from datetime import datetime
import sqlite3
con = sqlite3.connect("colorgenlogin.db")