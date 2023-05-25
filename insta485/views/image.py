import flask
from flask import request, redirect, session, jsonify, send_from_directory
import insta485


@insta485.app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    """Download a file."""
    return send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)