from app import app, login_manager
from app import chat_db as db
#from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt

mybcrypt = Bcrypt(app)

class User:
    def __init__(self,username, password_hash,is_active):
        self.username = username
        self.password_hash = password_hash
        #self.authenticated =False
        self.is_active = is_active
        self.is_anonymous = False
    
    def get_id(self):
        return self.username
    
    def is_authenticated(self):
        return self.is_active

    def get_user(username):
        conn = db.connect_db()
        cur = conn.cursor()
        cur.execute('select username,password, active from chatgpt.users where username = %s', (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return User(row[0], row[1],row[2]) 
        else:
            return None
    
    def check_password(password, password_hash):
        return mybcrypt.check_password_hash(password_hash, password)
    
    # not going to pass password yet
    def create_user(username, password):
        active = True
        hash = mybcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = db.connect_db()
            cur = conn.cursor()
            cur.execute(db.insert_user,(username,hash,active))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(e)
            return e


@login_manager.user_loader
def load_user(username):
    return User.get_user(username)