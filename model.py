from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///crunchbase_iqt.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                    autocommit = False,
                                    autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

### Data relationship
# One2One = one to one relationship
# One2M = one to many relationship
# M2M = many to many relationship

### Class declarations

# Table collecting the many to many relationships
association_table = Table('association', Base.metadata,
    Column('investmentcompany_id', Integer, ForeignKey('investmentcompany.id')),
    Column('portfoliocompany_id', Integer, ForeignKey('portfoliocompany.id')),
    Column('investmenttype_id', Integer, ForeignKey('investmenttype.id')),
    Column('sectorfocus_id', Integer, ForeignKey('sectorfocus.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
    )

# Information particular to each investment company
# M2M: An investment company will have many portfolio companies, investment types, sector focuses.  Vice versa.
# One2M: An investment company will have many partners.
class InvestmentCompany(Base):
    __tablename__ = "investmentcompany"

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable=True)
    city = Column(String(64), nullable=True)
    state = Column(String(64), nullable=True)
    zipcode = Column(String(15), nullable=True)
    homepage_url = Column(String(30), nullable=True)
    founded = Column(DateTime, nullable=True)
    partners = relationship("Partner", 
                    secondary=association_table,
                    backref="investmentcompany")
    portfoliocompanies = relationship("PortfolioCompany",
                    secondary=association_table,
                    backref="portfoliocompany")
    investmenttypes = relationship("InvestmentType",
                    secondary=association_table,
                    backref="investmenttype")
    sectorfocuses = relationship("SectorFocus",
                    secondary=association_table,
                    backref="sectorfocus")


# Information particular to each investment company Partner
# M2One: Many partners belong to only one investment company.
class Partner(Base):
    __tablename__ = "partner"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), nullable=True)
    last_name = Column(String(120), nullable=True)
    investmentcompany_id = Column(Integer, ForeignKey('investmentcompany.id'))


# Types of investments that an investment company makes
# M2M:  An investment type can belong to many investment companies and an investment company can have many investment types.
class InvestmentType(Base):
    __tablename__ = "investmenttype"
    id = Column(Integer, primary_key = True)
    type_description = Column(String(64), nullable=True)
    investmentcompany_id = Column(Integer, ForeignKey('investmentcompany.id'))


# Sectors in which an investment company typically puts funds into
# M2M:  A sector can belong to many investment companies and an investment company can put funds into many sectors.
class SectorFocus(Base):
    __tablename__ = "sectorfocus"
    id = Column(Integer, primary_key = True)
    sector_name = Column(String(30), nullable=True)
    investmentcompany_id = Column(Integer, ForeignKey('investmentcompany.id'))

# Information particular to each company that has received funds from an investment company 
# M2M: A portfolio company has many investment companies and categories.  Vice versa.
class PortfolioCompany(Base):
    __tablename__ = "portfoliocompany"
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(120), nullable=True)
    equity_percent_first_trans = Column(Integer, nullable=True)
    equity_percent_second_trans = Column(Integer, nullable=True)
    ownership_percent = Column(Integer, nullable=True)
    investmentcompany_id = Column(Integer, ForeignKey('investmentcompany.id'))
    categories = relationship("Category",
                    secondary=association_table,
                    backref="portfoliocompany")


# Categories to which each portfolio company belongs.
# M2M: A portfolio company can have many categories and each category belongs to many companies.
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    category_name = Column(String(30), nullable=True)
    portfoliocompany_id = Column(Integer, ForeignKey('portfoliocompany.id'))




### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
