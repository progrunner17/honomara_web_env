from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
from util import get_wday, str_to_date

dns = 'mysql+mysqlconnector://honomara:honomara@localhost/honomara'
engine = create_engine(dns, encoding="utf-8")
Base = declarative_base()


class Member(Base):
    __tablename__ = 'members'

    member_id = Column(Integer, primary_key=True)
    family_name = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    show_name = Column(String(20), nullable=False)
    kana = Column(String(40), nullable=False)
    year = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=False)
    visible = Column(Boolean, nullable=False)

    def __init__(self, form=None, **args):
        if form is not None:
            args = {}
            if form.get('member_id') != '':
                args['member_id'] = int(form.get('member_id'))
            else:
                args['member_id'] = None

            args['family_name'] = form.get('family_name')
            args['first_name'] = form.get('first_name')

            if form.get('show_name') != '':
                args['show_name'] = form.get('show_name')
            else:
                args['show_name'] = args['family_name']
            args['kana'] = form.get('kana')
            args['year'] = int(form.get('year'))
            args['sex'] = int(form.get('sex'))
            args['visible'] = bool(form.get('visible'))
        return super().__init__(**args)

    def __repr__(self):
        fields = {}
        fields['member_id'] = self.member_id
        fields['family_name'] = self.family_name
        fields['first_name'] = self.first_name
        fields['show_name'] = self.show_name
        fields['year'] = self.year
        if self.sex == 0:
            fields['sex'] = 'male'
        elif self.sex == 1:
            fields['sex'] = 'female'
        else:
            fields['sex'] = 'unknown or other'
        fields['visible'] = self.visible
        return "<Member('{member_id}','{family_name}', '{first_name}', '{show_name}', {year}, {sex}, {visible})>".format(**fields)


class AfterParticipant(Base):
    __tablename__ = 'after_participants'

    member_id = Column(Integer, ForeignKey('members.member_id'), primary_key=True)
    after_id = Column(Integer, ForeignKey('afters.after_id'), primary_key=True)

    def __repr__(self):
        return "<AfterParticipant(after_id:{}, member_id:{})>".\
            format(self.after_id, self.member_id)


class Restaurant(Base):
    __tablename__ = 'restaurants'
    restaurant_id = Column(Integer, primary_key=True)
    restaurant_name = Column(String(64), nullable=False)
    place = Column(String(20))
    comment = Column(Text)

    def __repr__(self):
        return "<Restaurant(id:{}, name:{}, plase:{})>".\
            format(self.restaurant_id, self.restaurant_name, self.place)


class After(Base):
    __tablename__ = 'afters'

    after_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    after_stage = Column(Integer, nullable=False, server_default=text('1'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'), nullable=False)
    total = Column(Integer)
    title = Column(String(128), nullable=False)
    comment = Column(Text)
    restaurant = relationship('Restaurant')

    participants = relationship(
        'Member',
        secondary=AfterParticipant.__tablename__,
        order_by='Member.year, Member.kana'
    )

    def __init__(self, form=None, **args):
        if form is not None:
            args = {}
            if form.get('after_id') != '':
                args['after_id'] = int(form.get('after_id'))
            else:
                args['after_id'] = None
            args['date'] = form.get('date')
            args['after_stage'] = int(form.get('after_stage'))
            args['restaurant_id'] = int(form.get('restaurant_id'))
            args['total'] = 0   # TODO
            args['title'] = form.get('title')
            args['comment'] = form.get('comment')
            participants = []
            for id in form.getlist('participants'):
                member = session.query(Member).get(id)
                participants.append(member)
            args['participants'] = participants
        return super().__init__(**args)

    def __repr__(self):
        return "<After(after_id:{}, {:%Y-%m-%d}, title:'{}')>".\
            format(self.after_id, self.date, self.title)


class TrainingParticipant(Base):
    __tablename__ = 'training_participants'

    member_id = Column(Integer, ForeignKey('members.member_id'), primary_key=True)
    training_id = Column(Integer, ForeignKey('trainings.training_id'), primary_key=True)

    def __repr__(self):
        return "<TrainingParticipant(training_id:{}, member_id:{})>".\
            format(self.training_id, self.member_id)


class Training(Base):
    __tablename__ = 'trainings'

    training_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    wday = Column(String(1))
    place = Column(String(20), nullable=False)
    weather = Column(String(20), nullable=False)
    title = Column(String(20), nullable=False)
    comment = Column(Text)

    participants = relationship(
        'Member',
        secondary=TrainingParticipant.__tablename__,
        order_by='Member.year, Member.kana'
    )

    def __init__(self, form=None, **args):
        if form is not None:
            args = {}
            if form.get('training_id') != '':
                args['training_id'] = int(form.get('training_id'))
            else:
                args['training_id'] = None
            args['date'] = str_to_date(form.get('date'))
            args['wday'] = get_wday(args['date'])
            # args['restaurant_id'] = int(form.get('restaurant_id', 0))
            args['place'] = form.get('place')   # TODO
            args['weather'] = form.get('weather')
            args['title'] = form.get('title')
            args['comment'] = form.get('comment')
            participants = []
            for id in form.getlist('participants'):
                member = session.query(Member).get(id)
                participants.append(member)
            args['participants'] = participants
        return super().__init__(**args)

    def __repr__(self):
        return "<Training(training_id:{}, {:%Y-%m-%d}, place:{}, title:'{}')>"\
            .format(self.training_id, self.date, self.place, self.title)


Session = sessionmaker(bind=engine)
session = Session()
