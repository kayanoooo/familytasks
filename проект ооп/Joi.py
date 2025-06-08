class Book:
    def __init__(self, genre=None, author=None):
        self.genre = genre
        self.author = author

    def __str__(self):
        return f"Книга: {self.genre}, автор: {self.author}"


# Создание книги с инициализацией
book1 = Book("Роман", "Лев Толстой")
print(book1)

book1.genre = "dfqjmi"
print(book1)