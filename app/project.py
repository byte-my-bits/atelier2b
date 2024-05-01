from datetime import datetime
import uuid

class Project():
    def __init__(self, name, type, client, client_address, current_user, project_structure, id="" ):
        # Main initialiser
        self.owner = current_user['id']
        self.id = uuid.uuid4().hex if not id else id
        self.creation_date = datetime.now()
        self.type = type

        self.data = project_structure

        self.data['informatii_generale']['an_proiect'] =  datetime.now().year
        self.data['informatii_generale']['titlu_proiect'] =  name
        self.data['informatii_generale']['beneficiar'] =  client
        self.data['informatii_generale']['adresa_beneficiar'] =  client_address
        self.data['informatii_generale']['proiectant_general'] =  "Atelier 2Ba"
        self.data['informatii_generale']['sediu_proiectant'] =  "Str. Orest Tafrali 3, Iasi 700495"
        
        
    
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
    

    
