from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


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
    year = Column(Integer, nullable=False)  # 点数
    sex = Column(Integer, nullable=False)  # 点数
    visible = Column(Boolean, nullable=False)  # 点数

#     afters = relationship(
#         'After',
#         secondary=AfterParticipant.__tablename__,
#         back_populates='participants',
#     )
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

    def __repr__(self):
        return "<Training(training_id:{}, {:%Y-%m-%d}, place:{}, title:'{}')>"\
            .format(self.training_id, self.date, self.place, self.title)


Session = sessionmaker(bind=engine)
session = Session()
