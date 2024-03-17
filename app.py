from flask import Flask, render_template, request, redirect, url_for, session
from geopy.distance import geodesic

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class_location = (17.464600, 78.366630)  # Replace with actual coordinates

# Manually define usernames and passwords
users = {
    'raji': '123456',
    'archana': '123456',
    'yogi': '123456',
    # Add more usernames and passwords as needed
}

def check_attendance_range(user_location, class_location, max_distance):
    distance = geodesic(user_location, class_location).meters
    return distance <= max_distance

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid username or password. Please try again."
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_latitude = float(request.form['latitude'])
        user_longitude = float(request.form['longitude'])
        user_location = (user_latitude, user_longitude)
        max_distance = 1000000
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))
        within_range = check_attendance_range(user_location, class_location, max_distance)
        return render_template('result.html', within_range=within_range)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
