from flask import Blueprint, render_template
from flask_restful import Api
from app.views import PrisonerResourceDetail, PrisonerListResource, UploadCSV, RegisterUser, UserLogin, RefreshToken, \
    PrisonerStatistics, AgeDistribution, PrisonPopulation

# Blueprint for serving HTML pages
main = Blueprint('main', __name__)


@main.route('/login')
def login_page():
    return render_template('login.html')


@main.route('/prisoner')
def prisoners_page():
    return render_template('prisoner.html')


@main.route('/prisoner-details')
def prisoner_details_page():
    return render_template('prisoner-detail.html')


def initialize_routes(app):
    api = Api(app)
    api.add_resource(PrisonerListResource, '/api/prisoners')
    api.add_resource(PrisonerResourceDetail, '/api/prisoners/<int:prisoner_id>')
    api.add_resource(UploadCSV, '/api/upload')
    api.add_resource(RegisterUser, '/api/register')
    api.add_resource(UserLogin, '/api/login')
    api.add_resource(RefreshToken, '/api/refresh')
    api.add_resource(PrisonerStatistics, '/api/statistics')
    api.add_resource(AgeDistribution, '/api/age-distribution')
    api.add_resource(PrisonPopulation, '/api/prison-population')
