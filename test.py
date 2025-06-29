import random
import datetime

def generate_random_string(inputstr, length=6):
    data = random.choices(inputstr,k=length)
    return ''.join(data)


print(generate_random_string("NaveenkumarVR",4))
print(datetime.datetime.now())