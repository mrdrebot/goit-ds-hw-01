from collections import UserDict
from datetime import datetime, date, timedelta
from typing import List, Union, Optional, Dict

class Field:
    def __init__(self, value: Union[str, datetime]):
        self.value: Union[str, datetime] = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    def __init__(self, name: str):
        if name:
            super().__init__(name)
        else:
            raise ValueError("You have not enterd name!")

class Phone(Field):
    def __init__(self, phone: str):
        if len(phone) == 10 and phone.isdigit():
            super().__init__(phone)
        else:
            raise ValueError("You have enterd less than 10 digitals in the number!")
        
class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.birthday: Optional[Birthday] = None
        self.phones: List[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        new_phone = Phone(phone_number)
        self.phones.append(new_phone)

    def add_birthday(self, birthday_date: str) -> None:
        self.birthday = Birthday(birthday_date)

    def remove_phone(self, remove_phone: str) -> None:
        for phone in self.phones:
            if phone.value == remove_phone:
                self.phones.remove(phone)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        old_p = Phone(old_phone)
        new_p = Phone(new_phone)

        if not any(old_phone == phone.value for phone in self.phones):
            raise ValueError("The entered number wasn`t found!")

        for phone in self.phones:
            if phone.value == old_p.value:
                phone.value = new_p.value

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
            
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday date: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, user_record) -> None:
          self.data[user_record.name.value] = user_record

    def find(self, contact_name: str) -> Optional[Record]:
        return self.data.get(contact_name)
    
    def delete(self, contact_name: str) -> None:
        self.data.pop(contact_name)

    def get_upcoming_birthdays(self) -> str:
        def find_next_weekday(start_date: date, weekday: int):
            days_ahead = weekday - start_date.weekday()

            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days=days_ahead)

        def adjust_for_weekend(birthday) -> datetime:
            if birthday.weekday() >= 5:
                return find_next_weekday(birthday, 0)
            return birthday
        
        days = 7
        upcoming_birthdays: List[Dict[str, str]] = []
        today: date = date.today()

        for user_name, user_data in self.data.items():
            if user_data.birthday:
                birthday_this_year = user_data.birthday.value.replace(year=today.year)

                if birthday_this_year.date() < today:
                    birthday_this_year = user_data.birthday.value.replace(year=today.year + 1)

                if 0 <= (birthday_this_year.date() - today).days <= days:
                    birthday_this_year = adjust_for_weekend(birthday_this_year)
                    congratulation_date_str: str = birthday_this_year.strftime("%Y.%m.%d")
                    upcoming_birthdays.append({"name": user_name, "birthday": congratulation_date_str})

        return f"Upcoming birthdays:\n { '; '.join(f"Name: {birthday['name']}, Upcoming birthday: {birthday['birthday']}" for birthday in upcoming_birthdays)}"

    def __str__(self) -> str:
        return f"Contacts:\n{"\n".join(str(user_data) for user_data in self.data.values())}"
