from decimal import Decimal

from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from flask_restful import Resource, reqparse
from sqlalchemy import func

from app import db
from app.models import Crime, Prison, Prisoner, User
from io import StringIO
import pandas as pd

import csv


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name of the prisoner is required')
parser.add_argument('age', type=int, required=True, help='Age of the prisoner is required')
parser.add_argument('gender', type=str, required=True, help='Gender of the prisoner is required')
parser.add_argument('crime', type=str, required=True, help='Type of crime committed is required')
parser.add_argument('sentence_years', type=int, required=True, help='Length of the sentence in years is required')
parser.add_argument('prison', type=str, required=True, help='Name of the prison is required')


class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return {'message': 'Username and password are required!'}, 400

        username = data['username']
        password = data['password']

        if not username or not password:
            return {'message': 'Username and password cannot be empty!'}, 400

        if User.query.filter_by(username=username).first():
            return {'message': 'User already exists'}, 401

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return {'message': 'Username and password are required!'}, 400

        username = data['username']
        password = data['password']

        if not username or not password:
            return {'message': 'Username and password cannot be empty!'}, 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid username or password'}, 401

        # Generate access token and refresh token
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Construct the response including access token, refresh token, and username
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'username': user.username
        }

        return response_data, 200


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {'access_token': new_access_token}, 200


class PrisonerStatistics(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            # Number of prisoners by crime type
            crime_count_query = db.session.query(
                Crime.crime_name, func.count(Prisoner.prisoner_id)
            ).join(Prisoner, Prisoner.crime_id == Crime.crime_id).group_by(Crime.crime_name).all()
            crime_count = {crime_name: count for crime_name, count in crime_count_query}

            # Average sentence length by crime type
            avg_sentence_query = db.session.query(
            Crime.crime_name, func.avg(Prisoner.sentence_years)
            ).join(Prisoner, Prisoner.crime_id == Crime.crime_id).group_by(Crime.crime_name).all()

            # Convert Decimal to float for JSON serialization and round the values
            average_sentence_by_crime = {
                crime_name: round(float(avg_sentence), 2) if isinstance(avg_sentence, Decimal) else round(avg_sentence, 2)
                for crime_name, avg_sentence in avg_sentence_query
            }

            # Gender distribution of prisoners
            gender_distribution_query = db.session.query(
                Prisoner.gender, func.count(Prisoner.prisoner_id)
            ).group_by(Prisoner.gender).all()
            gender_distribution = {gender: count for gender, count in gender_distribution_query}

            return {
                'crime_count': crime_count,
                'average_sentence_by_crime': average_sentence_by_crime,
                'gender_distribution': gender_distribution
            }, 200
        else:
            return jsonify({'message': 'User not found'}), 401


class PrisonerResourceDetail(Resource):
    @jwt_required()
    def get(self, prisoner_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            prisoner = Prisoner.query.get(prisoner_id)
            if prisoner:
                return prisoner.to_dict()
            return {'message': 'Prisoner not found'}, 404
        else:
            return jsonify({'message': 'User not found'}), 401


class PrisonerListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            prisoners = Prisoner.query.all()
            return [prisoner.to_dict() for prisoner in prisoners]
        else:
            return jsonify({'message': 'User not found'}), 401


class UploadCSV(Resource):
    def post(self):
        file = request.files['file']
        if not file:
            return {'message': 'No file uploaded'}, 400

        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_data = csv.reader(stream)
        next(csv_data)  # Skip the header row

        # Define a mapping for the gender values
        gender_mapping = {
            'M': 'Male',
            'F': 'Female',
            'O': 'Other'
        }

        for row in csv_data:
            prisoner_id, name, age, gender, crime, sentence_years, prison = row

            # Convert the gender value
            if gender in gender_mapping:
                gender = gender_mapping[gender]
            else:
                return {'message': f'Invalid gender value: {gender}'}, 400

            crime_name = Crime.query.filter_by(crime_name=crime).first()
            if not crime_name:
                crime_name = Crime(crime_name=crime)
                db.session.add(crime_name)
                db.session.commit()

            prison_name = Prison.query.filter_by(prison_name=prison).first()
            if not prison_name:
                prison_name = Prison(prison_name=prison)
                db.session.add(prison_name)
                db.session.commit()

            prisoner = Prisoner(
                name=name,
                age=int(age),
                gender=gender,
                crime_id=crime_name.crime_id,
                sentence_years=int(sentence_years),
                prison_id=prison_name.prison_id
            )
            db.session.add(prisoner)

        db.session.commit()
        return {'message': 'Data uploaded successfully'}, 200


class AgeDistribution(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            prisoners = Prisoner.query.all()
            df = pd.DataFrame([prisoner.to_dict() for prisoner in prisoners])
            age_distribution = df['age'].value_counts().reset_index()
            age_distribution.columns = ['age', 'count']
            return jsonify(age_distribution.to_dict(orient='records'))
        else:
            return jsonify({'message': 'User not found'}), 401


class PrisonPopulation(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            prison_population_query = db.session.query(
                Prisoner.prison_id, Prison.prison_name, func.count(Prisoner.prisoner_id)
            ).join(Prison, Prisoner.prison_id == Prison.prison_id).group_by(Prison.prison_id, Prison.prison_name).all()

            prison_population = [{'prison_name': prison_name, 'count': count} for prison_id, prison_name, count in
                             prison_population_query]
            return jsonify(prison_population)
        else:
            return jsonify({'message': 'User not found'}), 401


