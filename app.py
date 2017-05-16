from flask import Flask, render_template, request
import ftplib
import json
import os

app = Flask(__name__)

def connect_to_ftp():
    server = "ftp.divesb.com"
    user = "divesbcom"
    password = os.environ["DIVE_PASS"]
    return ftplib.FTP(server, user, password)

def download_json():
    ftp = connect_to_ftp()
    ftp.cwd("/api/")
    ftp.retrbinary("RETR menu.json", open("menu.json", 'wb').write)

def edit_json(info, filename):
    names = ["price", "description", "name"]
    item = {name: info[name] for name in names}
    item["image"] = filename
    item["price"] = float(item["price"])

    with open("menu.json") as f:
        data = json.load(f)

    for i, category in enumerate(data):
        if category['name'] == info["Category"]:
            data[i]["items"].append(item)

    with open("menu.json.out", "w") as f:
        json.dump(data, f, indent=4)


def upload_json():
    ftp = connect_to_ftp()
    ftp.cwd("/api/")
    ftp.storlines("STOR out.menu.json", open("menu.json.out", 'rb'))

def upload_image(f):
    ftp = connect_to_ftp()
    ftp.cwd("/api/divePhotos/")
    ftp.storlines("STOR " + f.filename, f)

@app.route('/')
def form():
   return render_template('form.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      f = request.files['image']
      f.filename = result['filename'] + f.filename[-4:]
      print(f)

      download_json()
      for x in result:
          print(x, result[x])
      edit_json(result, f.filename)

      upload_json()
      upload_image(f)

      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(host = "0.0.0.0", debug = True)
