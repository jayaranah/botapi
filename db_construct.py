import app
import sys
from re import search
    
"""
db.create_all()
user = User('John Doe', 'john.doe@example.com')
db.session.add(user)
db.session.commit()
"""

def construct(table_name, path_txt):
    f = open('db_example.txt', 'r')
    content = f.read().splitlines()
    f.close()
    for i in content:
        if table_name == 'Daftar_Tag':
            lst_re = search(r'(.*)\;\s+(\S*)\s+(\S*)\s+(\S*)', i)
            cm = app.Daftar_Tag(lst_re.group(1),lst_re.group(2),lst_re.group(3),lst_re.group(4))
        elif (table_name == 'Daftar_Jurus') or (table_name == 'Helper'):
            lst_re = search(r'(.*)\;\s+(\S*)', i)
            f_g2 = open(lst_re.group(2), 'r')
            g2_txt = f_g2.read()
            f_g2.close()
            cm = app.Daftar_Jurus(lst_re.group(1),g2_txt)
        else:
            print('There is no ' + table_name + ' table, please re-check your argument')
            sys.exit(1)
        app.db.session.add(cm)
        app.db.session.commit()    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python db_construct.py <table_name> <path_txt>')
        sys.exit(1)
    table_name = sys.argv[1]
    path_txt = sys.argv[2]
    construct(table_name, path_txt)
