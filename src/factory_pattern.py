"""Homework 1: Abstract Factory for vehicles (US/EU specs)."""

from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Базовий абстрактний транспортний засіб з інтерфейсом запуску двигуна."""

    def __init__(self, make: str, model: str) -> None:
        """Ініціалізує марку та модель."""
        self.make = make
        self.model = model

    @abstractmethod
    def start_engine(self) -> None:
        """Запускає двигун/мотор транспортного засобу."""
        raise NotImplementedError


class Car(Vehicle):
    """Легковий автомобіль."""

    def start_engine(self) -> None:
        """Імітує запуск двигуна авто."""
        print(f"{self.make} {self.model}: Двигун запущено")


class Motorcycle(Vehicle):
    """Мотоцикл."""

    def start_engine(self) -> None:
        """Імітує запуск мотора мотоцикла."""
        print(f"{self.make} {self.model}: Мотор заведено")


class VehicleFactory(ABC):
    """Абстрактна фабрика для створення транспортних засобів."""

    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        """Створює автомобіль з потрібними регіональними налаштуваннями."""
        raise NotImplementedError

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Створює мотоцикл з потрібними регіональними налаштуваннями."""
        raise NotImplementedError


class USVehicleFactory(VehicleFactory):
    """Фабрика США: додає позначку (US Spec)."""

    SPEC_SUFFIX = "(US Spec)"

    def create_car(self, make: str, model: str) -> Car:
        """Створює авто під специфікацію США."""
        return Car(make, f"{model} {self.SPEC_SUFFIX}")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Створює мотоцикл під специфікацію США."""
        return Motorcycle(make, f"{model} {self.SPEC_SUFFIX}")


class EUVehicleFactory(VehicleFactory):
    """Фабрика ЄС: додає позначку (EU Spec)."""

    SPEC_SUFFIX = "(EU Spec)"

    def create_car(self, make: str, model: str) -> Car:
        """Створює авто під специфікацію ЄС."""
        return Car(make, f"{model} {self.SPEC_SUFFIX}")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Створює мотоцикл під специфікацію ЄС."""
        return Motorcycle(make, f"{model} {self.SPEC_SUFFIX}")


if __name__ == "__main__":

    us_factory = USVehicleFactory()
    eu_factory = EUVehicleFactory()

    us_car = us_factory.create_car("Ford", "Mustang")
    us_car.start_engine()

    eu_bike = eu_factory.create_motorcycle("Yamaha", "MT-07")
    eu_bike.start_engine()

    eu_car = eu_factory.create_car("Toyota", "Corolla")
    eu_car.start_engine()
