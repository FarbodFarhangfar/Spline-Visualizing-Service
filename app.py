from flask import Flask, request, render_template
import splines

import os

cwd = os.getcwd()
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")



@app.route('/spline', methods=['POST', 'GET'])
def spline():
    """
    showing an image to help the user with inserting tck
    """
    if request.method == "POST":
        image = request.files["image"]
        if not image:
            return 'no image uploaded', 400
        else:

            file_dir = os.path.join(cwd, 'static', image.filename)
            filename = image.filename
            image.save(file_dir)

            filename = splines.showing_image(filename)
            return render_template("spline.html", user_image=filename[0], original=filename[1])


@app.route('/tck', methods=['POST', 'GET'])
def getting_TCK():
    """
    blow is an example of 't' for input
    0.|0.|0.|0.|0.14285714|0.28571429|0.42857143|0.57142857|0.71428571|0.85714286|1.|1.|1.|1.

    blow is an example of 'c' for input
    (0,495)|(60,400)|(190,500)|(355,400)|(415,380)|(445,400)|(515,340)|(640,435)|(740,400)|(1000,600)

    k is the degree of the spline
    """

    t = request.form['T']
    c = request.form['C']
    k = request.form['K']
    file_dir = request.form['dir'][:-1]
    # split t by '|'
    t = t.split('|')
    t = list(map(float, t))

    # split c and make a list of it
    c = c.split('|')
    x = []
    y = []
    for i in c:
        i = i.split(',')
        x.append(int(i[0][1:]))
        y.append(int(i[1][:-1]))
    c = [x[:], y[:]]
    del x, y

    k = int(k)

    tck = [t, c, k]

    filename = splines.showing_image(file_dir, spline=True, tck=tck)
    if filename[1]:
        return "Invalid tck for this image"
    return render_template('final_view.html', user_image=filename[0])


if __name__ == '__main__':
    app.run()
