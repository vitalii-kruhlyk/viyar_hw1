from collections import UserDict
from dataclasses import dataclass


@dataclass
class Field:
    value: str

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class Name(Field):
    pass


@dataclass
class Phone(Field):
    def __post_init__(self) -> None:
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError(
                f"Не виконується умова: телефон має бути числом з довжиною 10 символів. Отримано значення '{self.value}' довжиною {len(self.value)} символів."
            )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, Phone):
            return self.value == other.value
        return False


class Record:
    name: Name
    phones: list[Phone]

    def __init__(self, name: str, phones: list | None = None) -> None:
        self.name = Name(name)
        self.phones = phones if phones is not None else []

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        match = self.find_phone(phone)
        if match:
            self.phones.remove(match)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        match = self.find_phone(old_phone)
        if match:
            self.phones[self.phones.index(match)] = Phone(new_phone)
        else:
            raise ValueError(f"Номер {old_phone} не знайдено")

    def find_phone(self, phone: str) -> Phone | None:
        for saved_phone in self.phones:
            if saved_phone == phone:
                return saved_phone
        return None

    def __str__(self) -> str:
        return f"Власник: {self.name.value}, номера: {'; '.join(phone.value for phone in self.phones)}"


class AddressBook(UserDict[str, Record]):
    records: dict[str, Record]

    def add_record(self, record: Record) -> None:
        self.records[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.records.get(name)

    def delete(self, name: str) -> None:
        if name in self.records:
            del self.records[name]
