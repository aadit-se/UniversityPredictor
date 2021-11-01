from flask import render_template

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession


@app.route('/admin/viewDetection')
def adminViewDetection():
    try:
        if adminLoginSession() == "admin":
            return render_template('admin/viewDetection.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

# user
