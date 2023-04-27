from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = "marangozum"

### index ŞEHİR İLÇE BİLGİSİ İSTER


@app.route('/')
def home():
    print({"ip_1": request.remote_addr})
    return render_template('index.html')


### TÜM BİLGİLERİ İSTER ŞEHİR İLÇEYİ İŞLER

@app.route('/form')
def info():
    print(request.form)

    return render_template('info.html')


if __name__ == '__main__':
    app.run(debug=True)
