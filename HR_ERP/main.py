import MySQLdb
from flask import Flask, render_template, request ,redirect , url_for ,session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key='marco'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='hr_erp'

conn=MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin_dashboard_login')
def admin_dashboard_login():
    return render_template('admin_dashboard_login.html')


@app.route('/admin_dashboard_screen', methods=['POST','GET'])
def admin_dashboard_screen():

    # Agar already login hai to direct dashboard dikhao
    if session.get('admin_logged_in'):

        cursor = conn.connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM emp_data")
        total = cursor.fetchone()[0]
        print(total)

        cursor.execute("SELECT COUNT(*) FROM emp_data WHERE LOWER(emp_gender) = 'male'")
        male = cursor.fetchone()[0]
        print(male)

        cursor.execute("SELECT COUNT(*) FROM emp_data WHERE LOWER(emp_gender) = 'female'")
        female = cursor.fetchone()[0]
        print(female)

        cursor.execute("SELECT emp_dept, COUNT(*) FROM emp_data GROUP BY emp_dept")
        departments = cursor.fetchall()

        cursor.close()

        return render_template(
            'admin_dashboard_screen.html',
            total=total,
            male=male,
            female=female,
            departments=departments
        )

    # Agar login attempt ho raha hai
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pass')

        if username == "admin" and password == "marco":
            session['admin_logged_in'] = True
            return redirect("/admin_dashboard_screen")
        else:
            session['admin_logged_in'] = False
            return redirect("/admin_dashboard_login")

    return redirect(url_for('admin_dashboard_login'))

@app.route('/employee_dashboard_login')
def employee_dashboard_login():
    return render_template('employee_dashboard_login.html')



@app.route('/employee_dashboard', methods=['POST'])
def employee_dashboard():

    email = request.form.get('email')
    if not email:
        return "email is required"
    email = email.strip()
    print("email entered", email)
    cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM emp_data WHERE emp_email = %s", (email,))
    employee = cursor.fetchone()
    cursor.close()
    print("query result", employee)
    if employee:
        return render_template('employee_dashboard.html', employee=employee)
    else:
        return "employee not found"


@app.route('/add_employee')
def add_employee():
    print(session.get('admin_dashboard_login'))
    if not session.get('admin_logged_in'):
        return redirect('/')
    else:
        return render_template('add_employee.html')

@app.route('/registration',methods=['post'])
def registration():
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    gender = request.form.get('gender')
    photo = request.form.get('photo')
    skills = request.form.get('skills')
    department = request.form.get('department')

    my_cursor = conn.connection.cursor()
    q="""
    INSERT INTO emp_data(emp_name,emp_email,emp_mobile,emp_gender,emp_photo,emp_skill,emp_dept) VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    v=(name,email,mobile,gender,photo,skills,department)
    my_cursor.execute(q,v)

    conn.connection.commit()
    my_cursor.close()

    return render_template('registration.html', name=name, email=email, mobile=mobile , gender=gender, photo=photo,
                           skills=skills, department=department)



@app.route('/edit_employee')
def edit_employee():
    if not session.get('admin_logged_in'):
        return redirect("/")
    cursor = conn.connection.cursor()
    cursor.execute("SELECT * FROM emp_data")
    list_employees = cursor.fetchall()

    return render_template('edit_employee.html', list_employees=list_employees)

@app.route('/delete_employee')
def delete_employee():
    if not session.get('admin_logged_in'):
        return redirect('/')
    my_cursor = conn.connection.cursor()
    my_cursor.execute("SELECT * FROM emp_data")
    data = my_cursor.fetchall()
    my_cursor.close()
    return render_template("delete_employee.html", list_employees=data)



@app.route('/search_employee')
def search_employee():
    if not session.get('admin_logged_in'):
        return redirect('/')
    return render_template('search_employee.html')

@app.route('/show_all')
def show_employee():
    if not session.get('admin_logged_in'):
        return redirect('/')
    my_cursor = conn.connection.cursor()
    my_cursor.execute("SELECT * FROM emp_data")
    print("Select all query")
    list_employee = my_cursor.fetchall()

    return render_template('show_all.html',list_employee=list_employee)

@app.route('/edit_record')
def edit_record():
    record_id=request.args.get('eid')
    my_cursor2 = conn.connection.cursor()
    my_cursor2.execute("SELECT * FROM emp_data where eid=%s",(record_id,))
    print("Selected Record is here!")
    selected_emp=my_cursor2.fetchone()

    return render_template('edit_record.html',selected_emp=selected_emp)

@app.route('/delete_record', methods=['POST'])
def delete_record():
    del_id = request.form.get('eid')
    if del_id:
        my_cursor = conn.connection.cursor()
        my_cursor.execute("DELETE FROM emp_data WHERE eid=%s", (del_id,))
        conn.connection.commit()
        my_cursor.close()
        print("Record Deleted Successfully!")

    return redirect(url_for('delete_employee'))

@app.route('/update_record',methods=['POST'])
def update_record():
    update_id=request.form.get('eid')
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')

    gender = request.form.get('gender')
    photo = request.form.get('photo')
    skills = request.form.get('skills')
    department = request.form.get('department')
    my_cursor3 = conn.connection.cursor()
    my_cursor3.execute("UPDATE emp_data set emp_name=%s,  emp_email=%s,emp_mobile=%s, emp_gender=%s, emp_photo=%s, emp_skill=%s, emp_dept=%s where eid=%s",(name,mobile,email,gender,photo,skills,department,update_id))
    conn.connection.commit()
    print("Record Updated Successfully!")

    return render_template('update_record.html',update_id=update_id)

@app.route('/found_data', methods=['get'])
def found_data():
    eid = request.args.get('emp_id')
    print(eid)
    if not eid:
        return "NO id provided!"
    my_cursor = conn.connection.cursor()
    my_cursor.execute("SELECT * FROM emp_data where eid=%s", (eid,))
    data = my_cursor.fetchone()
    print("fetched:",data)

    if data is None:
        return "No data found!"
    return render_template('found_data.html', employee=data)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('/index.html')
app.run(debug=True)
