from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import create_engine
from sqlalchemy import String, Float, Column, ForeignKey, DateTime, Integer
from random import uniform
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URI = getenv('DATABASE_URI')

class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=30), nullable=False, unique=True)
    export_tax = Column(Float(), default=lambda: round(uniform(0.5, 1.5), 2))
    import_tax = Column(Float(), default=lambda: round(uniform(1.5, 7.6), 2))
    exports = relationship("Record", back_populates="exporter", foreign_keys="[Record.exporter_id]")
    imports = relationship("Record", back_populates="importer", foreign_keys="[Record.importer_id]")

    def __repr__(self) -> str:
        return f"Country: {self.name}"

class Record(Base):

    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    exporter_id = Column(Integer, ForeignKey("countries.id"))
    exporter = relationship("Country", back_populates="exports", foreign_keys=[exporter_id])
    importer_id = Column(Integer, ForeignKey("countries.id"))
    importer = relationship("Country", back_populates="imports", foreign_keys=[importer_id])
    date = Column(DateTime())
    total_amount = Column(Float())
    net_amount = Column(Float())
    product_category = Column(String(length=25), nullable=False)
    shipping_method = Column(String(length=15), nullable=False)

    def __repr__(self) -> str:
        return f"record n.{self.id}"


if __name__ == "__main__":
    engine = create_engine(DATABASE_URI)
    Country.metadata.create_all(engine)
    Record.metadata.create_all(engine)