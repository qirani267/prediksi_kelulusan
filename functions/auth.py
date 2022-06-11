from flask import redirect, render_template, session, request

def init(app, mysql):

    @app.route('/', methods=['GET'])
    def index():
        if not session.get("login_by_admin") is None:
            return redirect('/admin')
        if not session.get("login_by_user") is None:
            return redirect('/user')

        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login():
        con = mysql.connect()
        cursor = con.cursor()
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        cursor.execute(query, (str(request.form.get('username')),
                       str(request.form.get('password'))))
        rows = cursor.fetchone()
        cursor.close()

        if rows:
            session["login_by_admin"] = True
            session["user"] = rows[1]
            session["id"] = rows[0]
            session["role"] = 1
            return redirect('/admin')
        else:
           return render_template('login.html', msg="Username & Password sepertinya salah!!")
            
    @app.route('/logout', methods=['GET'])
    def logout():
        session["login_by_admin"] = None
        session["login_by_user"] = None
        return redirect('/')
