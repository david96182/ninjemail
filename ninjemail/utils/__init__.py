from faker import Faker
from faker.providers import BaseProvider
import secrets
import string
import random


MONTHS_MAPPING = {
    '1': 'January',
    '2': 'February',
    '3': 'March',
    '4': 'April',
    '5': 'May',
    '6': 'June',
    '7': 'July',
    '8': 'August',
    '9': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

class CountryProvider(BaseProvider):
    def country(self):
        """
        Generate a random country name.

        Returns:
            str: A random country name.
        """
        countries = [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
            "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
            "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil",
            "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
            "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the",
            "Congo, Republic of the", "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic",
            "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
            "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia",
            "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
            "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
            "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos",
            "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar",
            "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
            "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)",
            "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
            "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea",
            "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
            "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
            "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
            "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
            "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste",
            "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
            "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu",
            "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
        ]
        return self.random_element(countries)

def get_birthdate(birthdate):
    birthdate_split = birthdate.split('-')

    return birthdate_split[0], birthdate_split[1], birthdate_split[2]

def  generate_missing_info(username, password, first_name, last_name, country, birthdate):
    """
    Generate missing information for a user.

    This function takes in various user information as parameters and generates missing values 
    for them if they are not provided. It uses the Faker library to generate fake data when needed.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        country (str): The country of the user.
        birthdate (str): The birthdate of the user in the format 'MM-DD-YYYY'.

    Returns:
        tuple: A tuple containing the generated or provided values for the username, password, 
               first name, last name, country, and birthdate in the same order.

    """
    fake = Faker()
    fake.add_provider(CountryProvider)

    if not password:
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(random.randint(8, 12)))

    if not first_name:
        first_name = fake.first_name()

    if not last_name:
        last_name = fake.last_name()

    if not country:
        country = fake.country()

    if not birthdate:
        birthdate = fake.date_of_birth(minimum_age=18)
        birthdate = f"{birthdate.month}-{birthdate.day}-{birthdate.year}"

    if not username:
        first_initial = first_name[0].lower()
        last_name = last_name.replace(" ", "").lower()
        year = birthdate.split('-')[2]

        random_number = random.randint(100, 999)
        username = f"{first_initial}{last_name}{year}{random_number}"
        
    return username, password, first_name, last_name, country, birthdate 

def get_month_by_number(month_number):
    """
    Get the month name by its number.

    Args:
        month_number (str): The number of the month (1-12).

    Returns:
        str: The name of the month.
    """
    return MONTHS_MAPPING.get(month_number.removeprefix('0'), "Invalid month number")
