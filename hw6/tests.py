import pickle
import pytest
from datetime import date, timedelta
from pathlib import Path
from main import AddressBook, Birthday, Field, Name, Phone, Record, AddressBookMeta

# --- Field ---


class TestField:
    def test_value(self):
        assert Field("test").value == "test"

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

    def test_inherits_field(self):
        assert isinstance(Name("John"), Field)


# --- Phone ---


class TestPhone:
    def test_valid(self):
        assert Phone("1234567890").value == "1234567890"

    def test_invalid_length_short(self):
        with pytest.raises(ValueError):
            Phone("123")

    def test_invalid_length_long(self):
        with pytest.raises(ValueError):
            Phone("12345678901")

    def test_invalid_non_digits(self):
        with pytest.raises(ValueError):
            Phone("123456789a")

    def test_eq_string(self):
        assert Phone("1234567890") == "1234567890"

    def test_eq_phone(self):
        assert Phone("1234567890") == Phone("1234567890")

    def test_neq_string(self):
        assert Phone("1234567890") != "0987654321"

    def test_neq_phone(self):
        assert Phone("1234567890") != Phone("0987654321")

    def test_eq_non_phone_returns_false(self):
        assert Phone("1234567890").__eq__(123) == False

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

    def test_invalid_string(self):
        with pytest.raises(ValueError):
            Birthday("not-a-date")

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

    def test_str(self):
        assert str(Birthday("01.01.1990")) == "01.01.1990"


# --- Record ---


class TestRecord:
    def test_init_name(self):
        assert Record("John").name.value == "John"

    def test_init_empty_phones(self):
        assert Record("John").phones == []

    def test_init_no_birthday(self):
        assert Record("John").birthday is None

    def test_init_with_phones(self):
        record = Record("John", phones=["1234567890", "0987654321"])
        assert len(record.phones) == 2

    def test_init_with_birthday(self):
        record = Record("John", birthday="01.01.1990")
        assert record.birthday.value == "01.01.1990"

    def test_add_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        assert len(record.phones) == 1

    def test_add_multiple_phones(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        assert len(record.phones) == 2

    def test_add_invalid_phone(self):
        with pytest.raises(ValueError):
            Record("John").add_phone("123")

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
        assert record.find_phone("1234567890") is None

    def test_edit_nonexistent_phone(self):
        with pytest.raises(ValueError):
            Record("John").edit_phone("1234567890", "0987654321")

    def test_find_phone_existing(self):
        record = Record("John")
        record.add_phone("1234567890")
        assert record.find_phone("1234567890").value == "1234567890"

    def test_find_phone_nonexistent(self):
        assert Record("John").find_phone("1234567890") is None

    def test_add_birthday(self):
        record = Record("John")
        record.add_birthday("01.01.1990")
        assert record.birthday.value == "01.01.1990"

    def test_add_birthday_invalid(self):
        with pytest.raises(ValueError):
            Record("John").add_birthday("not-a-date")

    def test_days_to_birthday_no_birthday(self):
        assert Record("John").days_to_birthday() is None

    def test_days_to_birthday_today(self):
        today = date.today()
        record = Record("John")
        record.add_birthday(today.strftime("%d.%m.1990"))
        assert record.days_to_birthday() == 0

    def test_days_to_birthday_tomorrow(self):
        tomorrow = date.today() + timedelta(days=1)
        record = Record("John")
        record.add_birthday(tomorrow.strftime("%d.%m.1990"))
        assert record.days_to_birthday() == 1

    def test_days_to_birthday_past_this_year(self):
        yesterday = date.today() - timedelta(days=1)
        record = Record("John")
        record.add_birthday(yesterday.strftime("%d.%m.1990"))
        assert 363 <= record.days_to_birthday() <= 365

    def test_str_with_phones_and_birthday(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.add_birthday("01.01.1990")
        result = str(record)
        assert "John" in result
        assert "1234567890" in result
        assert "01.01.1990" in result

    def test_str_without_phones(self):
        assert "не вказано" in str(Record("John"))

    def test_str_without_birthday(self):
        assert "не вказано" in str(Record("John"))


# --- AddressBook ---


@pytest.fixture
def book(tmp_path):
    AddressBook.FILE_PATH = tmp_path / "test_address_book.pkl"
    AddressBookMeta._instances.clear()  # clear after path is set
    return AddressBook()


@pytest.fixture
def populated_book(book):
    for i in range(5):
        record = Record(f"Contact{i}")
        record.add_phone(f"123456789{i}")
        book.add_record(record)
    return book


class TestAddressBook:
    def test_init_empty(self, book):
        assert book.data == {}

    def test_add_record(self, book):
        book.add_record(Record("John"))
        assert "John" in book.data

    def test_add_record_uses_name_as_key(self, book):
        record = Record("John")
        book.add_record(record)
        assert book.data["John"] is record

    def test_find_existing(self, book):
        record = Record("John")
        book.add_record(record)
        assert book.find("John") is record

    def test_find_nonexistent(self, book):
        assert book.find("Jane") is None

    def test_delete_existing(self, book):
        book.add_record(Record("John"))
        book.delete("John")
        assert "John" not in book.data

    def test_delete_nonexistent(self, book):
        book.delete("Jane")  # should not raise

    def test_iterator_single_page(self, book):
        book.add_record(Record("John"))
        pages = list(book.iterator(page_size=10))
        assert len(pages) == 1
        assert len(pages[0]) == 1

    def test_iterator_multiple_pages(self, populated_book):
        pages = list(populated_book.iterator(page_size=2))
        assert len(pages) == 3
        assert len(pages[0]) == 2
        assert len(pages[1]) == 2
        assert len(pages[2]) == 1

    def test_iterator_empty(self, book):
        assert list(book.iterator()) == []

    def test_iterator_page_size_larger_than_data(self, populated_book):
        pages = list(populated_book.iterator(page_size=100))
        assert len(pages) == 1
        assert len(pages[0]) == 5

    def test_save_and_load(self, tmp_path):
        save_path = tmp_path / "test_save.pkl"

        AddressBook.FILE_PATH = save_path
        book = AddressBook()
        record = Record("John")
        record.add_phone("1234567890")
        record.add_birthday("01.01.1990")
        book.add_record(record)
        book.save()

        AddressBook.FILE_PATH = save_path
        restored = AddressBook()
        restored.load()

        assert "John" in restored.data
        assert restored.find("John").find_phone("1234567890") is not None
        assert restored.find("John").birthday.value == "01.01.1990"

    def test_load_missing_file(self, book):
        book.load()  # FILE_PATH doesn't exist — should not raise
        assert book.data == {}

    def test_load_from_file_on_init(self, tmp_path):
        save_path = tmp_path / "preloaded.pkl"
        data = {"John": Record("John")}
        with open(save_path, "wb") as f:
            pickle.dump(data, f)

        AddressBook.FILE_PATH = save_path
        AddressBookMeta._instances.clear()  # reset after setting path
        book = AddressBook()
        assert "John" in book.data
