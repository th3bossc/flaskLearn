# flaskLearn

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)



## Overview
Project created as part of learning flask through the course offered by [Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
The project is a blog site built using flask and jinja templating, and sqlite for the database

## Features

1. Offers authentication functionality with the help of flask-login library and SQLite database for storing encrypted user credentials
2. Allows users to create, update and delete posts
3. Account retreival functionality is offered in the form of email to recover lost password



## Installation

1. Clone the repository:

```bash
git clone https://github.com/th3bossc/flaskLearn.git

2. Navigate to the project directory:

```bash
cd flaskLearn

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt


4. Set up the necessary configuration variables, such as API keys, in the `.env` file.

5. Run the Flask development server:

```bash
python app.py


The server should now be running locally at `http://localhost:5000`.
