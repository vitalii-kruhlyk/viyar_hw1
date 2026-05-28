import pytest
from datetime import date, timedelta
from main import AddressBook, Birthday, Field, Name, Phone, Record

# --- Field ---


class TestField:
    def test_value(self):
        field = Field("test")
        assert field.value == "test"

    def test_str(self):
        assert str(Field("test")) == "test"

    def test_setter(self):
        field = Field("test")
        field.value = "updated"
        assert field.value == "updated"


# --- Name ---


class TestName:
    def test_value(self):
        assert Name("John").value == "John"


# --- Phone ---


class TestPhone:
    def test_valid(self):
        assert Phone("1234567890").value == "1234567890"

    def test_invalid_length(self):
        with pytest.raises(ValueError):
            Phone("123")

    def test_invalid_non_digits(self):
        with pytest.raises(ValueError):
            Phone("123456789a")

    def test_eq_string(self):
        assert Phone("1234567890") == "1234567890"

    def test_eq_phone(self):
        assert Phone("1234567890") == Phone("1234567890")

    def test_neq(self):
        assert Phone("1234567890") != Phone("0987654321")

    def test_setter_valid(self):
        phone = Phone("1234567890")
        phone.value = "0987654321"
        assert phone.value == "0987654321"

    def test_setter_invalid(self):
        phone = Phone("1234567890")
        with pytest.raises(ValueError):
            phone.value = "123"


# --- Birthday ---


class TestBirthday:
    def test_valid(self):
        assert Birthday("01.01.1990").value == "01.01.1990"

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            Birthday("1990-01-01")

    def test_invalid_date(self):
        with pytest.raises(ValueError):
            Birthday("32.01.1990")

    def test_date_property(self):
        assert Birthday("01.01.1990").date == date(1990, 1, 1)

    def test_setter_valid(self):
        bday = Birthday("01.01.1990")
        bday.value = "15.06.1995"
        assert bday.value == "15.06.1995"

    def test_setter_invalid(self):
        bday = Birthday("01.01.1990")
        with pytest.raises(ValueError):
            bday.value = "not-a-date"


# --- Record ---


class TestRecord:
    def test_init(self):
        record = Record("John")
        assert record.name.value == "John"
        assert record.phones == []
        assert record.birthday is None

    def test_add_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        assert len(record.phones) == 1

    def test_add_multiple_phones(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        assert len(record.phones) == 2

    def test_remove_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.remove_phone("1234567890")
        assert len(record.phones) == 0

    def test_remove_nonexistent_phone(self):
        record = Record("John")
        record.remove_phone("1234567890")  # should not raise
        assert len(record.phones) == 0

    def test_edit_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.edit_phone("1234567890", "0987654321")
        assert record.find_phone("0987654321") is not None

    def test_edit_nonexistent_phone(self):
        record = Record("John")
        with pytest.raises(ValueError):
            record.edit_phone("1234567890", "0987654321")

    def test_find_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        assert record.find_phone("1234567890").value == "1234567890"

    def test_find_nonexistent_phone(self):
        record = Record("John")
        assert record.find_phone("1234567890") is None

    def test_add_birthday(self):
        record = Record("John")
        record.add_birthday("01.01.1990")
        assert record.birthday.value == "01.01.1990"

    def test_days_to_birthday_no_birthday(self):
        assert Record("John").days_to_birthday() is None

    def test_days_to_birthday_future(self):
        tomorrow = date.today() + timedelta(days=1)
        record = Record("John")
        record.add_birthday(tomorrow.strftime("%d.%m.1990"))
        assert record.days_to_birthday() == 1

    def test_days_to_birthday_today(self):
        today = date.today()
        record = Record("John")
        record.add_birthday(today.strftime("%d.%m.1990"))
        assert record.days_to_birthday() == 0

    def test_days_to_birthday_past_this_year(self):
        yesterday = date.today() - timedelta(days=1)
        record = Record("John")
        record.add_birthday(yesterday.strftime("%d.%m.1990"))
        assert record.days_to_birthday() == 364

    def test_str(self):
        record = Record("John")
        record.add_phone("1234567890")
        assert "John" in str(record)
        assert "1234567890" in str(record)


# --- AddressBook ---


class TestAddressBook:
    def setup_method(self):
        self.book = AddressBook()
        self.record = Record("John")
        self.record.add_phone("1234567890")

    def test_add_record(self):
        self.book.add_record(self.record)
        assert "John" in self.book.data

    def test_find_existing(self):
        self.book.add_record(self.record)
        assert self.book.find("John") is self.record

    def test_find_nonexistent(self):
        assert self.book.find("Jane") is None

    def test_delete_existing(self):
        self.book.add_record(self.record)
        self.book.delete("John")
        assert "John" not in self.book.data

    def test_delete_nonexistent(self):
        self.book.delete("Jane")  # should not raise

    def test_iterator_single_page(self):
        self.book.add_record(self.record)
        pages = list(self.book.iterator(page_size=10))
        assert len(pages) == 1
        assert len(pages[0]) == 1

    def test_iterator_multiple_pages(self):
        for i in range(5):
            self.book.add_record(Record(f"Contact{i}"))
        pages = list(self.book.iterator(page_size=2))
        assert len(pages) == 3  # 2 + 2 + 1
        assert len(pages[0]) == 2
        assert len(pages[2]) == 1

    def test_iterator_empty(self):
        pages = list(self.book.iterator())
        assert pages == []
