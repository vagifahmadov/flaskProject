from flask import Flask, render_template, request
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
    return render_template('index.html')


### TÜM BİLGİLERİ İSTER ŞEHİR İLÇEYİ İŞLER

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        # Get the list of files from webpage
        files = request.files.getlist("myFiles")

        # Iterate for each file in the files List, and Save them
        print(files)
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

        return_data = {'city': city, 'year': year, 'dist': dist, 'brand': brand, 'totalFiles': len(files)}
        print(return_data)
        return "Uploaded successfully!"

    return "Not supported method!"


@app.route('/info')
def info():
    brand = request.args['brand']
    city = request.args['city']
    dist = request.args['dist']
    year = request.args['year']
    total_files = request.args['totalFiles']
    data = {'brand': brand, 'city': city, 'year': year, 'dist': dist, 'totalFiles': total_files}
    print('CALLED from here')
    return render_template('result.html', data=data)


@app.route('/csv')
def csv_f():
    ram_res = []
    with open('db.csv') as f:
        # print(f.read())
        ram_res.append(f.read())
    f.close()
    ram_res.append({"name": "111saa.jpg"})
    # open the file in the write mode
    print(ram_res)
    with open('db.csv', 'w', newline='') as file:
        fieldnames = ['name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        list(map(lambda d: print(d), ram_res))
        list(map(lambda d: writer.writerow(d), ram_res))

    # close the file
    f.close()

    return "Ok"


if __name__ == '__main__':
    app.run(debug=True)
