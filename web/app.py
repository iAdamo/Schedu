#!/usr/bin/python3

from models import storage
from flask import redirect, flash, request
from flask_wtf.csrf import CSRFError
from web.schedu import app


@app.errorhandler(404)
def page_not_found(e):
    """handle error 404
    """
    return redirect('https://enimo.tech')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.path in ('*'):
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    else:
        return redirect('/')


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
