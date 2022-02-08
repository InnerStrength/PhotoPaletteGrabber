import os
from flask import Flask, redirect, render_template, request
from flask_bootstrap import Bootstrap
from palette import Palette
from werkzeug.utils import secure_filename

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    return render_template("start.html")


@app.route("/palette.html", methods=["POST", "GET"])
def gen_palette():
    image = request.files["image"]
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.root_path, 'static', 'img', filename))
    size = request.form.get("size")
    sensitivity = request.form.get("sensitivity")
    output = Palette(filename, size, sensitivity).make_palette()
    return render_template("palette.html", output=output)


if __name__ == "__main__":
    app.run(debug=True)
