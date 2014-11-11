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

###############  Data relationship  ###############
# One2One = one to one relationship
# One2M = one to many relationship
# M2M = many to many relationship



###############  Association Tables  ###############

investmentcompany_sectorfocus = Table('investmentcompany_sectorfocus', Base.metadata,
    Column('investmentcompany_id', Integer, ForeignKey('investmentcompany.id')),
    Column('sectorfocus_id', Integer, ForeignKey('sectorfocus.id'))
    )

portfoliocompany_category = Table('portfoliocompany_category', Base.metadata,
    Column('portfoliocompany_id', Integer, ForeignKey('portfoliocompany.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
    )


############### Class declarations  ###################

# Information particular to each investment company
# M2M: An investment company will have many portfolio companies, investment types, sector focuses.  Vice versa.
# One2M: An investment company will have many partners.

class IqtPartner(Base):
    __tablename__ = "iqtpartner"
    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable=False)
    permalink = Column(String(120), nullable=False)

class InvestmentCompany(Base):
    __tablename__ = "investmentcompany"

    id = Column(Integer, primary_key = True)
    uuid = Column(Integer, nullable=True)
    permalink = Column(String(120), nullable=False)
    name = Column(String(120), nullable=True)
    homepage_url = Column(String(30), nullable=True)
    founded = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    number_of_investments = Column(Integer, nullable = True)
    city = Column(String(64), nullable=True)
    state = Column(String(64), nullable=True)
    
    partners = relationship("Partner", 
                    backref="investmentcompany")
    sectors = relationship("SectorFocus",
                    secondary=investmentcompany_sectorfocus,
                    backref="investmentcompanies")



# Investment details as a result of an investment company and a portfolio company relationship   
class Investment(Base):
    __tablename__ = "investment"

    id = Column(Integer, primary_key = True)
    investmentcompany_id = Column(Integer, ForeignKey('investmentcompany.id'), nullable=False)
    portfoliocompany_id = Column(Integer, ForeignKey('portfoliocompany.id'), nullable=False)
    
    money_raised = Column(Integer, nullable=True)  ### Total invested into a portfolio company by an investment company
    funding_round = Column(String(15), nullable=True) ### Seed, Venture, Series A - C
    equity_percent_first_trans = Column(Integer, nullable=True)  ### IQT information
    equity_percent_second_trans = Column(Integer, nullable=True)  ### IQT information
    ownership_percent = Column(Integer, nullable=True)  ### IQT information

    investmentcompany = relationship("InvestmentCompany", backref="investment")  
    portfoliocompany = relationship("PortfolioCompany", backref="investment")



# Information particular to each investment company Partner
# M2One: Many partners belong to only one investment company.
class Partner(Base):
    __tablename__ = "partner"  ## Person who works at an investment company who is responsible for a specific portfolio company

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=True)
    last_name = Column(String(120), nullable=True)
    title = Column(String(120), nullable=True)
    investmentcompany_id = Column(Integer, ForeignKey('investmentcompany.id'))


# Sectors in which an investment company typically puts funds into
# M2M:  A sector can belong to many investment companies and an investment company can put funds into many sectors.
class SectorFocus(Base):
    __tablename__ = "sectorfocus"
    id = Column(Integer, primary_key = True)
    sector = Column(String(120), nullable=True)  ## analytics, software, mobile, SaaS, advertising, curated web, etc


# Information particular to each company that has received funds from an investment company 
# M2M: A portfolio company has many investment companies and categories.  Vice versa.
class PortfolioCompany(Base):
    __tablename__ = "portfoliocompany"  ## company receiving funding from investment companies
    
    id = Column(Integer, primary_key=True)
    uuid = Column(Integer, nullable=False)
    permalink = Column(String(120), nullable=False)
    company_name = Column(String(120), nullable=True)
    city = Column(String(64), nullable=True)
    state = Column(String(64), nullable=True)
    homepage_url = Column(String(30), nullable=True)
    founded = Column(DateTime, nullable=True)
    total_funding = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    
    categories = relationship("Category",
                    secondary=portfoliocompany_category,
                    backref="portfoliocompanies")


# Categories to which each portfolio company product/service belongs.
# M2M: A portfolio company can have many categories and each category belongs to many companies.
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    category = Column(String(120), nullable=True)  ## analytics, software, security, storage, enterprise, etc
    




### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
