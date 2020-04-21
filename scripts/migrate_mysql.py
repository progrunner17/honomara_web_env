#!/usr/bin/env python3
import psycopg2
import mysql.connector
import re
import MeCab
import csv
from re import search
from psycopg2.extras import DictCursor
from psycopg2.errors import DuplicateColumn
from time import sleep

conn = psycopg2.connect('user=honomara dbname=honomara password=honomara')


def get_data(sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        data = cur.fetchall()
    return data


def get_data_dict(sql):
    with conn.cursor() as cur:
        cur.execute(sql)
        data = cur.fetchall()
        col_name = [col.name for col in cur.description]
    return [dict(zip(col_name, d)) for d in data]


def get_colname(table):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM {} LIMIT 1;'.format(table))
        data = [col.name for col in cur.description]
    return data


def exec_transaction(sql):
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def get_table_list():
    return [table[0] for table in get_data('SELECT relname FROM pg_stat_user_tables;')]


def get_sequence_list():
    return [seq[0] for seq in get_data('''SELECT c.relname FROM pg_class c LEFT join pg_user u ON c.relowner = u.usesysid WHERE c.relkind = 'S';''')]


def exec_transactions(sqls):
    with conn.cursor() as cur:
        for sql in sqls:
            cur.execute(sql)
    conn.commit()


conn2 = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='honomara',
    password='honomara',
    database='honomara',
)
cur2 = conn2.cursor(dictionary=True)


create_member_table = '''
CREATE TABLE IF NOT EXISTS member (
    `id`          INT          PRIMARY KEY AUTO_INCREMENT,
    `family_name` VARCHAR(30)  NOT NULL,
    `family_kana` VARCHAR(30),
    `first_name`  VARCHAR(30)  NOT NULL,
    `first_kana`  VARCHAR(30),
    `show_name`   VARCHAR(30)  NOT NULL,
    `kana`        VARCHAR(60)  NOT NULL, -- for index
    `year`        INT          NOT NULL,
    `sex`         INT          NOT NULL DEFAULT 0, -- 0=man, 1=woman
    `visible`     BOOL         NOT NULL DEFAULT true
);
'''

cur2.execute(create_member_table)
conn2.commit()


def name_len(name):
    l = len(name)
    l -= name.count(')')
    l -= name.count('(')
    l -= name.count('）')
    l -= name.count('（')
    return l


colname = get_colname('person')
mecab = MeCab.Tagger("-Ochasen")
regkana = re.compile(r'[ァ-ヶー]+')

for fields in get_data('SELECT * FROM person ORDER BY class;'):
    item = dict(zip(colname, fields))
    if not item['name']:
        name = item['fullname']
    elif not item['fullname']:
        name = item['name']
    elif name_len(item['fullname']) > name_len(item['name']):
        name = item['fullname']
    else:
        name = item['name']
    fam_n = re.match("^[^（()）]+", item['after_name']).group()

    fir_n = re.match("[^（()）　]*$", name.replace(fam_n, ''))
    if not fir_n or len(fir_n.group()) == 0:
        fir_n = '不明'
        parse_name = fam_n
    else:
        fir_n = fir_n.group()
        fir_n = fir_n.replace(' ', '')
        fir_n = fir_n.replace('　', '')
        parse_name = fam_n + fir_n
    if re.match(".*[（()）].*", name):
        after_name = name
    else:
        after_name = item['after_name']
    parse_result = mecab.parse(parse_name)
    kana_list = regkana.findall(parse_result.replace('\n', ' '))
    kana = ''.join(kana_list)
    year = item['class'] + 2000 - 9
    sex = '男' if item['sex'] == 0 else '女'
    cur2.execute('''
    INSERT INTO member (id,family_name,first_name,show_name,kana,year,sex,visible)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s);''', (item['person_id'], fam_n, fir_n, after_name, kana, year, item['sex'], item['visible']))

    parse_result = mecab.parse(parse_name)  # ふりがなを取得
    kana_list = regkana.findall(parse_result.replace('\n', ' '))
#         print(kana_list,d)
    if len(kana_list) == 0:
        print("[PARSE ERROR]", parse_name)
        continue
    else:
        # dd = cur2.execute('''SELECT member.kana, member.family_name, member.first_name FROM member WHERE id = {} ;'''.format(int(item['person_id'])))
        # d = cur2.fetchall()
        if not re.match(kana_list[0], kana):
            if len(kana_list) > 1 and re.search(kana_list[1] + '$', kana):
                first_kana = kana_list[1]
                family_kana = kana[:-len(first_kana)]
            else:
                continue
        else:
            family_kana = kana_list[0]
            first_kana = kana[len(family_kana):]
        cur2.execute('''UPDATE member SET family_kana = '{}', first_kana = '{}' WHERE id = {};'''.format(
            family_kana, first_kana, int(item['person_id'])))


conn2.commit()


# update the csv file !!!!!!!!
csv_path = "/vagrant/notebooks/member.csv"
# in most case this path would be /vagrant/notebooks/member.csv or like that

with open(csv_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur2.execute('''UPDATE member SET kana = '{}' WHERE id = {};'''.format(
            row['kana'], int(row['person_id'])))
conn2.commit()


mecab = MeCab.Tagger("-Ochasen")
regkana = re.compile(r'[ァ-ヶー]+')

csv_path = "/vagrant/notebooks/member.csv"
# in most case this path would be /vagrant/notebooks/member.csv or like that

with open(csv_path, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        dd = cur2.execute('''SELECT member.kana, member.family_name, member.first_name FROM member WHERE id = {} ;'''.format(
            int(row['person_id'])))
        d = cur2.fetchall()

        parse_result = mecab.parse("{} {}".format(
            d[0]['family_name'], d[0]['first_name']))
        kana_list = regkana.findall(parse_result.replace('\n', ' '))
#         print(kana_list,d)
        if len(kana_list) == 0:
            print("[PARSE ERROR]", row['kana'], d, row)
            continue
        else:
            if not re.match(kana_list[0], d[0]['kana']):
                if len(kana_list) > 1 and re.search(kana_list[1] + '$', d[0]['kana']):
                    first_kana = kana_list[1]
                    family_kana = d[0]['kana'][:-len(first_kana)]
                else:
                    if row['family_kana']:
                        family_kana = row['family_kana']
                        first_kana = row['first_kana']
                    else:
                        continue
            else:
                family_kana = kana_list[0]
                first_kana = d[0]['kana'][len(family_kana):]
            cur2.execute('''UPDATE member SET family_kana = '{}', first_kana = '{}' WHERE id = {};'''.format(
                family_kana, first_kana, int(row['person_id'])))
conn2.commit()


cur2.execute('''
ALTER TABLE member DROP COLUMN kana;
''')

conn2.commit()


# TRAINING


# add training_id
try:
    exec_transaction(''' CREATE SEQUENCE IF NOT EXISTS training_id_seq; ''')
    exec_transaction(
        '''ALTER TABLE training ADD COLUMN training_id integer NOT NULL DEFAULT nextval('training_id_seq');''')
except DuplicateColumn as err:
    print(err)
    conn = psycopg2.connect('user=honomara dbname=honomara password=honomara')


create_training_table = """
CREATE TABLE IF NOT EXISTS training (
    `id`      INT           PRIMARY KEY AUTO_INCREMENT,
    `date`    DATE          NOT NULL,
    `place`   VARCHAR(30)   NOT NULL,
    `weather` VARCHAR(30),
    `title`   VARCHAR(100)  NOT NULL,
    `comment` TEXT,
    INDEX USING BTREE (date)
);
"""

cur2.execute(create_training_table)
conn2.commit()


query = "INSERT INTO training (id,date,place,weather,title,comment) VALUES (%s,%s,%s,%s,%s,%s);"
for row in get_data_dict('SELECT * FROM training;'):
    data = (row['training_id'], str(row['date']), row['site'],
            row['weather'], row['subject'], row['comment'])
    cur2.execute(query, data)
conn2.commit()


# AFTER


exec_transaction('''CREATE SEQUENCE IF NOT EXISTS after_id_seq ;''')
try:
    exec_transaction(
        '''ALTER TABLE after ADD COLUMN after_id integer NOT NULL DEFAULT nextval('after_id_seq');''')
except DuplicateColumn as err:
    print(err)
    conn = psycopg2.connect('user=honomara dbname=honomara password=honomara')


create_restaurant_table = """
CREATE TABLE IF NOT EXISTS restaurant (
    id               INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_name  VARCHAR(30) NOT NULL,
    place            VARCHAR(30),
    comment TEXT
);
"""

cur2.execute(create_restaurant_table)
conn2.commit()


restaurant = get_data_dict('''
SELECT restaurant,site,avg(cost_max) AS cost_max,
avg(cost_min) AS cost_min , avg(number_max) AS n_max,
avg(number_min) AS n_min 
FROM after 
WHERE restaurant != '?' AND restaurant != '？' AND restaurant != ''
GROUP BY (restaurant,site) 
ORDER BY restaurant;
''')

cur2.execute(
    "INSERT INTO restaurant (restaurant_name,place,comment) VALUES ('Undefined','Undefined','Undefined');")
cur2.execute("UPDATE restaurant SET id = 0 WHERE  restaurant_name = 'Undefined' and place = 'Undefined' and comment = 'Undefined';")
for restaurant in restaurant:
    restaurant_name = restaurant['restaurant']
    if restaurant_name == '' or restaurant_name == '?' or restaurant_name == '？':
        continue
    else:
        print(restaurant_name)
    place = restaurant['site']
    comment = "費用目安 {}\n".format(
        int((restaurant['cost_max'] + restaurant['cost_min']) / 2))
    comment += "適正人数 {}人\n".format(
        int((restaurant['n_max'] + restaurant['n_min']) / 2))
    cur2.execute('INSERT INTO restaurant (restaurant_name,place,comment) VALUES (%s,%s,%s)',
                 (restaurant_name, place, comment))
conn2.commit()

create_after_table = """
CREATE TABLE IF NOT EXISTS after (
    `id`            INT PRIMARY KEY AUTO_INCREMENT,
    `date`          DATE NOT NULL,
    `after_stage`   INT NOT NULL DEFAULT 1,  
    `restaurant_id` INT NOT NULL, 
    `title`         VARCHAR(100) NOT NULL, 
    `comment`       TEXT,
    FOREIGN KEY (`restaurant_id`) REFERENCES restaurant(`id`),
    INDEX USING BTREE(`date`));
"""

cur2.execute(create_after_table)
conn2.commit()

for data in get_data_dict('SELECT * FROM after ORDER BY date;'):
    name = data['restaurant']
    if name == '' or name == '?' or name == '？':
        restaurant_id = 0
    else:
        cur2.execute('SELECT * FROM restaurant WHERE restaurant_name = %s AND place = %s',
                     (data['restaurant'], data['site']))
        restaurant_id = cur2.fetchall()[0]['id']
    id = data['after_id']
    date = data['date']
    after_stage = data['after']
    title = data['topic']
    comment = data['comment']
    cur2.execute('''
    INSERT INTO after (id,date,after_stage,restaurant_id,title,comment) 
    VALUES (%s,%s,%s,%s,%s,%s);''', (id, date, after_stage, restaurant_id, title, comment))

conn2.commit()


query = '''
ALTER TABLE restaurant ADD score float;
'''

cur2.execute(query)
query = '''
ALTER TABLE restaurant ALTER score SET DEFAULT 0;
'''
cur2.execute(query)

conn2.commit()

query = '''
UPDATE restaurant,
(
SELECT restaurant.id as id , count(after.id) as cnt
FROM after JOIN restaurant 
ON restaurant.id=after.restaurant_id
WHERE after.date >  '2015-01-01' 
GROUP BY restaurant.id
) AS items
SET restaurant.score = items.cnt
WHERE restaurant.id = items.id;
'''
cur2.execute(query)
conn2.commit()


# PARTICIPANTS

try:
    exec_transactions([
        '''ALTER TABLE participant ADD COLUMN after_id integer;''',
        '''ALTER TABLE participant ADD COLUMN training_id integer ''',
        '''ALTER TABLE participant ADD COLUMN origin varchar''',
    ])

    exec_transactions(['''
    UPDATE participant SET after_id = after.after_id, origin='after'
    FROM after WHERE participant.id = after.id;
    ''',
                       '''
    UPDATE participant SET training_id = training.training_id, origin='training'
    FROM training WHERE participant.id = training.id;
    '''])

except DuplicateColumn as err:
    print(err)
    conn = psycopg2.connect('user=honomara dbname=honomara password=honomara')

create_after_participant_table = '''
CREATE TABLE IF NOT EXISTS  after_participant (
    member_id   INT NOT NULL,
    after_id    INT NOT NULL
);
'''
create_training_participant_table = '''
CREATE TABLE IF NOT EXISTS  training_participant (
    member_id   INT NOT NULL,    
    training_id INT NOT NULL
);
'''

cur2.execute(create_after_participant_table)
cur2.execute(create_training_participant_table)
cur2.execute(
    '''ALTER TABLE after_participant ADD CONSTRAINT FOREIGN KEY (member_id) REFERENCES member(id);''')
cur2.execute(
    '''ALTER TABLE after_participant ADD CONSTRAINT  FOREIGN KEY (after_id) REFERENCES after(id);''')
cur2.execute(
    '''ALTER TABLE training_participant ADD CONSTRAINT  FOREIGN KEY (member_id) REFERENCES member(id);''')
cur2.execute(
    '''ALTER TABLE training_participant ADD CONSTRAINT  FOREIGN KEY (training_id) REFERENCES training(id);''')
conn2.commit()

for row in get_data_dict('SELECT * FROM participant;'):
    if row['origin'] == 'after':
        cur2.execute('INSERT INTO after_participant (member_id,after_id) VALUES (%s,%s);',
                     (row['person_id'], row['after_id']))
    elif row['origin'] == 'training':
        cur2.execute('INSERT INTO training_participant (member_id,training_id) VALUES (%s,%s);',
                     (row['person_id'], row['training_id']))
conn2.commit()


# RACE_AND_RESULT

create_race_base_table = '''
CREATE TABLE IF NOT EXISTS race_base (
    `race_name`      VARCHAR(60) PRIMARY KEY,
    `race_name_kana` VARCHAR(60),
    `prefecture`     VARCHAR(30),
    `comment`        TEXT
);
'''

create_race_table = '''
CREATE TABLE IF NOT EXISTS race (
    `id`        INT PRIMARY KEY AUTO_INCREMENT,
    `race_name` VARCHAR(60) NOT NULL,
    `date`      DATE NOT NULL,
    `comment`   TEXT
);
'''
create_race_type_table = '''
CREATE TABLE IF NOT EXISTS race_type (
    `id`         INT PRIMARY KEY AUTO_INCREMENT,
    `race_type`  VARCHAR(30) NOT NULL DEFAULT 'road', 
    `show_name`  VARCHAR(30), 
    `ranking`    INT NOT NULL DEFAULT 100, 
    `duration`   FLOAT,
    `distance`   FLOAT,
    `comment`    TEXT
);
'''

create_result_table = '''
CREATE TABLE IF NOT EXISTS result (
    `member_id`     INT NOT NULL, 
    `race_type_id`  INT NOT NULL, 
    `race_id`       INT NOT NULL, 
    `result`        INT NOT NULL,
    `comment`       TEXT
);
'''

cur2.execute(create_race_base_table)
cur2.execute(create_race_table)
cur2.execute(create_race_type_table)
cur2.execute(create_result_table)
conn2.commit()
#cur2.execute('''ALTER TABLE race ADD CONSTRAINT FOREIGN KEY (race_name) REFERENCES race_base(race_name);''')
cur2.execute(
    '''ALTER TABLE result ADD CONSTRAINT FOREIGN KEY (member_id)    REFERENCES member(id);''')
cur2.execute(
    '''ALTER TABLE result ADD CONSTRAINT FOREIGN KEY (race_type_id) REFERENCES race_type(id);''')
cur2.execute(
    '''ALTER TABLE result ADD CONSTRAINT FOREIGN KEY (race_id)      REFERENCES race(id);''')
conn2.commit()


ds = get_data('SELECT DISTINCT race_name FROM race;')
ds = [(d[0].strip()) for d in ds]  # if re.match('横浜',d[0])]
ds = set(ds)
ds = list(ds)
ds.sort()
prev = ''
# for d in ds:
#     if prev[:5:] == d[:5:]:
#         print(d,prev)
#     prev = d


table = {}
table["いたばしリバーサイド・ハーフマラソン"] = "いたばしリバーサイドハーフマラソン"
table["おきなわマラソン_"] = "おきなわマラソン"
table["戸田・彩湖フルマラソン&ウルトラマラソン"] = "戸田・彩湖フルマラソン＆ウルトラマラソン"
ds = [table.get(d, d) for d in ds]
ds = set(ds)
ds = list(ds)
ds.sort()

for d in ds:
    cur2.execute('INSERT INTO race_base (race_name) VALUES (%s);', (d,))

conn2.commit()


table = {}
table["いたばしリバーサイド・ハーフマラソン"] = "いたばしリバーサイドハーフマラソン"
table["おきなわマラソン_"] = "おきなわマラソン"
table["戸田・彩湖フルマラソン&ウルトラマラソン"] = "戸田・彩湖フルマラソン＆ウルトラマラソン"

n = get_data('SELECT count(*) FROM race; ')[0][0]
ofst = 0
limit = n
while ofst < n:
    ds = get_data_dict('SELECT race_id,race_name,date FROM race ORDER BY race_id OFFSET {ofst} LIMIT {lmt};'.format(
        ofst=ofst, lmt=limit))
    for d in ds:
        d['race_name'] = table.get(d['race_name'], d['race_name']).strip()
#         print(d)
        cur2.execute('INSERT INTO race (id, race_name, date) VALUES (%s,%s,%s);',
                     (d['race_id'], d['race_name'], d['date']))
    ofst += limit
conn2.commit()

ds = get_data_dict('''
SELECT distance_id AS race_type_id, distance AS distance, distance_name AS show_name, ranking  FROM distance ORDER BY ranking;
''')
time = list(filter(lambda d: search('時間', d['show_name']), ds))
road = list(filter(lambda d: search('マラソン|キロ|マイル', d['show_name']), ds))
track = list(filter(lambda d: search('メートル', d['show_name']), ds))

# print(len(ds))
# print(len(time))
# print(len(road))
# print(len(track))

for t in time:
    t['duration'] = float(t['show_name'].replace('時間走', '')) * 3600
    t['distance'] = None
    t['race_type'] = 'time'
    print(t)
    cur2.execute('''INSERT INTO race_type (id, race_type, duration, show_name, ranking) VALUES (%s,%s,%s,%s,%s);''',
                 (t['race_type_id'], t['race_type'], t['duration'], t['show_name'], t['ranking']))


for t in track:
    t['race_type'] = 'track'
    t['distance'] = float(t['distance'])
    print(t)
    cur2.execute('''INSERT INTO race_type (id, race_type, duration, show_name, ranking) VALUES (%s,%s,%s,%s,%s);''',
                 (t['race_type_id'], t['race_type'], t['distance'], t['show_name'], t['ranking']))


for t in road:
    t['distance'] = float(t['distance'])
    t['race_type'] = 'road'
    print(t)
    cur2.execute('''INSERT INTO race_type (id, race_type, duration, show_name, ranking) VALUES (%s,%s,%s,%s,%s);''',
                 (t['race_type_id'], t['race_type'], t['distance'], t['show_name'], t['ranking']))
conn2.commit()

n = get_data('SELECT count(*) FROM result; ')[0][0]
print(n)
ofst = 0
limit = 10
while ofst < n:
    ds = get_data_dict('''
    SELECT person_id as member_id, race_id, distance_id as race_type_id,time as result, display_time, comment FROM result
    ORDER BY race_id OFFSET {ofst} LIMIT {lmt};
    '''.format(ofst=ofst, lmt=limit))
    for d in ds:
        if not d['result']:
            print(d)
            continue

        sss = int(d['result'].total_seconds())
        strsss = '{:02}:{:02}:{:02}'.format(
            sss//3600, sss % 3600//60, sss % 60)
        if not re.search(d['display_time'], strsss):
            comment = 'note:"{}" {}'.format(
                d['display_time'], '' if d['comment'] is None else d['comment'])
        else:
            comment = '' if d['comment'] is None else d['comment']
        cur2.execute('''INSERT INTO result (member_id, race_id, race_type_id, result, comment) VALUES (%s,%s,%s,%s,%s);''',
                     (d['member_id'], d['race_id'], d['race_type_id'], int(d['result'].total_seconds()), comment))

    ofst += limit
conn2.commit()
