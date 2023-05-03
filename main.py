from flask import Flask, render_template, request
import random
import string


app = Flask(__name__, static_folder='static', template_folder='templates')
upload_folder = 'uploads'
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
        for file in files:
            extension = str(file.filename).split(".")[-1]
            filename = "{fn}.{ex}".format(fn=''.join(random.choices(string.ascii_letters, k=16)), ex=extension)
            path = "{upf}/{fn}".format(upf=upload_folder, fn=filename)
            file.save(path)
        city = request.form.get('city')
        dist = request.form.get('dist')
        brand = request.form.get('brand')

        return_data = {'city': city, 'dist': dist, 'brand': brand, 'totalFiles': len(files)}
        print(return_data)
        return "Uploaded successfully!"

    return "Not supported method!"


@app.route('/info')
def info():
    brand = request.args['brand']
    city = request.args['city']
    dist = request.args['dist']
    total_files = request.args['totalFiles']
    data = {'brand': brand, 'city': city, 'dist': dist, 'totalFiles': total_files}
    print('CALLED from here')
    return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
