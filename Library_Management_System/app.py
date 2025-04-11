from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Rutwik',
    database='library_db'
)
cursor = db.cursor()

def is_admin_or_employee():
    return session.get('role') in ['admin', 'employee']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        table = role.capitalize()
        cursor.execute(f"SELECT * FROM {table} WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            session['role'] = role
            return redirect(url_for(f'{role}_dashboard'))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO Member (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/employee/dashboard')
def employee_dashboard():
    if session.get('role') != 'employee':
        return redirect(url_for('login'))
    return render_template('employee_dashboard.html')


@app.route('/member/dashboard')
def member_dashboard():
    if session.get('role') != 'member':
        return redirect(url_for('login'))
    return render_template('member_dashboard.html')

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM Author")
    authors = cursor.fetchall()
    cursor.execute("SELECT * FROM Publisher")
    publishers = cursor.fetchall()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        publisher_id = request.form['publisher_id']
        quantity = request.form['quantity']
        cursor.execute("INSERT INTO Book (title, author_id, publisher_id, quantity) VALUES (%s, %s, %s, %s)",
                    (title, author_id, publisher_id, quantity))
        db.commit()
        return redirect(url_for('manage_books'))
    return render_template('add_book.html', authors=authors, publishers=publishers)

@app.route('/admin/add-member', methods=['GET', 'POST'])
def add_member():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor.execute("INSERT INTO Member (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        db.commit()
        return redirect(url_for('view_members'))
    return render_template('add_member.html')

@app.route('/admin/view-members')
def view_members():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM Member")
    members = cursor.fetchall()
    return render_template('view_members.html', members=members)

@app.route('/admin/delete-member/<int:member_id>')
def delete_member(member_id):
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("DELETE FROM Member WHERE id=%s", (member_id,))
    db.commit()
    return redirect(url_for('view_members'))

@app.route('/manage-books')
def manage_books():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor = db.cursor(dictionary=True)
    cursor.execute("""SELECT Book.id, Book.title, Author.name AS author, Publisher.name AS publisher, Book.quantity 
                      FROM Book
                      JOIN Author ON Book.author_id = Author.id 
                      JOIN Publisher ON Book.publisher_id = Publisher.id""")
    books = cursor.fetchall()
    cursor.close()
    return render_template('manage_books.html', books=books)

@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM Author")
    authors = cursor.fetchall()
    cursor.execute("SELECT * FROM Publisher")
    publishers = cursor.fetchall()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        publisher_id = request.form['publisher_id']
        quantity = request.form['quantity']
        cursor.execute("UPDATE Book SET title=%s, author_id=%s, publisher_id=%s, quantity=%s WHERE id=%s",
                       (title, author_id, publisher_id, quantity, book_id))
        db.commit()
        return redirect(url_for('manage_books'))

    cursor.execute("SELECT * FROM Book WHERE id=%s", (book_id,))
    book = cursor.fetchone()
    return render_template('edit_book.html', book=book, authors=authors, publishers=publishers)

@app.route('/delete-book/<int:book_id>')
def delete_book(book_id):
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("DELETE FROM Book WHERE id=%s", (book_id,))
    db.commit()
    return redirect(url_for('manage_books'))

@app.route('/admin/authors')
def view_authors():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("SELECT id, name FROM Author")
    authors = cursor.fetchall()
    return render_template('authors.html', authors=authors)

@app.route('/admin/publishers')
def view_publishers():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("SELECT id, name FROM Publisher")
    publishers = cursor.fetchall()
    return render_template('publishers.html', publishers=publishers)

@app.route('/view-reservations')
def view_reservations():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM Reservation")
    reservations = cursor.fetchall()
    return render_template('view_reservations.html', reservations=reservations)

@app.route('/admin/vendors')
def manage_vendors():
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM Vendor")
    vendors = cursor.fetchall()
    return render_template('manage_vendors.html', vendors=vendors)

@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    if not is_admin_or_employee():
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        cursor.execute("INSERT INTO Vendor (name, contact) VALUES (%s, %s)", (name, contact))
        db.commit()
        return redirect(url_for('manage_vendors'))

    return render_template('add_vendor.html')

@app.route('/admin/vendor/delete/<int:vendor_id>')
def delete_vendor_by_id(vendor_id):
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("DELETE FROM Vendor WHERE id=%s", (vendor_id,))
    db.commit()
    return redirect(url_for('manage_vendors'))

@app.route('/member/view-books')
def view_books():
    if session.get('role') != 'member':
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM Book")
    books = cursor.fetchall()
    return render_template('view_books.html', books=books)

@app.route('/member/reserve-book', methods=['GET', 'POST'])
def reserve_book():
    if session.get('role') != 'member':
        return redirect(url_for('login'))
    if request.method == 'POST':
        book_id = request.form['book_id']
        username = session['username']
        cursor.execute("SELECT id FROM Member WHERE username=%s", (username,))
        member = cursor.fetchone()
        if member:
            cursor.execute("INSERT INTO Reservation (book_id, member_id, reservation_date) VALUES (%s, %s, CURDATE())", (book_id, member[0]))
            db.commit()
            return "Book reserved successfully!"
    cursor.execute("SELECT * FROM Book")
    books = cursor.fetchall()
    return render_template('reserve_book.html', books=books)

@app.route('/member/my-fines')
def my_fines():
    if session.get('role') != 'member':
        return redirect(url_for('login'))
    username = session['username']
    cursor.execute("SELECT id FROM Member WHERE username=%s", (username,))
    member_id = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Fine WHERE member_id=%s", (member_id,))
    fines = cursor.fetchall()
    return render_template('my_fines.html', fines=fines)

@app.route('/admin/fines')
def manage_fines():
    if not is_admin_or_employee():
        return redirect(url_for('login'))

    cursor.execute("""
        SELECT Fine.id, Member.username, Fine.amount, Fine.reason, Fine.date_assessed
        FROM Fine
        JOIN Member ON Fine.member_id = Member.id
    """)
    fines = cursor.fetchall()
    return render_template('manage_fines.html', fines=fines)

@app.route('/admin/fine/add', methods=['GET', 'POST'])
def add_fine():
    if not is_admin_or_employee():
        return redirect(url_for('login'))

    cursor.execute("SELECT id, username FROM Member")
    members = cursor.fetchall()

    if request.method == 'POST':
        member_id = request.form['member_id']
        amount = request.form['amount']
        reason = request.form['reason']
        date_assessed = request.form['date_assessed']

        cursor.execute(
            "INSERT INTO Fine (member_id, amount, reason, date_assessed) VALUES (%s, %s, %s, %s)",
            (member_id, amount, reason, date_assessed)
        )
        db.commit()
        return redirect(url_for('manage_fines'))

    return render_template('add_fine.html', members=members)

@app.route('/admin/fine/delete/<int:fine_id>')
def delete_fine(fine_id):
    if not is_admin_or_employee():
        return redirect(url_for('login'))
    cursor.execute("DELETE FROM Fine WHERE id=%s", (fine_id,))
    db.commit()
    return redirect(url_for('manage_fines'))

if __name__ == '__main__':
    app.run(debug=True)
