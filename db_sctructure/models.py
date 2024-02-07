from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import create_engine
from sqlalchemy import Integer, String, Float, Column, ForeignKey, DateTime
from random import uniform
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URI = f'mysql+mysqlconnector://{getenv("DB_USER")}:{getenv("DB_PASS")}@localhost/{getenv("DB_NAME")}'

class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(length=30), nullable=False, unique=True)
    export_tax =  Column(Float(), default= lambda: round(uniform(0.5, 1.5),2))
    import_tax = Column(Float(), default= lambda: round(uniform(1.5, 7.6),2))


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True)
    exporter_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    exporter: Mapped['Country'] = relationship(back_populates="exports")
    import_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    importer: Mapped['Country'] = relationship(back_populates="imports")
    date = Column(DateTime())
    total_amount = Column(Float())
    net_amount = Column(Float())
    product_category = Column(String(length=25), nullable=False)
    shipping_method = Column(String(length=15), nullable=False)


if __name__ == "__main__":
    engine = create_engine(DATABASE_URI)
    Country.metadata.create_all(engine)
    Record.metadata.create_all(engine)