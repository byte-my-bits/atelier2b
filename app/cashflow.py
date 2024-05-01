from datetime import datetime
import uuid
import json



# CashFlow class
class CashFlow():

    with open('../settings/cashflow_categories.json', 'r') as f:
        VALID_CATEGORIES = json.load(f)['cashflow']

    def __init__(self, amount, description, category, subcategory, user_id, id="", date=None):
        # Main initialiser
        self.amount = amount
        self.description = description
        self.category , self.subcategory = self.validate_category(category, subcategory)
        self.user_id = user_id
        self.id = uuid.uuid4().hex if not id else id
        self.date = date if date else datetime.now()

    @classmethod
    def validate_category(cls, category,subcategory):
        # Validate category against list of valid categories
        for main_category in cls.VALID_CATEGORIES:
            if isinstance(cls.VALID_CATEGORIES[main_category], dict):
                for sub_category in cls.VALID_CATEGORIES[main_category]:
                    if subcategory in cls.VALID_CATEGORIES[main_category][sub_category]:
                        return category,subcategory
        return None,None

    @classmethod
    def make_from_dict(cls, d):
        # Initialise Expense object from a dictionary
        return cls(d['amount'], d['description'], d['category'], d['subcategory'], d['user_id'], d['id'], d['date'])

    def dict(self):
        # Return dictionary representation of the object
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "user_id": self.user_id,
            "date": self.date
        }