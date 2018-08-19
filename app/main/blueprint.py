from flask import Blueprint

main = Blueprint('main', __name__)

import views, error_handler
