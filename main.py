from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')
upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = "marangozum"

### index ŞEHİR İLÇE BİLGİSİ İSTER


@app.route('/')
def home():
    print({"ip_1": request.remote_addr})
    return render_template('index.html')


### TÜM BİLGİLERİ İSTER ŞEHİR İLÇEYİ İŞLER

@app.route('/upload')
def upload():
    if request.method == 'POST':

        # Get the list of files from webpage
        files = request.files.getlist("file")

        # Iterate for each file in the files List, and Save them
        for file in files:
            path = "{upf}/{fn}".format(upf=upload_folder, fn=file.filename)
            file.save(path)
        print(request.form)
        return "<h1>Files Uploaded Successfully.!</h1>"

    return render_template('info.html')


if __name__ == '__main__':
    app.run(debug=True)
