#!/usr/bin/python3

from models import storage
from flask import abort, redirect, flash, request
from flask_wtf.csrf import CSRFError
from web.schedu import app



@app.errorhandler(404)
def page_not_found(e):
    """handle error 404
    """
    return redirect('https://github.com/ibhkh')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.path == '/auth/sign_in':
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    elif request.path == '/auth/sign_out':
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    elif request.path == '/':
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    else:
        abort(400)

        
@app.teardown_appcontext
def teardown(exception):
    """A method to remove the current SQLAlchemy Session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
