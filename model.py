from abc import ABC, abstractmethod

# Superclasse de preço
class Price(ABC):

    @abstractmethod
    def get_charge(self, days_rented: int) -> float:
        pass

    def get_frequent_renter_points(self, days_rented: int) -> int:
        return 1

# Subclasse para livros REGULAR
class RegularPrice(Price):

    def get_charge(self, days_rented: int) -> float:
        amount = 2
        if days_rented > 2:
            amount += (days_rented - 2) * 1.5
        return amount

# Subclasse para livros NEW_RELEASE
class NewReleasePrice(Price):

    def get_charge(self, days_rented: int) -> float:
        return days_rented * 3

    def get_frequent_renter_points(self, days_rented: int) -> int:
        return 2 if days_rented > 1 else 1

# Subclasse para livros CHILDREN
class ChildrenPrice(Price):

    def get_charge(self, days_rented: int) -> float:
        amount = 1.5
        if days_rented > 3:
            amount += (days_rented - 3) * 1.5
        return amount

# Classe Book agora usa Price ao invés de price_code
class Book:

    REGULAR = 0
    NEW_RELEASE = 1
    CHILDREN = 2

    def __init__(self, title: str, price_code: int):
        self.title = title
        self.set_price_code(price_code)

    def set_price_code(self, price_code: int):
        if price_code == Book.REGULAR:
            self.price = RegularPrice()
        elif price_code == Book.NEW_RELEASE:
            self.price = NewReleasePrice()
        elif price_code == Book.CHILDREN:
            self.price = ChildrenPrice()
        else:
            raise ValueError("Invalid price code")

    def get_charge(self, days_rented: int) -> float:
        return self.price.get_charge(days_rented)

    def get_frequent_renter_points(self, days_rented: int) -> int:
        return self.price.get_frequent_renter_points(days_rented)

# Classe Rental permanece igual
class Rental:
    def __init__(self, book: Book, days_rented: int):
        self.book = book
        self.days_rented = days_rented

    def get_charge(self) -> float:
        return self.book.get_charge(self.days_rented)

    def get_frequent_renter_points(self) -> int:
        return self.book.get_frequent_renter_points(self.days_rented)

# Classe Client também permanece praticamente igual
class Client:

    def __init__(self, name: str):
        self.name = name
        self.rentals = []

    def add_rental(self, rental: Rental):
        self.rentals.append(rental)

    def statement(self) -> str:
        total_amount = 0
        frequent_renter_points = 0
        result = f"Rental summary for {self.name}\n"
        
        for rental in self.rentals:
            amount = rental.get_charge()
            frequent_renter_points += rental.get_frequent_renter_points()

            result += f"- {rental.book.title}: {amount}\n"
            total_amount += amount
        
        result += f"Total: {total_amount}\n"
        result += f"Points: {frequent_renter_points}"
        return result
