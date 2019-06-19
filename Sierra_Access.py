from sqlalchemy import Column, Integer, Table, ForeignKey, MetaData, String, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import configparser

"""
Base = declarative_base(metadata=MetaData(schema='sierra_view'))


bib_record_order_record_link = Table('bib_record_order_record_link', Base.metadata,
                                     Column('order_record_id', Integer, ForeignKey('order_record.id')),
                                     Column('bib_record_id', Integer, ForeignKey('bib_record.id')))


class OrderRecord(Base):
    __tablename__ = 'order_record'
    id = Column(Integer, primary_key=True)
    bib_records = relationship("BibRecord", secondary=bib_record_order_record_link, back_populates="order_records")
    order_view = relationship("OrderView", uselist=False, back_populates='order_record')

    def __init__ (self, id): #this is incase we want to access the instance variables
        self.id = id

    def __repr__(self):
        """"""
        return"<OrderRecords - '%s'>" % (self.id)


class BibRecord(Base):
    __tablename__ = 'bib_record'
    id = Column(Integer, primary_key=True) #same column as record_id
    bcode1 = Column(String(1))
    bib_view = relationship("BibView", uselist=False, back_populates='bib_record')
    order_records = relationship("OrderRecord", secondary=bib_record_order_record_link, back_populates="bib_records")
    varfield_views = relationship("VarfieldView", uselist=True, back_populates='bib_record')

    def __init__(self):
        self.id = id
        self.bcode1 = bcode1

    def __repr__(self):
        """"""
        return "<BibRecord - '%s' : '%s'>" % (self.id, self.bcode1)

class OrderView(Base):
    __tablename__='order_view'
    id = Column(Integer, primary_key=True)
    record_num = Column(Integer)
    record_id = Column(Integer, ForeignKey('order_record.id')) #record_id not the order_record_id b/c that column dne
    order_record = relationship("OrderRecord",  back_populates='order_view')

    def __init__(self):
        self.id = id
        self.record_num = record_num
        self.record_id = record_id

    def __repr__(self):
        """"""
        return "<OrderView - '%s' : '%s' - '%s'>" % (self.id, self.record_num, self.record_id)

class BibView(Base):
    __tablename__='bib_view'
    id = Column(Integer, ForeignKey('bib_record.id'), primary_key=True )
    title = Column(String)
    record_num = Column(Integer)
    bib_record = relationship("BibRecord", back_populates='bib_view')

    def __init__(self):
        self.id = id
        self.title = title
        self.record_num = record_num

    def __repr__(self):
        """"""
        return "<BibView - '%s' : '%s'>" % (self.id, self.title)

class VarfieldView(Base):
    __tablename__ = 'varfield_view'
    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey('bib_record.id'))
    bib_record = relationship("BibRecord", back_populates='varfield_views')
    marc_tag = Column(Integer)
    field_content = Column(String)

    def __init__(self):
        self.id = id
        self.record_id = record_id
        self.marc_tag = marc_tag
        self.field_content = field_content

    def __repr__(self):
        """"""
        return "<VarfieldView - '%s' : '%s' - '%s' - '%s'>" % (self.id, self.record_id,
                                                        self.marc_tag, self.field_content)

"""
class SierraAccess:
    def __init__(self):
        self.engine = None
        self.session = None

        config = configparser.ConfigParser()
        config.sections()
        config.read('sierra.ini')

        self.drivername = config._sections['SIERRA']['drivername']
        self.username = config._sections['SIERRA']['username']
        self.password = config._sections['SIERRA']['password']
        self.host = config._sections['SIERRA']['host']
        self.port = config._sections['SIERRA']['port']
        self.database = config._sections['SIERRA']['database']

        self.connection_string = "%s://%s:%s@%s:%s/%s" % (
                self.drivername,
                self.username,
                self.password,
                self.host,
                self.port,
                self.database
                )

    def connect(self):
        self.engine = create_engine(self.connection_string,  pool_size=20, max_overflow=0)
        self.session = sessionmaker(bind=self.engine)
        return self.session()
