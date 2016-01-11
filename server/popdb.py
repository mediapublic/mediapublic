import json
import os
import subprocess
import uuid

def pop_db(sql):
    with open('temp.sql', 'w') as f:
        f.write(sql)
    cli = [
        'sqlite3',
        'mediapublic.sqlite',
        '<',
        'temp.sql',
    ]
    #print(' '.join(cli))
    os.system(' '.join(cli))
    #os.remove('temp.sql')

def read_orgs():
    with open('orgs.json', 'r') as f:
        orgs = json.loads(f.read())
    return orgs

def create_sql(orgs):
    sql = ''
    for org in orgs:
        _fields = [
            'short_name',
            'long_name',
            'long_description',
            'address_0',
            'address_1',
            'city',
            'state',
            'zipcode',
            'phone',
            'fax',
            'primary_website',
            'secondary_website',
            'image_url',
        ]
        _values = [
            org['station'],
            '',
            '',
            '',
            '',
            org['town'],
            org['state'],
            '',
            '',
            '',
            org['website'],
            '',
            '',
        ]
        fields = 'id, '
        values = '"%s", ' % str(uuid.uuid4()).replace('-','')
        for index in range(0,len(_fields)):
            fields += '%s, ' % _fields[index]
            values += '"%s", ' % _values[index]
        fields = fields[:-2]
        values = values[:-2]
        sql += 'insert into organizations(%s) values(%s);\n' % (fields, values)
    return sql

if __name__ == '__main__':

    orgs = read_orgs()
    sql = create_sql(orgs)
    pop_db(sql)
