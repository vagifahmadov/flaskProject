from flask import Flask, render_template, request, jsonify, json, session
import random
import string
import csv

app = Flask(__name__, static_folder='static', template_folder='templates')
upload_folder = 'static/img/header'
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = "marangozum"


### index ŞEHİR İLÇE BİLGİSİ İSTER

@app.route('/')
def home():
    # print({"ip_1": request.remote_addr})
    csv_file = "db.csv"
    dict_data = []
    c = 0
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row.update({'active': 'active'}) if c == 0 else row.update({'active': ''})
            c += 1
            print(row)
            dict_data.append(row)

    return render_template('index.html', data=dict_data)


### TÜM BİLGİLERİ İSTER ŞEHİR İLÇEYİ İŞLER

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        # Get the list of files from webpage
        files = request.files.getlist("myFiles")

        # Iterate for each file in the files List, and Save them
        print(files)
        filename = ''
        for file in files:
            extension = str(file.filename).split(".")[-1]
            print(extension)
            filename = "{fn}.{ex}".format(fn=''.join(random.choices(string.ascii_letters, k=16)), ex=extension)
            path = "{upf}/{fn}".format(upf=upload_folder, fn=filename)
            file.save(path)
        city = request.form.get('city')
        dist = request.form.get('dist')
        brand = request.form.get('brand')
        year = request.form.get('year')
        # insert to CSV
        csv_file = "db.csv"
        csv_columns = ['city', 'dist', 'brand', 'year', 'fileName']
        dict_data = []
        csv_file = "db.csv"
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dict_data.append(row)
        dict_data.append({'city': city, 'year': year, 'dist': dist, 'fileName': filename, 'brand': brand})
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                data: dict
                for data in dict_data:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

        print(dict_data[0])
        session['data'] = dict_data[0]
        # return redirect(url_for('.info', messages=messages, code=302))
        # return render_template('result.html', data=return_data)
        return jsonify(dict_data[0])

    return "Not supported method!"


@app.route('/info')
def info():
    messages = session['data']
    print('CALLED from here')
    return render_template('result.html', data=json.loads(json.dumps(messages)))


@app.route('/csv')
def csv_f():
    csv_columns = ['No', 'Name', 'Country']
    dict_data = []
    csv_file = "db.csv"
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dict_data.append(row)
            print(row)

    dict_data2 = [
        {'No': 1, 'Name': 'Alex', 'Country': 'India'},
        {'No': 2, 'Name': 'Ben', 'Country': 'USA'},
        {'No': 3, 'Name': 'Shri Ram', 'Country': 'India'},
        {'No': 4, 'Name': 'Smith', 'Country': 'USA'},
        {'No': 5, 'Name': 'Yuva Raj', 'Country': 'India'},
    ]

    list(map(lambda d: dict_data.append(d), dict_data2))
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            data: dict
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")

    return "Ok"


if __name__ == '__main__':
    app.run(debug=True)
