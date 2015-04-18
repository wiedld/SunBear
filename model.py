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




######################################################################

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///DataBear.db", echo=True)
    Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
    Base.query = Session.query_property()
    return Session()

    # urlparse.uses_netloc.append("postgres")
    # url = urlparse.urlparse(os.environ["DATABASE_URL"])




def main():
    """For future use."""
    pass

if __name__ == "__main__":
    main()