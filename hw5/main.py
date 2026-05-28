from collections import UserDict
from datetime import date, datetime
from typing import Generator


class Field:
    _value: str

    def __init__(self, value: str) -> None:
        self.value = value # -> setter -> '_value' field

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, val: str) -> None:
        self._value = val

    def __str__(self) -> str:
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    _value: str | None

    @Field.value.setter
    def value(self, val: str) -> None:
        if not val.isdigit() or len(val) != 10:
            raise ValueError(
                f"Не виконується умова: телефон має бути числом з довжиною 10 символів. Отримано значення '{val}' довжиною {len(val)} символів."
            )
        self._value = val

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self._value == other
        if isinstance(other, Phone):
            return self._value == other._value
        return False


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    @Field.value.setter
    def value(self, val: str) -> None:
        try:
            datetime.strptime(val, self.DATE_FORMAT)
        except ValueError:
            raise ValueError(f"День народження має бути в форматі DD.MM.YYYY, отримано: {val}")
        self._value = val

    @property
    def date(self) -> date:
        return datetime.strptime(self._value, self.DATE_FORMAT).date()


class Record:
    name: Name
    phones: list[Phone]
    birthday: Birthday | None

    def __init__(self, name: str, phones: list[str] | None = None, birthday: str | None = None) -> None:
        self.name = Name(name)
        self.phones = [Phone(p) for p in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None

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

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def days_to_birthday(self) -> int | None:
        if not self.birthday:
            return None
        today = date.today()
        next_bday = self.birthday.date.replace(year=today.year)
        if next_bday < today:
            next_bday = next_bday.replace(year=today.year + 1)
        return (next_bday - today).days

    def __str__(self) -> str:
        phones_part = f"номера: {'; '.join(p.value for p in self.phones) if self.phones else 'не вказано'}"
        bday_part = f"день народження: {self.birthday if self.birthday else 'не вказано'}"
        return f"Власник: {self.name.value}, {phones_part}, {bday_part}"


class AddressBook(UserDict[str, Record]):
    data: dict[str, Record]

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def iterator(self, page_size: int = 10) -> Generator[list[Record], None, None]:
        records = list(self.data.values())
        for i in range(0, len(records), page_size):
            yield records[i : i + page_size]