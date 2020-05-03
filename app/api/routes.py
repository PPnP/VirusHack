from flask import Blueprint

from app.api.controllers.confirmation import VolunteerConfirmationController, RequestConfirmationController


api = Blueprint('api', __name__, template_folder='../templates', static_folder='../static')

api.add_url_rule('/confirmation/volunteer', view_func=VolunteerConfirmationController.as_view('VolunteerConfirmation'))
api.add_url_rule('/confirmation/request', view_func=RequestConfirmationController.as_view('RequestConfirmation'))
