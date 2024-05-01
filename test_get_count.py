#!/Users/jasonhucks/.venv/bin/python
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.user import User

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))