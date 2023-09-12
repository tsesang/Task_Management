from flask import Flask, render_template, request

app = Flask(__name__)

# app.config['pictures/']
app.config['SECRET_KEY'] = 'secretkey'


# app.listen(6000)

# @app.route('/')
# def home():
#     return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/')
# def home():
#     return render_template('contact.html')

# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         name = request.form['name']
#         message = request.form['message']
#         return f"Thank you, {name}, for your message: {message}"
    
@app.route('/students_list')
def students() :
    list1 = ['trarik','delek','sherap']
    return render_template('students.html', names = list1)

@app.route('/exams/<int:a>')
def exams(a):
    return render_template('exams.html',marks =a )

@app.route('/<custom_route>') #dynamic route
def cutom_fun(custom_route):
    return f'this page is for {custom_route}'

#Learning File Handling



@app.route ('/')
def form_page():
    return render_template('fileupload.html')

@app.route('/upload',methods =['post'])
def upload():
    fileObj = request.files['image']
    if fileObj:
        fileObj.save('pictures/' + fileObj.filename)
        return 'Success'
    else :
        return 'no files uploaded'
    
if __name__ == '__main__':
    app.run(debug=True)


