from dotenv import load_dotenv
from utils import *
from models import Country, Record
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from os import getenv
load_dotenv()
engine = create_engine(getenv('DATABASE_URI'))

Session = sessionmaker(bind=engine)

with Session() as session:
    records = []

    for _ in range(0, 5000):

        country_selector = CountriesSelector()
        date_generator = DateGen()

        exp_stmt = select(Country).where(
            Country.name == country_selector.exporter)
        imp_stmt = select(Country).where(
            Country.name == country_selector.importer)
        exporter = session.execute(exp_stmt).scalar()
        importer = session.execute(imp_stmt).scalar()

        exporter = session.merge(exporter)
        importer = session.merge(importer)

        amount = AmountCreator(
            export_tax=exporter.export_tax, import_tax=importer.import_tax)

        record = Record(
            exporter_id=exporter.id, exporter=exporter, importer_id=importer.id,
            importer=importer, date=date_generator.generate_date(),
            total_amount=amount.amount, net_amount=amount.net_amount,
            product_category=choice(ProductCategories._member_names_),
            shipping_method=choice(TransportMethod._member_names_)
        )
        records.append(record)

    session.add_all(records)
    session.commit()
