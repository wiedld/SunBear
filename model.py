from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref, scoped_session
Base = declarative_base()

#######################################################################

##  STEP1 = make the db file and metadata.  In python shell:
# -i model.py  >  create_engine  >  Base.metadata.create_all(eng)

##  STEP 2 = Perform seeding.
ENGINE = None
Session = None
# function connect() at bottom...before main.
## in python shell:  -i model.py > s=connect() >

class Demographic(Base):
    """from Social Explorer"""
    __tablename__ = "Demographics"
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(15))    # is unique per row
    popdensity = Column(Float)
    pctemployed = Column(Float)
    pctmnf = Column(Float)
    pctlogistics = Column(Float)
    pctit = Column(Float)
    pctprof = Column(Float)
    hhincq10 = Column(Integer)
    hhincq30 = Column(Integer)
    hhincq50 = Column(Integer)
    hhincq70 = Column(Integer)
    hhincq90 = Column(Integer)
    hhincq95 = Column(Integer)
    pctheatelec = Column(Float)


# object attributes:
# zip,popdensity,pctemployed,pctmnf,pctlogistics,pctit,pctprof,hhincq10,hhincq30,hhincq50,hhincq70,hhincq90,hhincq95,pctheatelec

# object attributes - detailed name:
# zip,Population Density (per sq. mile),% of labor force employed,% employed in manufacturing,% empl logistics,% empl  IT,% empl prof,Households: Quintile Means: Lowest Quintile,Households: Quintile Means: Second Quintile,Households: Quintile Means: Third Quintile,Households: Quintile Means: Fourth Quintile,Households: Quintile Means: Highest Quintile,Households: Quintile Means: Top 5 Percent,% heat with elect



class Geographic(Base):
    """from Social Explorer"""
    __tablename__ = "Geographics"
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(15))    # is unique per row
    type_addy = Column(String(100))
    primary_city = Column(String(30))
    acceptable_cities = Column(String(100))
    unacceptable_cities = Column(String(100))
    state = Column(String(2))
    county = Column(String(30))
    timezone = Column(String(30))
    area_codes = Column(String(3))
    latitude = Column(Float)
    longitude = Column(Float)
    world_region = Column(String(30))
    country = Column(String(2))           # select only for US
    decommissioned = Column(String(10))
    estimated_population = Column(Integer)
    notes = Column(String(100))


# object attributes
# zip,type,primary_city,acceptable_cities,unacceptable_cities,state,county,timezone,area_codes,latitude,longitude,world_region,country,decommissioned,estimated_population,notes





class Zillow_demo(Base):
    """from zillow API"""
    __tablename__ = "Zillow_demos"
    id = Column(Integer, primary_key=True)
    zipcode = Column(String(15))    # is unique per row
    type_addy = Column(String(100))
    primary_city = Column(String(30))
    acceptable_cities = Column(String(100))
    unacceptable_cities = Column(String(100))
    state = Column(String(2))
    county = Column(String(30))
    timezone = Column(String(30))
    area_codes = Column(String(3))
    latitude = Column(Float)
    longitude = Column(Float)
    world_region = Column(String(30))
    country = Column(String(2))           # select only for US
    decommissioned = Column(String(10))
    estimated_population = Column(Integer)
    notes = Column(String(100))



class zillow_neighborhood(Base):
    """from zillow API"""
    __tablename__ = "zillow_neighborhoods"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))    # is unique per row
    latitude = Column(Float)
    longitude = Column(Float)





######################################################################

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///DataBear.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    # Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
    # Base.query = Session.query_property()
    return Session()

    # urlparse.uses_netloc.append("postgres")
    # url = urlparse.urlparse(os.environ["DATABASE_URL"])




def main():
    """For future use."""
    pass

if __name__ == "__main__":
    main()