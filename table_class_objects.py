from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
import os


DATABASE_URL = os.environ.get('DATABASE_URL')


engine = create_engine(DATABASE_URL, echo=True)
session = scoped_session(sessionmaker(bind=engine,
                                    autocommit = False,
                                    autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

###############  Data relationship  ###############
# One2One = one to one relationship
# One2M = one to many relationship
# M2M = many to many relationship


############### Class declarations  ###################

# Information particular to each investment company
# M2M: An investment company will have many portfolio companies, investment types, sector focuses.  Vice versa.
# One2M: An investment company will have many partners.


class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key = True)

    first_name = Column(String(120), nullable=True)
    last_name = Column(String(120), nullable=True)
    email = Column(String(100), nullable = True)
    password = Column(String(100), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

     

class InvestmentCompany(Base):
    __tablename__ = "investmentcompany"

    id = Column(Integer, primary_key = True)

    uuid = Column(String(50), nullable=True)
    permalink = Column(String(120), nullable=False)
    name = Column(String(120), nullable=True)
    homepage_url = Column(String(100), nullable=True)
    founded = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    number_of_investments = Column(Integer, nullable = True)
    city = Column(String(64), nullable=True)
    state = Column(String(64), nullable=True)



    
# Investment details as a result of an investment company and a portfolio company relationship   
class Investment(Base):
    __tablename__ = "investment"

    id = Column(Integer, primary_key = True)
    investmentcompany_id = Column(Integer, ForeignKey('investmentcompany.id'), nullable=False)
    portfoliocompany_id = Column(Integer, ForeignKey('portfoliocompany.id'), nullable=False)
    
    money_raised = Column(Integer, nullable=True)  ### Total invested into a portfolio company by an investment company
    funding_round = Column(String(15), nullable=True) ### Seed, Venture, Series A - C
    
    investmentcompany = relationship("InvestmentCompany", backref="investment")  
    portfoliocompany = relationship("PortfolioCompany", backref="investment")


# Information particular to each company that has received funds from an investment company 
# M2M: A portfolio company has many investment companies and categories.  Vice versa.
class PortfolioCompany(Base):
    __tablename__ = "portfoliocompany"  ## company receiving funding from investment companies
    
    id = Column(Integer, primary_key=True)

    uuid = Column(String(50), nullable=False)
    permalink = Column(String(120), nullable=False)
    company_name = Column(String(120), nullable=True)
    city = Column(String(64), nullable=True)
    state = Column(String(64), nullable=True)
    homepage_url = Column(String(100), nullable=True)
    founded = Column(DateTime, nullable=True)
    total_funding = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    

class VCList(Base):
    __tablename__ = "vc"

    id = Column(Integer, primary_key = True)

    name = Column(String(120), nullable=True)
    permalink = Column(Text, nullable=False)



def create_tables():

    Base.metadata.create_all(engine)


### End class declarations

def main():
    # pass
    create_tables()
   
if __name__ == "__main__":
    main()
