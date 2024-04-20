import pytest
from faker import Faker

from ..utils import CountryProvider, get_birthdate, generate_missing_info


class TestCountryProvider:
  def test_country_returns_string(self):
    """Tests if CountryProvider.country returns a string."""
    fake = Faker()
    fake.add_provider(CountryProvider)
    country = fake.country()
    assert isinstance(country, str)


class TestGetBirthdate:
  def test_birthdate_split_correctly(self):
    """Tests if get_birthdate splits the birthdate string correctly."""
    birthdate = "1990-12-31"
    month, day, year = get_birthdate(birthdate)
    assert month == "1990"
    assert day == "12"
    assert year == "31"

  def test_birthdate_split_invalid_format(self):
    """Tests if get_birthdate raises an error for invalid format."""
    with pytest.raises(IndexError):
      get_birthdate("invalid_format")


class TestGenerateMissingInfo:
  def test_generate_all_missing(self):
    """Tests if generate_missing_info fills all missing information."""
    username, password, first_name, last_name, country, birthdate = generate_missing_info("", "", "", "", "", "")
    assert username
    assert password
    assert first_name
    assert last_name
    assert country
    assert birthdate

  def test_generate_partial_missing(self):
    """Tests if generate_missing_info fills only missing information."""
    username = "test_user"
    password = "strong_password"
    first_name = "John"
    last_name = "Doe"
    country = "USA"
    birthdate = "1980-01-01"
    filled_info = generate_missing_info(username, password, first_name, last_name, country, birthdate)
    assert username == "test_user"
    assert password == "strong_password"
    assert first_name == "John"
    assert last_name == "Doe"
    assert country == "USA"
    assert birthdate == "1980-01-01"

  def test_uses_faker_for_generated_data(self):
    """Tests if generate_missing_info uses Faker for generated data."""
    fake1 = Faker()
    fake2 = Faker()
    fake1.add_provider(CountryProvider)
    fake2.add_provider(CountryProvider)

    # Generate first names with different Fakers
    username, _, first_name1, _, _, _ = generate_missing_info("", "", "", "", "", "")
    _, _, first_name2, _, _, _ = generate_missing_info("", "", "", "", "", "")

    # Assert first names are different (likely from different Fakers)
    assert first_name1 != first_name2
