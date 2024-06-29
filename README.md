**Prisoner Management System**
This project is a Prisoner Management System built with Flask, MySQL, and Flask-RESTful.
Deployed on heroku CLI 
To directly see the project please go to https://prisoner-management-system-3d0646e3806f.herokuapp.com/login
you can access application using
username:hamzafaisal
password:password123

That is how the application look
<img width="1431" alt="Screenshot 2024-06-30 at 2 11 09 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/51936dce-df5b-4e5e-a06c-f25a6f074332">

<img width="1423" alt="Screenshot 2024-06-30 at 2 11 26 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/38f24185-b88f-426a-9331-3d5a72f9d1a7">




Prerequisites
Before running this project, make sure you have the following installed:

-Python 3.9 or higher
-MySQL (for local development)
-Git (optional, for version control)
-Installation

**Clone the repository:**

-git clone https://github.com/hamzafaisaljarral/prisoner_data_management.git
-cd prisoner_data_management


**Setup Virtual Environment:**


Install virtualenv if not already installed
-pip install virtualenv

Create a virtual environment
-virtualenv venv

# Activate the virtual environment
# On Windows
-venv\Scripts\activate
# On macOS/Linux
-source venv/bin/activate

# Install Dependencies:
-pip install -r requirements.txt
-Create .env file:

# Create a .env file in the root directory of your project with the following configuration:
**you can use these that is deployed mySQL DB on heroku you can use it**
SECRET_KEY = 'please-add-something-unique'
DEV_DATABASE_URL=mysql://u7kx3ipb59dgfnd4:yf4ma1z6fkjt90vp@irkm0xtlo2pcmvvz.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/mode6c9z20vtel4p
TEST_DATABASE_URL=mysql+pymysql://prison_admin:password@localhost/prison_test
SQLALCHEMY_DATABASE_URI =mysql://u7kx3ipb59dgfnd4:yf4ma1z6fkjt90vp@irkm0xtlo2pcmvvz.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/mode6c9z20vtel4p
JWT_SECRET_KEY = 'your_jwt_secret_key'

# if you have mySQL setup on your system please do following.
mysql -u root -p
CREATE DATABASE prison_management;
CREATE DATABASE prisoner_test;

# please replace .env with correct credentials 
SECRET_KEY = 'please-add-something-unique'
DEV_DATABASE_URL='mysql+pymysql://prison_admin:password@localhost/prison_management'
TEST_DATABASE_URL=mysql+pymysql://prison_admin:password@localhost/prison_test
SQLALCHEMY_DATABASE_URI =mysql+pymysql://prison_admin:password@localhost/prison_management
JWT_SECRET_KEY = 'your_jwt_secret_key'



# Run this after creating .env
**Apply Migrations:**
-flask db migrate
-flask db upgrade


**Run the Application:**
-flask run

The application should now be running locally. Open your web browser and go to http://localhost:5000 to access the application.

API Endpoints
Register User: http://127.0.0.1:5000/api/register
<img width="1037" alt="Screenshot 2024-06-30 at 1 36 53 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/21b8f5cf-f646-4974-b587-fac5e545e1cf">

Login Page: http://localhost:5000/login
<img width="1438" alt="Screenshot 2024-06-30 at 1 38 57 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/52cae185-f88f-4239-b807-a4a2aa03b24d">

Prisoner List Page: http://localhost:5000/prisoner
<img width="1433" alt="Screenshot 2024-06-30 at 1 39 57 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/a2f3d967-b2e7-4f3c-a346-9b1e69c8a28e">
<img width="1437" alt="Screenshot 2024-06-30 at 1 40 18 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/7c3bc4d2-44ec-4c8f-bbb6-5b64cfb06dcf">
<img width="1436" alt="Screenshot 2024-06-30 at 1 40 35 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/c5749255-cdd6-447c-a089-638bc14a1d1e">

<img width="1437" alt="Screenshot 2024-06-30 at 1 40 49 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/6fb687a0-c2a4-4c9e-87af-ff23d475decd">

Prisoner Details Page: http://localhost:5000/prisoner-details
<img width="1429" alt="Screenshot 2024-06-30 at 1 41 01 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/4be01e37-b361-4be4-ab36-a77d56edc96d">

API Documentation: After running the app,
detailed API documentation.
For using deployed api please use https://prisoner-management-system-3d0646e3806f.herokuapp.com instead of http://127.0.0.1:5000

Register User: http://127.0.0.1:5000/api/register  (POST)
Body:
json:
{
    "username":"newuser",
    "password":"password123"
}

Login API: http://127.0.0.1:5000/api/login  (POST)
body:
json:
{
    "username":"newuser",
    "password":"password123"
}

Upload Data in csv: http://127.0.0.1:5000/api/upload (POST)
body:
form data:
file:
Authorization:
Bearer Token: (paste authorization token)

Get Prisoner : http://127.0.0.1:5000/api/prisoners (GET)
Authorization:
Bearer Token: (paste access_token)

<img width="1059" alt="Screenshot 2024-06-30 at 1 54 07 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/9cdbbd5e-299d-40c1-a789-25cd3c6b9d0b">

Get prisoner Details: http://127.0.0.1:5000/api/prisoners/2 (GET)
Authorization:
Bearer Token: (Paste access_token)
<img width="1049" alt="Screenshot 2024-06-30 at 1 55 26 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/3872296f-8c3c-4658-bd78-bede1b31094f">

Get the prisoner Stats : http://127.0.0.1:5000/api/statistics (GET)
Authorization:
Bearer Token: (Paste access_token)
This will return the 
• Number of prisoners by crime type.
• Average sentence length by crime type.
• Gender distribution of prisoners.

<img width="1058" alt="Screenshot 2024-06-30 at 2 01 25 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/86d6387f-33c6-429a-b6d8-066fd42a0b7f">

Get the prisoner age count : http://127.0.0.1:5000/api/age-distribution (GET)
Authorization:
Bearer Token: (Paste access_token)
<img width="1052" alt="Screenshot 2024-06-30 at 2 05 03 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/fa5ab158-4f0c-4d74-a453-66e1de1bdaa1">

Get the prison population for each prison : http://127.0.0.1:5000/api/prison-population (GET)
Authorization:
Bearer Token: (Paste access_token)

<img width="1060" alt="Screenshot 2024-06-30 at 2 07 24 AM" src="https://github.com/hamzafaisaljarral/prisoner_data_management/assets/39766112/ba98cf16-f910-4b2e-810f-bbb8d1647851">


Additional Notes
For production deployment, configure appropriate environment variables and ensure necessary security measures are implemented.
Ensure all dependencies are updated and reviewed regularly for security updates.
