from flask_login import current_user, LoginManager, UserMixin

class User(UserMixin):
    
    def __init__(self, user_email=None, user_password=None, db=None):
        self.authenticated = False
        self.email = None
        self.password = None

        if db and user_email and not user_password:
            cur = db.connection.cursor()
            cur.execute("SELECT `__user`.`user_id`," 
                + " `__user`.`user_name`,"
                + "`__user`.`user_username`,"
                + " `__user`.`user_password`"
                + " FROM `wms`.`__user`"
                + " WHERE `__user`.`user_username` = %s", [user_email])
            
            data = cur.fetchall()

            if not data: 
                cur.close()
                self.authenticated = False
                return 
        
            ((_, self.__user_name, self.__user_email, self.__user_password),) = data
            cur.close()
            self.authenticated = False
            self.email = user_email
            self.password = None
        elif db and user_password and user_email:
            cur = db.connection.cursor()
            cur.execute("SELECT `__user`.`user_id`," 
                + " `__user`.`user_name`,"
                + "`__user`.`user_username`,"
                + " `__user`.`user_password`"
                + " FROM `wms`.`__user`"
                + " WHERE `__user`.`user_username` = (%s) AND `__user`.`user_password` = (%s)", (user_email, user_password))
            
            data = cur.fetchall()
            if not data: 
                self.authenticated = False
                cur.close()
                return

            ((_, self.__user_name, self.__user_email, self.__user_password),) = data
  
            cur.close()

            if  self.__user_email == user_email and self.__user_password == user_password:
                self.authenticated = True

        

    @classmethod
    def get(cls, user_id=None, db=None):
        if user_id and db:
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM `wms`.`__user` WHERE `__user`.`user_username` = %s", [user_id])
            data = cur.fetchall()
            if not data: 
                return None
            (( _, username, user_email,_), ) = data
            
            return User(username, user_email, db)
        else:
            return None

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.__user_email

    def get_user_name(self):
        return self.__user_name