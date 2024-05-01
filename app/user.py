from datetime import datetime
import uuid


# User class
class User():
    def __init__(self, first_name, last_name, role, email, id="", verified=False):
        # Main initialiser
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = uuid.uuid4().hex if not id else id
        self.verified = verified
        self.creation_date = datetime.now()
        self.role = role
    

    @classmethod
    def make_from_dict(cls, d):
        # Initialise User object from a dictionary
        print("############################################### DEBUG: make_from_dict")
        ret_value = cls(d['first_name'], d['last_name'], d['role'], d['email'], d['id'], d['verified'])
        print(ret_value)
        print("############################################### DEBUG: make_from_dict")
        return ret_value

    def dict(self):
        # Return dictionary representation of the object
        print("############################################### DEBUG: dict")
        print(self.role)
        print("############################################### DEBUG: dict")
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role" : self.role,
            "email": self.email,
            "verified": self.verified         
        }

    def display_name(self):
        # Return concatenation of name components
        return self.first_name + " " + self.last_name

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


# Anonymous user class
class Anonymous():

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None
