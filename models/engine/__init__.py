from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

serializable = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}