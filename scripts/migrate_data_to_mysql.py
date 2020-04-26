import psycopg2
import mysql.connector
import re
import MeCab
import csv
from re import search
from psycopg2.extras import DictCursor
from psycopg2.errors import DuplicateColumn, IntegrityError


class Postgres:
    conn = None
    cur = None

    def __init__(self, user='honomara', database='honomara', password='honomara'):
        self.conn = psycopg2.connect(
            'user={} dbname={} password={}'.format(user, database, password))

    def query(self, sql, dictionary=True, fetch=False):
        with self.conn.cursor() as cur:
            cur.execute(sql)
            if fetch:
                data = cur.fetchall()
                if dictionary:
                    col_name = [col.name for col in cur.description]
                    data = [dict(zip(col_name, d)) for d in data]
                return data

    def commit(self):
        self.conn.commit()

    def __del__(self):
        self.conn.close()


class Mysql:
    conn = None
    cur = None

    def __init__(self, user='honomara', database='honomara', password='honomara'):
        self.conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user=user,
            password=password,
            database=database,
        )

    def query(self, sql, tpl=None, dictionary=True, fetch=False):
        if self.cur is None:
            self.cur = self.conn.cursor(dictionary=dictionary)
        if tpl is not None:
            self.cur.execute(sql, tpl)
        else:
            self.cur.execute(sql)
        if fetch:
            return self.cur.fetchall()

    def commit(self):
        self.conn.commit()


msql = Mysql()
psql = Postgres()


def name_len(name):
    l = len(name)
    l -= name.count(')')
    l -= name.count('(')
    l -= name.count('）')
    l -= name.count('（')
    return l


def get_names(item):
    if not item['name']:
        name = item['fullname']
    elif not item['fullname']:
        name = item['name']
    elif name_len(item['fullname']) > name_len(item['name']):
        name = item['fullname']
    else:
        name = item['name']
    fam_n = re.match("^[^（()）]+", item['after_name']).group()  # アフター名からカッコを除いた
    fir_n = re.match("[^（()）　]*$", name.replace(fam_n, ''))
    if not fir_n or len(fir_n.group()) == 0:
        fir_n = ''
        parse_name = fam_n
    else:
        fir_n = fir_n.group()
        fir_n = fir_n.replace(' ', '')
        fir_n = fir_n.replace('　', '')
        parse_name = fam_n + fir_n

    if re.match(".*[（()）].*", name):
        after = name
    else:
        after = item['after_name']

    return fam_n, fir_n, after


def get_kana(family, first, after=None):
    mecab = MeCab.Tagger("-Ochasen")
    regkana = re.compile(r'[ァ-ヶー]+')
    name = family + first if first else family
    if re.match('[ァ-ヶー]+', name):  # 変換不要
        return name, name, None
    parse_result = mecab.parse(name)
    parse_result = parse_result.replace('\n', ' ')
    parse_result = re.sub(r'[ァ-ヶー][行変]', "0", parse_result)  # マ行　とかそういう奴を消すため
    kana_list = regkana.findall(parse_result)
    if len(kana_list) == 0:  # 不明
        kana = None
        family_kana = None
        first_kana = None
    elif len(kana_list) == 1 or first is None:  # 苗字だけ
        kana = ''.join(kana_list)
        family_kana = kana
        first_kana = None
    else:
        kana = ''.join(kana_list)
        family_kana = kana_list[0]
        first_kana = ''.join(kana_list[1:])

    return kana, family_kana, first_kana


# member
print("migrating member")
for item in psql.query('SELECT * FROM person ORDER BY class;', fetch=True):
    family, first, after = get_names(item)
    kana, family_kana, first_kana = get_kana(family, first)
    year = item['class'] + 1991

    ret = msql.query('''
    INSERT INTO member (id,family_name,family_kana,first_name,first_kana,show_name,year,sex,visible)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                     (item['person_id'], family, family_kana, first, first_kana, after,  year, item['sex'], item['visible']))

# training
print("migrating training")
try:
    psql.query(' CREATE SEQUENCE IF NOT EXISTS training_id_seq;')
    psql.query(
        '''ALTER TABLE training ADD COLUMN training_id integer NOT NULL DEFAULT nextval('training_id_seq');''')
    psql.commit()
except DuplicateColumn as err:
    psql.conn = psycopg2.connect(
        'user=honomara dbname=honomara password=honomara')

query = "INSERT INTO training (id,date,place,weather,title,comment) VALUES (%s,%s,%s,%s,%s,%s);"
for row in psql.query('SELECT * FROM training;', fetch=True):
    data = (row['training_id'], str(row['date']), row['site'],
            row['weather'], row['subject'], row['comment'])
    msql.query(query, data)

# restaurant
print("migrating restaurant")
msql.query('''
INSERT  INTO restaurant (id, name,place,comment)
VALUES (1,'Undefined','Undefined','Undefined')
;''')

restaurants = psql.query('''
SELECT
restaurant AS name,
site AS place,
avg(cost_max)       AS cost_max,
avg(cost_min)        AS cost_min ,
avg(number_max) AS n_max,
avg(number_min)  AS n_min,
count( after.date >  '2015-01-01' OR NULL) AS score
FROM after
WHERE after.restaurant != '?' AND after.restaurant != '？' AND after.restaurant != ''
GROUP BY (name,place)
ORDER BY place,name DESC;
''', fetch=True)


for r in restaurants:
    if r['name'] in ['', '?', '？']:
        continue

    place = r['place']
    cost = int((r['cost_max'] + r['cost_min']) / 2)
    number = int((r['n_max'] + r['n_min']) / 2)
    comment = "費用目安 {}\n".format(cost)
    comment += "適正人数 {}人\n".format(number)
    msql.query(
        'INSERT INTO restaurant (name,place,comment,score) VALUES (%s,%s,%s,%s)',
        (r['name'], r['place'], comment, r['score']))

# after
print("migrating after")
try:
    psql.query('''CREATE SEQUENCE IF NOT EXISTS after_id_seq ;''')
    psql.query(
        '''ALTER TABLE after ADD COLUMN after_id integer NOT NULL DEFAULT nextval('after_id_seq');''')
    psql.commit()
except DuplicateColumn as err:
    print(err)
    psql = Postgres()

r1 = msql.query('SELECT * FROM restaurant WHERE id = 1;',fetch=True)[0]
for d in psql.query('SELECT * FROM after ORDER BY date;', fetch=True):
    r = None
    if d['restaurant'] not in ['', '?', '？']:
        r = msql.query('SELECT * FROM restaurant WHERE name = %s AND place = %s',
                          (d['restaurant'], d['site']), fetch=True)[0]
    if r is None:
        r = r1
    r_id = r['id']

    try:
        msql.query('''
        INSERT INTO after (id,date,after_stage,restaurant_id,title,comment)
        VALUES (%s,%s,%s,%s,%s,%s);''', (d['after_id'], d['date'], d['after'], r_id, d['topic'], d['comment']))
    except Exception as err:
        print(err)
        print(d)
        print(r)
        raise Exception

# participants
print("migrating participants")
try:
    psql.query(
        '''
        ALTER TABLE participant ADD COLUMN after_id integer;
        ALTER TABLE participant ADD COLUMN training_id integer;
        ALTER TABLE participant ADD COLUMN origin varchar;
        UPDATE participant SET after_id = after.after_id, origin='after'
            FROM after WHERE participant.id = after.id;
        UPDATE participant SET training_id = training.training_id, origin='training'
            FROM training WHERE participant.id = training.id;
        ''')
    psql.commit()
except DuplicateColumn as err:
    psql = Postgres()

for row in psql.query('SELECT * FROM participant;', fetch=True):
    if row['origin'] == 'after':
        msql.query('INSERT INTO after_participant (member_id,after_id) VALUES (%s,%s);',
                   (row['person_id'], row['after_id']))
    elif row['origin'] == 'training':
        msql.query('INSERT INTO training_participant (member_id,training_id) VALUES (%s,%s);',
                   (row['person_id'], row['training_id']))
# race_base
msql.query('''TRUNCATE TABLE race_base;''')
ds = psql.query('''SELECT DISTINCT race_name FROM race;''', fetch=True)

table = {
    "いたばしリバーサイド・ハーフマラソン": "いたばしリバーサイドハーフマラソン",
    "おきなわマラソン_": "おきなわマラソン",
    "戸田・彩湖フルマラソン&ウルトラマラソン": "戸田・彩湖フルマラソン＆ウルトラマラソン"
}
ds = set(map(lambda n: table.get(n['race_name'], n['race_name']).strip(), ds))
ds = list(ds)
ds.sort()

for d in ds:
    msql.query('INSERT INTO race_base (race_name) VALUES (%s);', (d,))
# race
print("migrating race")
for d in psql.query('SELECT race_id,race_name,date FROM race ORDER BY race_id;', fetch=True):
    d['race_name'] = table.get(d['race_name'], d['race_name'])
    msql.query('INSERT INTO race (id, race_name, date) VALUES (%s,%s,%s);',
               (d['race_id'], d['race_name'], d['date']))
# race_type
print("migrating race_type")
ds = psql.query('''
SELECT distance_id AS race_type_id, distance AS distance, distance_name AS show_name, ranking  FROM distance ORDER BY ranking;
''', fetch=True)

time = list(filter(lambda d: search('時間', d['show_name']), ds))
road = list(filter(lambda d: search('マラソン|キロ|マイル', d['show_name']), ds))
track = list(filter(lambda d: search('メートル', d['show_name']), ds))


for t in time:
    t['duration'] = float(t['show_name'].replace('時間走', '')) * 3600
    t['distance'] = None
    t['race_type'] = 'time'
    msql.query('''INSERT INTO race_type (id, race_type, duration, show_name, ranking) VALUES (%s,%s,%s,%s,%s);''',
               (t['race_type_id'], t['race_type'], t['duration'], t['show_name'], t['ranking']))


for t in track:
    t['race_type'] = 'track'
    t['distance'] = float(t['distance'])  # km単位
    msql.query('''INSERT INTO race_type (id, race_type, duration, show_name, ranking) VALUES (%s,%s,%s,%s,%s);''',
               (t['race_type_id'], t['race_type'], t['distance'], t['show_name'], t['ranking']))


for t in road:
    t['distance'] = float(t['distance'])
    t['race_type'] = 'road'
    msql.query('''INSERT INTO race_type (id, race_type, duration, show_name, ranking) VALUES (%s,%s,%s,%s,%s);''',
               (t['race_type_id'], t['race_type'], t['distance'], t['show_name'], t['ranking']))
# result
print("migrating result")
n = psql.query('SELECT count(*) FROM result; ', fetch=True)[0]['count']
ofst = 0
limit = 100
for ofst in range(0, n, limit):
    ds = psql.query('''
    SELECT person_id as member_id, race_id, distance_id as race_type_id,time as result, display_time, comment
    FROM result ORDER BY race_id OFFSET {} LIMIT {};'''.format(ofst, limit), fetch=True)
    for d in ds:
        if not d['result']:  # 結果がない場合は飛ばす
            continue
#         sss = int(d['result'].total_seconds())
#         strsss = '{:02}:{:02}:{:02}'.format(sss//3600, sss % 3600//60, sss % 60)

        msql.query('''INSERT INTO result (member_id, race_id, race_type_id, result, comment) VALUES (%s,%s,%s,%s,%s);''',
                   (d['member_id'], d['race_id'], d['race_type_id'], int(d['result'].total_seconds()), d['comment']))

msql.commit()
