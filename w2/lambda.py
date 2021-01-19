people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "asian", "house": "balls"},
    {"name": "jj", "house": "beef"}
]


# def f(person):
#     return person["name"]


# people.sort(key=f)

people.sort(key=lambda person: person["name"])

print(people)
