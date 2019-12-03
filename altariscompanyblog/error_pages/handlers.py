# handlers.py
from flask import Blueprint,render_template

error_pages = Blueprint('error_pages',__name__)

#passes the code 404 on an error page if not found passing the error encountered
@error_pages.app_errorhandler(404)
def error_404(error):
    #returns a tuple, the pages and the 404 code 
    return render_template('error_pages/404.html'), 404

#add in any other error we want ( http and authorization errors and so on...)   
@error_pages.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html'), 403 