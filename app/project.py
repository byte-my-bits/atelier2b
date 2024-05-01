from datetime import datetime
import uuid

class Project():
    def __init__(self, name, type, address, current_user, id="" ):
        # Main initialiser
        self.name = name
        self.type = type
        self.owner = current_user['id']
        self.members = [current_user]
        self.address = address        
        self.id = uuid.uuid4().hex if not id else id
        self.creation_date = datetime.now()
        self.invite_token = f"{uuid.uuid4().hex[:8]}" if not id else id
        
        print(f"+-----------------------------------------------------+")
        print(f"![Debug]! Name: {self.name}")
        print(f"![Debug]! Type: {self.type}")
        print(f"![Debug]! Owner: {self.owner}")
        print(f"![Debug]! Members: {self.members}")
        print(f"![Debug]! Address: {self.address}")
        print(f"![Debug]! ID: {self.id}")
        print(f"![Debug]! Creation Date: {self.creation_date}")
        print(f"![Debug]! Invite Token: {self.invite_token}")
        print(f"+-----------------------------------------------------+")
        
    
    @classmethod
    def make_fromdict(cls,d):
        # Initialise Household object from a dictionary
        return cls(d['name'], d['type'], d['members'], d['address'], d['id'])
    
    def dict(self):
        # Return dictionary representation of the object
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "members": self.members,
            "owner": self.owner,
            "address": self.address,
            "created": str(self.creation_date),
            "invite_token": self.invite_token
        }
    def add_member(self, member):
        # Add new member to project
        self.members.append(member)
    
    def remove_member(self, member):
        # Remove member from project
        self.members.remove(member)

    def display_name(self):
        # Return name
        return self.name
    
    def display_type(self):
        # Return type
        return self.type

    def display_members(self):  
        # Return members
        return self.members
    
    def display_address(self):
        # Return address
        return self.address
    
    def get_id(self):
        return self.id
    

    
