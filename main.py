import TxtDatabase2
import random
db = TxtDatabase2.Database("db.txt")

print(db.get_variables("names", 10, 90))