from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from app.database import db
from app.models.produto import Produto
import json

UPLOAD_FOLDER = 'app/images/anuncios'

class CampanhaController:
    pass