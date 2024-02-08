from enum import StrEnum, auto
from datetime import datetime
from functools import partial
from dataclasses import dataclass, field
from random import randint, choice

class Countries(StrEnum):
    UNATED_STATES = auto()
    MEXICO = auto()
    ITALY = auto()
    CHINA = auto()
    FRANCE = auto()
    CHILE = auto()
    JAPAN = auto()
    SPAIN = auto()
    CANADA = auto()
    INDIA = auto()
    COLOMBIA = auto()
    GERMANY = auto()


class ProductCategories(StrEnum):
    FOOD = auto()
    ELECTRODOMESTIC = auto()
    ROW_MATERIAL = auto()
    MACHINES = auto()
    CLOTHS = auto()
    PLASTIC = auto()
    AUTOS = auto()
    METAL = auto()
    WOOD = auto()
    PLANTS = auto()


class TransportMethod(StrEnum):
    SHIP = auto()
    AIRCRAFT = auto()


@dataclass
class DateGen:
    year: bool = field(init=False)
    month: int = field(init=False) 
    day: int  = field(init=False)

    def __post_init__(self):
        self.set_year()
        self.month = randint(1, 12)
        self.day = randint(1,31)

    @property
    def is_valid_date(self) -> bool:
        """Check if the date is valid

        Returns:
            bool: True if the date is valid, False otherwise
        """
        try:
            datetime(year=self.year, month=self.month, day=self.day)
            return True
        except ValueError:
            return False
        
    def set_year(self) -> None:
        """Ramdonly chooses a year between 2022 or 2023
        """
        if randint(0, 1):
            self.year = 2022
        else:
            self.year = 2023
        
    def generate_date(self) -> datetime:
        """Generates a date with the random values asigned after the initiation and 
         check if the date is valid.

        Returns:
            datetime: a datetime instance with the format YYYY-MM-DD HH:MM:SS
        """
        while not self.is_valid_date:
            self.day -= 1
        return datetime(year=self.year, month=self.month, day=self.day)


@dataclass
class CountriesSelector:
    """Class that selects countries from the Contries class as exporter and importer"""
    importer: Countries = field(init=False, default_factory=lambda: choice(Countries._member_names_))
    exporter: Countries = field(init=False, default_factory=lambda: choice(Countries._member_names_))

    def __post_init__(self):
        self.country_match()
    
    def country_match(self):
        while self.exporter == self.importer:
            self.importer = choice(Countries._member_names_)
    
    
if __name__ == '__main__':
    date_gen = DateGen()
    picker = CountriesSelector()
    print(date_gen.generate_date())
    print(choice(Countries._member_names_))
    print(picker.exporter, picker.importer)