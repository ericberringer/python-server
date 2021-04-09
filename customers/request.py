CUSTOMERS = [
    {
      "name": "Dirk Diggler",
      "address": "100 Fecal Street, Apt. 69",
      "email": "DigtheDirk@tushpush.biz",
      "id": 1
    },
    {
      "name": "Keiko BroHey",
      "address": "2950 Washington Street, Apt. Aja",
      "email": "KBro@heyko.gov",
      "id": 2
    },
    {
      "name": "Sage Klein",
      "address": "1600 Scort Court, Apt. 100",
      "email": "TurtlesandKatz@kleinhive.net",
      "id": 3
    },
    {
      "email": "Logan@Mustachio.biz",
      "address": "420 Rippin Way, Apt. Z",
      "name": "Logan Webb",
      "id": 4
    }
]

def get_all_customers():
    return CUSTOMERS

# Function with a single parameter
def get_single_customer(id):
    # Variable to hold the found customer, if it exists
    requested_customer = None

    # Iterate the CUSTOMER list above. Very similar to the
    # for..of loops you used in JavaScript.
    for customer in CUSTOMERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer