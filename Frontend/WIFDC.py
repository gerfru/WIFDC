#Imports we surely need
from flask import Flask, render_template, abort, request, url_for, flash, redirect
from forms import CourseForm
from DBConnector import connectDB


# Wir definieren die App und einen Namen, der vom Filenamen übernommen wird.
# The flash() function stores flashed messages in the client’s browser session, which requires setting a secret key. This secret key is used to secure sessions, which allow Flask to remember information from one request to another, such as moving from the new message page to the index page. The user can access the information stored in the session, but cannot modify it unless they have the secret key, so you must never allow anyone to access your secret key. See the Flask documentation for sessions for more information
app = Flask(__name__)
app.config['SECRET_KEY'] = '9cfdb598bb32931ca09aa2e8807fa2e1c82868045c85fe07'

courses_list = [{
    'title': 'Python 101',
    'description': 'Learn Python basics',
    'price': 34,
    'available': True,
    'level': 'Beginner'
    }]


messages = [{'title': 'Nachricht 1',
             'content': 'Lena'},
            {'title': 'Nachricht 2',
             'content': 'Lumos'}
            ]

 # You use the @app.route() decorator to create a view function called index(), which calls the render_template() function as the return value, which in turn renders a template called index.html
@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

# Here you use the @app.errorhandler() decorator to register the function page_not_found() as a custom error handler. The function takes the error as an argument, and it returns a call to the render_template() function with a template called 404.html. You also return the integer 404 after the render_template() call. This tells Flask that the status code in the response should be 404. If you don’t add it, the default status code response will be 200, which means that the request has succeeded.
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Here you use the same pattern as you did for the 404 error handler. You use the app.errorhandler() decorator with a 500 argument to make a function called internal_error() into an error handler. You render a template called 500.html, and respond with a status code of 500.
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# You use the @app.route() decorator to create a view function called Webform(), which calls the render_template() function as the return value, which in turn renders a template called Webform.html. In the Webform, messages will be displayed.
# Furthermore, through parsing "messages", we display these messages on the site.
@app.route('/Webform')
def Webform():
    return render_template('Webform.html', messages=messages)

# Too easy :-)
@app.route('/about/')
def about():
    return render_template('about.html')

#In the route below, you have a URL variable idx. This is the index that will determine what message will be displayed. For example, if the URL is /messages/0, the first message (Message Zero) will be displayed. You use the int converter to accept only positive integers, because URL variables have string values by default.
#
#Inside the message() view function, you have a regular Python list called messages with three messages. (In a real-world scenario, these messages would come from a database, an API, or another external data source.) The function returns a call to the render_template() function with two arguments, message.html as the template file, and a message variable that will be passed to the template. This variable will have a list item from the messages list depending on the value of the idx variable in the URL.
#
# Additionally, we import the abort() function, which you use to abort the request and respond with an error. In the message() view function, you use a try ... except clause to wrap the function. You first try to return the messages template with the message that corresponds to the index in the URL. If the index has no corresponding message, the IndexError exception will be raised. You then use the except clause to catch that error, and you use abort(404) to abort the request and respond with a 404 Not Found HTTP error.
@app.route('/messages/<int:idx>')
def message(idx):
    app.logger.info('Building the messages list...')
    messages = ['Message Zero', 'Message One', 'Message Two']
    try:
        app.logger.debug('Get message with index: {}'.format(idx))
        return render_template('message.html', message=messages[idx])
    except IndexError:
        app.logger.error('Index {} is causing an IndexError'.format(idx))
        abort(404)


# In the if statement you ensure that the code following it is only executed when the request is a POST request via the comparison request.method == 'POST'.

# You then extract the submitted title and content from the request.form object that gives you access to the form data in the request. If the title is not provided, the condition if not title would be fulfilled. In that case, you display a message to the user informing them that the title is required using the flash() function. This adds the message to a flashed messages list. You will later display these messages on the page as part of the base.html template. Similarly, if the content is not provided, the condition elif not content will be fulfilled. If so, you add the 'Content is required!' message to the list of flashed messages.

# If the title and the content of the message are properly submitted, you use the line messages.append({'title': title, 'content': content}) to add a new dictionary to the messages list, with the title and content the user provided. Then you use the redirect() function to redirect users to the index page. You use the url_for() function to link to the index page.
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('Webform'))

    return render_template('create.html')

@app.route('/courses/')
def courses():
    return render_template('courses.html', courses_list=courses_list)


@app.route('/addCourse/', methods=('GET', 'POST'))
def addCourse():
    form = CourseForm()
    if form.validate_on_submit():
        courses_list.append({'title': form.title.data,
                             'description': form.description.data,
                             'price': form.price.data,
                             'available': form.available.data,
                             'level': form.level.data
                             })
        return redirect(url_for('courses'))
    return render_template('addCourse.html', form=form)


@app.route('/DBConnector/')
def DBConnector():
    conn, cur = connectDB('localhost', 'HCE')
    cur.execute('select * from hce.Test_WIFDC.posts')
    posts = cur.fetchall()
    conn.close()
    print(posts)
    return render_template('DBConnector.html', posts=posts)

@app.route('/createDBentry/', methods=('GET', 'POST'))
def createDBentry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn, cur = connectDB('localhost', 'HCE')
            strQuery = '''INSERT INTO hce.TEST_WIFDC.posts (title, content) VALUES ('{strTitle}','{strContent}')'''
            cur.execute(strQuery.format(strTitle=title,strContent=content))
            conn.commit()
            conn.close()
            return redirect(url_for('DBConnector'))

    return render_template('createDBentry.html')