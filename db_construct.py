import app
    
"""
db.create_all()
user = User('John Doe', 'john.doe@example.com')
db.session.add(user)
db.session.commit()
"""

f = open('db_example.txt', 'r')
content = f.read().splitlines()
for i in content:
    lst = i.split()
    ct = app.User(lst[0],lst[1])
    app.db.session.add(ct)
    app.db.session.commit()
f.close()
