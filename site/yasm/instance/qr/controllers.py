from flask import Blueprint, render_template, request
from xhtml2pdf import pisa
from io import StringIO, BytesIO
import qrcode
import qrcode.image.svg
import uuid

module = Blueprint('qr', __name__, url_prefix='/qr')

@module.route('/', methods=['GET'])
def index(path="dummy"):
    return render_template(
        "qr/base.html"
    )

@module.route('/contract.pdf', methods=['POST'])
def generateContract():
    img = BytesIO()
    qrcode.make(request.form["child_passport"], image_factory = qrcode.image.svg.SvgPathImage).save(img)
    svgString = "".join(chr(x) for x in img.getvalue()).replace('<?xml version=\'1.0\' encoding=\'UTF-8\'?>', '') # WTF
    # xhtml2pdf fails on svg, use jpeg
    fileName = '/tmp/' + str(uuid.uuid4()) + '.jpg'
    qrcode.make(request.form["child_passport"]).save(fileName)
    jpgString = '<img src="file://' + fileName + '"/>'
    html = render_template("qr/contract.html", ctx = request.form, qr = jpgString)
    pdf = BytesIO()
    htmlString = StringIO(html)
    pisa.CreatePDF(htmlString, dest=pdf)
    headers = {
        "Content-Type": "application/pdf",
        "Content-Disposition": "inline; filename*=%D0%A0%D0%BE%D0%B4%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B4%D0%BE%D0%B3%D0%BE%D0%B2%D0%BE%D1%80%20%D0%9B%D0%AD%D0%A8.pdf" }
    return pdf.getvalue(), 200, headers

from pyzbar.pyzbar import decode
from PIL import Image

@module.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == "POST":
        tmpFile = request.files["file"]
        qr = decode(Image.open(tmpFile))
        return qr[0].data
    return '''
    <!doctype html>
    <meta charset="utf-8" />
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
