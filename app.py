from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sarvesh98#",
    database="images"
)
cursor = db.cursor()

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to save the uploaded image to the server
def save_image(image):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))

# Route to display images
@app.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            save_image(image)
            cursor.execute("INSERT INTO images (filename) VALUES (%s)", (image.filename,))
            db.commit()
    
    cursor.execute("SELECT filename FROM images")
    images = [row[0] for row in cursor.fetchall()]
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
