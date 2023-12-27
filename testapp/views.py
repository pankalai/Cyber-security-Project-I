from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from re import compile, search
import sqlite3


def index(request,notes=None):
    if "user_id" in request.session:
        if not notes:
            notes = get_notes(str(request.session.get("user_id", None)))
        users = get_users()
        return render(
            request,
            "index.html", 
            {
                "notes":notes,
                "users": users
            }
        )
    return redirect("/login")

def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        credit_card = request.POST.get('credit_card')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        """
        BROKEN AUTHENTICATION

        Weak passwords are easy to crack by experimenting.

        The following requires a password of at least eight characters, 
        with at least one lowercase letter, one uppercase letter and one number.

        reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$"
        pattern = compile(reg)
        valid = search(pattern, password)
        if not valid:
            return HttpResponse("Password too weak. Password must contain at least eight characters, with at least one lowercase letter, one uppercase letter and one number.")
        """
       
        text = """
            INSERT INTO users (first_name,last_name,username,password,credit_card,admin) 
            VALUES  (?,?,?,?,?,?)
        """

        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute(text, (first_name,last_name,username,password,credit_card,False))
        conn.commit()
        return redirect("/login")    

def login(request):
    if request.method == "GET":
        if "username" not in request.session:
            return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        text = "SELECT id,password,admin FROM users where username = ?"
        user = cursor.execute(text,[username]).fetchone()
  
        if not user:
            return HttpResponse("Unknown user")
        if user[1] != password:
            return HttpResponse("Wrong password")

        request.session["user_id"] = user[0]
        request.session["admin"] = user[2]
    return redirect("/")

def logout(request):
    if "admin" in request.session:
        del request.session["admin"]
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect("/")

def admin(request):
    """
    SECURITY MISCONFIGURATION

    Without checking rights, all users have access
    for a page intended for admins, which have
    information about all of the users.

    Adding a simple check this can be avoided.

    if not is_admin(request):
        raise PermissionDenied()
    """
    users = get_users()
    return render(request, "admin.html", {"users":users})

def get(request):
    note = request.GET.get('note')
    user_id = str(request.session.get("user_id", None))

    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    if note:
        text = "SELECT user_id, note FROM notes WHERE user_id = '%s' and note like '%%%s%%'" % (
            user_id,
            note
        )
    else:
        text = "SELECT user_id, note FROM notes WHERE user_id = '%s'" % user_id

    content = cursor.execute(text).fetchall()

    """
    SENSITIVE DATA EXPOSURE

    With sql injection vulnerability existing, input
    ' UNION SELECT 1,credit_card FROM users WHERE first_name like 'sam
    returns credit card number of another user unencrypted

    It must be encrypted before writing to the database,
    for example by using Fernet

    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    fernet = Fernet(key)
    credit_card = fernet.encrypt(credit_card.encode())
    """

    return render(
            request,
            "index.html", 
            {
                "notes":content,
            }
        )


def add(request):
    note = request.GET.get('note')
    user_id = str(request.session.get("user_id", None))

    if not note:
        return redirect("/")

    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    text = "INSERT INTO notes (user_id,note) VALUES (" + user_id + ",'" + note + "')"

    cursor.executescript(text)
    conn.commit()

    """
    INJECTION

    For example, with 'add' input
    '); DELETE FROM notes WHERE ('1'='1
    command clears table 'notes' 

    By providing input as a parameter and using the execute method,
    which executes only one command, the problem disappears

    text = "INSERT INTO notes (note) VALUES (?)"
    cursor.execute(text, [note])
    """
    return redirect("/")

def csrf(request):
    return render(request, "csrf.html")

def get_users():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    text = "SELECT first_name, last_name, username, credit_card FROM users"
    users = cursor.execute(text).fetchall()
    return users

def get_notes(user_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    text = "SELECT * FROM notes WHERE user_id = ?"
    content = cursor.execute(text, [user_id]).fetchall()
    return content

def is_admin(request):
    return request.session.get("admin", False)





