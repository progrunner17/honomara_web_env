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

r1 = msql.query('SELECT * FROM restaurant WHERE id = 1;', fetch=True)[0]
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
# competitions
print("migrating competitions")
# msql.query('''TRUNCATE TABLE race_base;''')
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
    msql.query(
        'INSERT INTO competitions (name, show_name) VALUES (%s, %s);', (d, d))
# race_types
print("migrating races")
ds = psql.query('''
SELECT distance_id, race_id FROM result ORDER BY race_id, distance_id;
''', fetch=True)
last_d = {'distance_id': 0, 'race_id': 0}
race_name_distance_id = []
for d in ds:
    if [d['distance_id'], d['race_id']] == [last_d['distance_id'], last_d['race_id']]:
        continue
    last_d = d
    query_get_distance_data = 'SELECT distance, distance_name FROM distance WHERE distance_id={};'.format(
        d['distance_id'])
    distance_data = psql.query(query_get_distance_data, fetch=True)[0]
    show_name = distance_data['distance_name']
    query_get_race_name = 'SELECT race_name FROM race WHERE race_id={};'.\
        format(d['race_id'])
    race_name = psql.query(query_get_race_name, fetch=True)[0]['race_name']
    race_name = table.get(race_name, race_name)
    if [race_name, d['distance_id']] in race_name_distance_id:
        continue
    race_name_distance_id.append([race_name, d['distance_id']])
    competition_id = msql.query(
        'SELECT id FROM competitions WHERE name=%s;', (race_name,), fetch=True)[0]['id']
    if '時間' in show_name:
        type = 3
        distance = None
        dulation = float(show_name.replace('時間走', '')) * 3600
    elif ('マラソン' in show_name) or ('キロ' in show_name) or ('マイル' in ['show_name']):
        type = 0
        distance = float(distance_data['distance'])
        dulation = None
    elif 'メートル' in show_name:
        type = 2
        distance = float(distance_data['distance'])  # km単位
        dulation = None
    msql.query('INSERT INTO races (competition_id, show_name, type, distance, dulation) VALUES (%s, %s, %s, %s, %s);',
               (competition_id, show_name, type, distance, dulation))
# results
print("migrating results")
n = psql.query('SELECT count(*) FROM result; ', fetch=True)[0]['count']
ofst = 0
limit = 100
for ofst in range(0, n, limit):
    ds = psql.query('''
    SELECT person_id AS member_id, race_id, distance_id, time as result, display_time, comment
    FROM result ORDER BY race_id OFFSET {} LIMIT {};'''.format(ofst, limit), fetch=True)
    for d in ds:
        if not d['result']:  # 結果がない場合は飛ばす
            continue
#         sss = int(d['result'].total_seconds())
#         strsss = '{:02}:{:02}:{:02}'.format(sss//3600, sss % 3600//60, sss % 60)
        query_get_date = 'SELECT date FROM race WHERE race_id={}'.\
            format(d['race_id'])
        date = psql.query(query_get_date, fetch=True)[0]['date']
        query_get_race_name = 'SELECT race_name FROM race WHERE race_id={};'.\
            format(d['race_id'])
        race_name = psql.query(query_get_race_name, fetch=True)[0]['race_name']
        race_name = table.get(race_name, race_name)
        competition_id = msql.query(
            'SELECT id FROM competitions WHERE name=%s;', (race_name,), fetch=True)[0]['id']
        query_get_distance_name = 'SELECT distance_name FROM distance WHERE distance_id={};'.format(
            d['distance_id'])
        distance_name = psql.query(query_get_distance_name, fetch=True)[
            0]['distance_name']
        race_type_id = msql.query(
            'SELECT id FROM races WHERE competition_id = %s and show_name = %s;', (competition_id, distance_name), fetch=True)[0]['id']
        msql.query('''INSERT INTO results (date, member_id, competition_id, race_id, record, comment) VALUES (%s,%s,%s,%s,%s,%s);''',
                   (date, d['member_id'], competition_id, race_type_id, int(d['result'].total_seconds()), d['comment']))

msql.commit()
