from flask import Flask, flash, request, redirect, url_for, render_template,url_for
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import pickle
from tensorflow.keras.models import load_model
# from pushbullet import PushBullet
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



# Loading Model
pneumonia_model = load_model('models/pneumonia_model_resnet101.h5')
covid_model = load_model('models\covid.h5')

# Configuring Flask
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "lungxpert"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def send_email_with_data( receiver_email, subject, data):
    # Construct HTML content for the email
    html_content = """
    <html>
    <head>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .positive {{
                color: red;
                font-weight: bold;
            }}
            .negative {{
                color: green;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h2>{} Test report</h2>
        <table>
            
            <tr>
                <td>First Name</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Last Name</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Email</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Phone</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Aadhar No. </td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Gender</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Age</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Address</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Result</td>
                <td class="{}">{}</td>
            </tr>
        </table>
    </body>
    </html>
    """.format(data['type'],data['firstname'], data['lastname'], data['email'], data['phone'],data['aadhar'], data['gender'].upper(), data['age'],data['address'] ,data['message'].lower(), data['message'])
    message = MIMEMultipart("alternative")
    message["From"] = 'aditidagadkhair3011@gmail.com'
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add HTML content to the message
    message.attach(MIMEText(html_content, "html"))

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login('aditidagadkhair3011@gmail.com', '****')
        server.sendmail('aditidagadkhair3011@gmail.com', receiver_email, message.as_string())


########################### Routing Functions ########################################

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/faq')
def faq():
    return render_template('faq.html')
@app.route('/treatment')
def treatment():
    return render_template('treatment.html')
    

@app.route('/pneumonia')
def pneumonia():
    return render_template('pneumonia.html')

@app.route('/covid')
def covid():
    return render_template('covid.html')


########################### Result Functions ########################################


@app.route('/resultp', methods=['POST'])
def resultp():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        aadhar = request.form['aadhar']
        address = request.form['address']
        file = request.files['file']    #input image
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
            img = cv2.imread('static/uploads/'+filename)
            img = cv2.resize(img,(224,224))
            img = np.expand_dims(img,axis=0)
            img = img/255.0
            pred = pneumonia_model.predict(img)
            message = "Pneumonia Negative"
            if pred < 0.5:
                pred = 0
            else:
                message = "Pneumonia Positive"
                pred = 1
            # send_email(email=email,message=message)
            data = {
                 'firstname': firstname,
                 'lastname': lastname,
                 'email': email,
                 'phone': phone,
                 'gender': gender,
                 'age': age,
                 'message' : message,
                 'type' : 'PNEUMONIA',
                 'aadhar': aadhar,
                 'address' : address
                }
            send_email_with_data(receiver_email=email,subject="Pneumonia Test Report",data=data)
            return render_template('resultp.html', filename=filename, fn=firstname, ln=lastname, age=age, r=pred, gender=gender,aadhar=aadhar, address=address, smell=smell, taste=taste, breathe=breathe)

        else:
            flash('Allowed image types are - png, jpg, jpeg')
            return redirect('/')
@app.route('/resultc', methods=['POST'])
def resultc():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        aadhar = request.form['aadhar']
        address = request.form['address']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
            img = cv2.imread('static/uploads/'+filename)
            img = cv2.resize(img, (224, 224))
            img = img.reshape(1, 224, 224, 3)
            img = img/255.0
            pred = covid_model.predict(img)
            message = "Covid Negative"
            if pred < 0.5:
                pred = 0
                message = "Covid Positive"
            else:
                pred = 1
            data = {
                 'firstname': firstname,
                 'lastname': lastname,
                 'email': email,
                 'phone': phone,
                 'gender': gender,
                 'age': age,
                 'message' : message,
                 'type' : 'COVID 19',
                 'aadhar': aadhar,
                 'address' : address
                }
            send_email_with_data(receiver_email=email,subject="Covid 19 Test Report",data=data)
            return render_template('resultc.html', filename=filename, fn=firstname, ln=lastname, age=age, r=pred, gender=gender,aadhar=aadhar,address=address)

        else:
            flash('Allowed image types are - png, jpg, jpeg')
            return redirect(request.url)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    app.run(debug=True)
