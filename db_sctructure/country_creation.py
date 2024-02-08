from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from os import getenv
from models import Country
from utils import Countries
load_dotenv()

engine = create_engine(getenv('DATABASE_URI'))


if __name__ == "__main__":

    with Session(engine) as session:
        for name in Countries._member_names_:
            country = Country(name=name)
            session.add(country)
            session.commit()
            