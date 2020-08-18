from flask import Blueprint
from flask_restful import Api
from xyzFfootball.util.imports import import_submodules


xyz_bp = Blueprint('api_student', __name__, url_prefix="/app")
xyz_api = Api(xyz_bp)

import_submodules(globals(), __name__, __path__)

