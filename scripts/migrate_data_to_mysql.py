#!/usr/bin/env python
# coding: utf-8
from time import sleep
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

    def reload(self):
        self.conn = psycopg2.connect(
            'user=honomara dbname=honomara password=honomara')

    def __del__(self):
        self.conn.close()


class Mysql:
    conn = None
    cur = None

    def __init__(self, user='honomara', database='honomara', password='honomara'):
        self.password = password
        self.user = user
        self.database = database
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

    def reload(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user=self.user,
            password=self.password,
            database=self.database,
        )


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
#         parse_name = fam_n
    else:
        fir_n = fir_n.group()
        fir_n = fir_n.replace(' ', '')
        fir_n = fir_n.replace('　', '')
#         parse_name = fam_n + fir_n

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
    member_id = item['person_id']
    family, first, show_name = get_names(item)
    kana, family_kana, first_kana = get_kana(family, first)
    year = item['class'] + 1991
    sex = 'male' if item['sex'] == 0 else 'female' if item['sex'] == 1 else None
    if sex == None:
        pass
    visible = item['visible']
    ret = msql.query('''
    INSERT INTO member (id,family_name,family_kana,first_name,first_kana,show_name,year,sex,visible)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                     (member_id, family, family_kana, first, first_kana, show_name,  year, sex, visible))

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

query = "INSERT INTO training (id,date,type,weather,title,comment) VALUES (%s,%s,%s,%s,%s,%s);"
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


def isascii(s):
    return all(map(lambda c: ord(c) < 0x80, list(s)))


def normalize_name(name):
    tmp = name.strip()         # delete trailing whitespace
    tmp = tmp.replace('_', '')  # "おきなわマラソン_" → "おきなわマラソン"

    if not all(map(lambda c: ord(c) < 0x80, list(tmp))):  # 英数(ascii)以外を含む場合　＜＝＞　日本語の場合
        tmp = tmp.translate(str.maketrans({
            chr(ord(i) + ord('！') - ord('!')): i for i in list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")}))
        tmp = tmp.translate(str.maketrans({
            i: chr(ord(i) + ord('！') - ord('!')) for i in list("0123456789!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~")}))
    return tmp


# race_base // competition
# msql.query('''TRUNCATE TABLE race_base;''')
races = psql.query('''SELECT DISTINCT * FROM race;''', fetch=True)

# table = {
#     "いたばしリバーサイド・ハーフマラソン": "いたばしリバーサイドハーフマラソン",
#     "おきなわマラソン_": "おきなわマラソン",
#     "戸田・彩湖フルマラソン&ウルトラマラソン": "戸田・彩湖フルマラソン＆ウルトラマラソン"
# }
# ds = set(map(lambda n: table.get(n['race_name'], n['race_name']).strip(), ds))


races = list(set(map(lambda r: normalize_name(r["race_name"]), races)))
races.sort()

for race in races:
    tmp = msql.query(
        'SELECT id FROM competition WHERE name = %s', (race,), fetch=True)

    if len(tmp) == 0:
        msql.query('INSERT INTO competition (name) VALUES (%s) ;', (race,))
psql.commit()


def mysql_get_competition_id(name):
    #     print(name)
    tmp = msql.query(
        'select name, id from competition where name = %s;', (name,), fetch=True)
#     print(tmp)
    assert len(tmp) == 1
    return tmp[0]['id']


def infer_type(competition_name, distance, distance_name):
    is_time = search('時間', distance_name) != None
    is_road = search('マラソン|キロ|マイル', distance_name) != None
    is_track = search('メートル', distance_name) != None
    l = len(list(filter(lambda n: n, [is_time, is_road, is_track])))
    assert(l == 1)

    show_name = None
    time = None
    type = None
    if is_time:
        time = float(distance_name.replace('時間走', '')) * \
            3600 * 1000  # time in miliseconds
#         print("{} time: {}".format(competition_name, time// 1000 // 3600))
        type = "time"
        show_name = distance_name
    if is_road:
        if search('マラソン|マイル', distance_name) != None:
            show_name = distance_name
        if search('trail|トレイル', competition_name.lower()):
            type = "trail"
        else:
            type = "road"

    if is_track:  # TODO 単位揃え
        #         distance = float(distance)                                       # distance in km
        show_name = distance_name
        type = "track"

    ret = {}
    ret["competition_name"] = competition_name
    ret["type"] = type
    ret["distance"] = distance
    ret["time"] = time
    ret["show_name"] = show_name
    return ret

# msql.commit()
# msql.conn.rollback()
# psql.reload()


q = '''
SELECT DISTINCT
race.race_name as race_name,
distance.distance as distance,
distance.distance_name as distance_name,
distance.distance_id as distance_id,
count(*)
FROM result
INNER JOIN distance
ON result.distance_id = distance.distance_id
INNER JOIN race
ON result.race_id = race.race_id
GROUP BY (race_name, distance.distance_id)
ORDER BY race_name;'''


ds = psql.query(q, fetch=True)
for course in ds:
    #     print(course)
    course['race_name'] = normalize_name(course['race_name'])
    competition_id = mysql_get_competition_id(course['race_name'])
    c = infer_type(course['race_name'],
                   course['distance'], course['distance_name'])
    c["competition_id"] = competition_id
    c["distance_id"] = course["distance_id"]

    cid = msql.query("SELECT * FROM course WHERE (competition_id = %s AND type = %s AND (distance = %s OR time = %s))",
                     (c["competition_id"], c["type"], c["distance"], c["time"]), fetch=True)
    if len(cid) == 0:
        msql.query('''INSERT INTO course (competition_id, type, distance, time, show_name) VALUES (%s,%s,%s,%s,%s);''',
                   (c["competition_id"], c["type"], c["distance"], c["time"], c["show_name"]))


def get_course_id(d):
    competition_name = normalize_name(d['race_name'])
    competition_id = mysql_get_competition_id(competition_name)
    distance = d['distance']
#     time = int(d['time'].total_seconds() * 1000)

    print("{}({})".format(competition_name, competition_id))
    cid = msql.query(""" SELECT * FROM course WHERE competition_id=%s AND distance=%s; """,
                     (competition_id, distance), fetch=True)
    if len(cid) != 1:
        print("competition_id = {}".fomrat(competition_id))
        print("distance = {}".fomrat(distance))
        print("len", len(cid))
        print("d", d)
        raise Exception("may be time")
    return cid[0]['id']


def get_race_id(course_id, date):
    tmp = msql.query('''SELECT id from race WHERE course_id=%s AND date=%s;''',
                     (course_id, date), fetch=True)
    if len(tmp) > 1:
        print(course_id, date)
        raise Exception
    elif len(tmp) == 0:
        msql.query('''INSERT INTO race (course_id, date) VALUES (%s,%s);''',
                   (course_id, date))
        lids = msql.query(
            '''SELECT LAST_INSERT_ID() as lid FROM race LIMIT 1;''', fetch=True)
#         print("race.id", lids)
        lid = lids[0]['lid']
        return lid
    else:
        return tmp[0]['id']


print("migrating result")
n = psql.query('SELECT count(*) FROM result; ', fetch=True)[0]['count']
# n = 100
ofst_start = 0
limit = 20

q = '''
    SELECT * FROM result
    INNER JOIN race
    ON result.race_id = race.race_id
    INNER JOIN distance
    ON result.distance_id = distance.distance_id
    ORDER BY id OFFSET {} LIMIT {};
    '''
for ofst in range(ofst_start, n, limit):
    ds = psql.query(q.format(ofst, limit), fetch=True)
    for d in ds:
        course_id = get_course_id(d)
        race_id = get_race_id(course_id, d['date'])
        member_id = d['person_id']
        time = int(d['time'].total_seconds() * 1000) if d['time'] else None
        distance = d['distance']  # float in km
        comment = d['comment'] or ""

        tmp_prev = msql.query('''SELECT id from result WHERE race_id=%s AND time=%s AND distance=%s ;''',
                              (race_id, time, distance), fetch=True)
        msql.query('''INSERT INTO result (race_id, time, distance, comment) VALUES (%s,%s,%s,%s);''',
                   (race_id, time, distance, comment))

        tmp = msql.query(
            '''SELECT LAST_INSERT_ID() as lid FROM result LIMIT 1;''', fetch=True)
#         print("result.id", tmp)
        result_id = tmp[0]['lid']

        msql.query('''INSERT INTO race_participant (result_id, member_id) VALUES (%s,%s);''',
                   (result_id, member_id))
msql.commit()
