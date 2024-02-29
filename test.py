data = {
                 'firstname': 'Adi',
                 'lastname': 'D',
                 'email': 'email',
                 'phone': 'phone',
                 'gender': 'gender',
                 'age': 50,
                 'filename' : 'filename',
                 'message' : 'message'
                }

with open('./static/reports/data.txt', 'w') as file:
        file.write("First Name: {}\n".format(data.get('firstname')))
        file.write("Last Name: {}\n".format(data.get('lastname')))
        file.write("Email: {}\n".format(data.get('email')))
        file.write("Phone: {}\n".format(data.get('phone')))
        file.write("Gender: {}\n".format(data.get('gender')))
        file.write("Age: {}\n".format(data.get('age')))