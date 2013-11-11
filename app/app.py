from flask import Flask,jsonify,render_template,url_for,request,redirect
from werkzeug import secure_filename
import os

# from xhtml2pdf import pisa
# from cStringIO import StringIO


APP_PATH = '/Users/luizfelipe/Dropbox/flask/pycode/ENVPYCODE/'
UPLOAD_FOLDER = APP_PATH + 'static/uploads/tmp/'
ALLOWED_EXTENSIONS = set(['zip'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
	retorno=''
	
	return render_template('home.html', retorno=retorno)

@app.route('/generated',methods=['POST','GET'])
def generate():
	if request.method == 'POST':
		code = request.form['code']
		language = request.form['language-type']
		try:
			lines = request.form['line_number']
		except:
			lines = None
	
		return render_template('generated.html',code=code,language=language,lines=lines)
		
	else:
		return redirect(url_for('home'))


# # Utility function
# def convertHtmlToPdf(sourceHtml, outputFilename):
# 	# open output file for writing (truncated binary)
# 	resultFile = open(outputFilename, "w+b")

# 	# convert HTML to PDF
# 	pisaStatus = pisa.CreatePDF(
# 			sourceHtml,                # the HTML to convert
# 			dest=resultFile)           # file handle to recieve result

# 	# close output file
# 	resultFile.close()                 # close output file

# 	# return True on success and False on errors
# 	return pisaStatus.err



def fetch_resources(uri, rel):
	import os

	path = os.path.join(APP_PATH+'static', uri.replace("/media/", ""))
	return path


# @app.route('/makepdf',methods=['POST','GET'])
# def makepdf():
# 	if request.method == 'POST':
# 		#pdf = StringIO()
# 		global str
# 		pdf_data = request.form['content']
# 		print pdf_data
		
# 		convertHtmlToPdf(pdf_data,APP_PATH+'static/created/pdf.pdf')
# 		return "forcar download here"
# 	else:
# 		return redirect(url_for('home'))


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/code-upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			import zipfile
			import uuid
			
			#cria nome unico
			unique_dir = uuid.uuid4()

			
			fh = open(UPLOAD_FOLDER + filename, 'rb')
			z = zipfile.ZipFile(fh)

			#cria dir randomico tendo a certeza que eh unico
			if not os.path.exists(UPLOAD_FOLDER+str(unique_dir)):
				os.makedirs(UPLOAD_FOLDER+str(unique_dir))
			
			for name in z.namelist():
				outpath = UPLOAD_FOLDER + str(unique_dir)
				z.extract(name, outpath)
			fh.close()


			retorno='true'
			return render_template('zipcode.html', retorno=retorno)
		else:
			print " erro   "
			return "bad zip file"
	
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form action="" method=post enctype=multipart/form-data>
	  <p><input type=file name=file>
		 <input type=submit value=Upload>
	</form>
	'''

if __name__ == '__main__':
	app.debug = True
	app.run()