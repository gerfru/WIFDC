from flask import Flask, render_template, abort, request, url_for, flash, redirect
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '3a6be9453b5623d2c6ae4789271af440554380051de68c47'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


messages = [{'title': 'Nachricht 1',
             'content': 'Lena'},
            {'title': 'Nachricht 2',
             'content': 'Lumos'}
            ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Webform')
def Webform():
    return render_template('Webform.html', messages=messages)

@app.route('/500')
def error500():
    abort(500)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/comments/')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]
    return render_template('comments.html', comments=comments)

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
            return redirect(url_for('index'))

    return render_template('create.html')