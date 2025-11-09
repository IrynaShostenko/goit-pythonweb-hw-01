"""Homework 2 — SOLID library example with CLI."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, List


# ──────────────── SRP: єдина відповідальність ────────────────
@dataclass(frozen=True)
class Book:
    """Сутність книги: єдина відповідальність — зберігання даних."""

    title: str
    author: str
    year: int

    def __str__(self) -> str:
        """Рядкове представлення книги."""
        return f'Title: "{self.title}", Author: {self.author}, Year: {self.year}'


# ──────────────── ISP: чіткий, мінімальний контракт ────────────────
class LibraryInterface(ABC):
    """Контракт бібліотеки: додати, видалити, отримати книги."""

    @abstractmethod
    def add_book(self, book: Book) -> None:
        """Додає книгу до сховища."""
        raise NotImplementedError

    @abstractmethod
    def remove_book(self, title: str) -> bool:
        """Видаляє першу книгу за назвою (case-insensitive). Повертає True, якщо видалено."""
        raise NotImplementedError

    @abstractmethod
    def get_books(self) -> Iterable[Book]:
        """Повертає ітерабельну колекцію книг."""
        raise NotImplementedError


# ─────────────── LSP: базова реалізація, взаємозамінна ───────────────
class InMemoryLibrary(LibraryInterface):
    """Проста бібліотека в пам'яті."""

    def __init__(self) -> None:
        """Ініціалізує порожнє сховище книг."""
        self._books: List[Book] = []

    def add_book(self, book: Book) -> None:
        """Додає книгу до пам'яті."""
        self._books.append(book)

    def remove_book(self, title: str) -> bool:
        """Видаляє перший збіг за назвою, ігноруючи регістр."""
        t = title.lower()
        for idx, b in enumerate(self._books):
            if b.title.lower() == t:
                del self._books[idx]
                return True
        return False

    def get_books(self) -> Iterable[Book]:
        """Повертає знімок поточного списку книг."""
        return list(self._books)


# ─────────────── OCP: розширення через декоратори ───────────────
class LoggingLibraryDecorator(LibraryInterface):
    """Декоратор логування операцій add/remove, не змінюючи базову бібліотеку."""

    def __init__(self, inner: LibraryInterface) -> None:
        """Зберігає посилання на внутрішню реалізацію бібліотеки."""
        self._inner = inner

    def add_book(self, book: Book) -> None:
        """Логує й делегує додавання книги."""
        print(f"[LOG] add: {book}")
        self._inner.add_book(book)

    def remove_book(self, title: str) -> bool:
        """Логує й делегує видалення книги за назвою."""
        print(f'[LOG] remove: "{title}"')
        return self._inner.remove_book(title)

    def get_books(self) -> Iterable[Book]:
        """Делегує отримання всіх книг."""
        return self._inner.get_books()


class SortedViewLibrary(LibraryInterface):
    """Представлення, що повертає книги відсортованими за назвою (та роком)."""

    def __init__(self, inner: LibraryInterface) -> None:
        """Зберігає внутрішню реалізацію для делегування операцій."""
        self._inner = inner

    def add_book(self, book: Book) -> None:
        """Делегує додавання книги."""
        self._inner.add_book(book)

    def remove_book(self, title: str) -> bool:
        """Делегує видалення книги за назвою."""
        return self._inner.remove_book(title)

    def get_books(self) -> Iterable[Book]:
        """Повертає відсортований список книг."""
        return sorted(self._inner.get_books(), key=lambda b: (b.title.lower(), b.year))


# ─────────────── DIP: високорівневий менеджер залежить від абстракції ───────────────
class LibraryManager:
    """Керує сценаріями: валідація вводу, взаємодія з бібліотекою, вивід."""

    def __init__(self, library: LibraryInterface) -> None:
        """Приймає абстрактну бібліотеку, а не конкретну реалізацію."""
        self._lib = library

    def add_book(self, title: str, author: str, year_raw: str) -> None:
        """Валідує дані, створює Book та додає до бібліотеки."""
        year = self._parse_year(year_raw)
        self._lib.add_book(Book(title=title, author=author, year=year))
        print("Book added.")

    def remove_book(self, title: str) -> None:
        """Видаляє книгу за назвою та повідомляє результат."""
        ok = self._lib.remove_book(title)
        print("Book removed." if ok else "Book not found.")

    def show_books(self) -> None:
        """Друкує всі книги або повідомляє, що бібліотека порожня."""
        books = list(self._lib.get_books())
        if not books:
            print("No books in library.")
            return
        for b in books:
            print(b)

    @staticmethod
    def _parse_year(value: str) -> int:
        """Парсить рік; має бути додатним цілим. Підіймає ValueError з причиною."""
        try:
            year = int(value)
            if year <= 0:
                raise ValueError("non-positive")
            return year
        except ValueError as exc:
            raise ValueError("Year must be a positive integer.") from exc


# ─────────────── CLI ───────────────
def main() -> None:
    """Точка входу в консольний застосунок (цикл команд)."""
    base = InMemoryLibrary()
    with_logging = LoggingLibraryDecorator(base)
    sorted_view = SortedViewLibrary(with_logging)

    manager = LibraryManager(sorted_view)

    while True:
        command = input("Enter command (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                year = input("Enter book year: ").strip()
                try:
                    manager.add_book(title, author, year)
                except ValueError as exc:
                    print(f"Error: {exc}")
            case "remove":
                title = input("Enter book title to remove: ").strip()
                manager.remove_book(title)
            case "show":
                manager.show_books()
            case "exit":
                break
            case _:
                print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
