from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session


engine = create_engine("sqlite:///crunchbase_iqt.db", echo=True)
session = scoped_session(sessionmaker(bind=engine,
                                    autocommit = False,
                                    autoflush = False))

Base = declarative_base()
Base.query = session.query_property()




############### Class declarations  ###################

# Information particular to each investment company
# M2M: An investment company will have many portfolio companies, investment types, sector focuses.  Vice versa.
# One2M: An investment company will have many partners.

class IqtPartner(Base):
    __tablename__ = "iqtpartner"
    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable=False)
    permalink = Column(String(120), nullable=False)





### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
