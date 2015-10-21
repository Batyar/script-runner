from flask import Flask, flash, redirect, url_for, request, get_flashed_messages, render_template, session, abort, send_file
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from flask.ext.bcrypt import check_password_hash
from models import *
import os, re, mimetypes

def split_folders_and_files(path):
    arr = sorted(os.listdir(path), key=lambda s: s.lower())
    files, folders = [], []
    for i in arr:
      files.append(i) if os.path.isfile(path + i) else folders.append(i)
    return render_template('files.html', files=files, folders=folders, check_img=check_img)

def flash_and_redirect(message):
    flash(message)
    return redirect(url_for('login'))

def check_img(file):
    if re.compile(r'(?i)(\.(?:jpg|jpeg|gif|png)$)').search(file) is not None:
        return True
    else:
        return False

def handle_files(abs_path):
    if not os.path.exists(abs_path):
        return abort(404)
    elif os.path.isfile(abs_path):
        return send_file(abs_path)
    else:
        return split_folders_and_files(abs_path + '/')