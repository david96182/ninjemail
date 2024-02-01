def get_birthdate(birthdate):
    birthdate_split = birthdate.split('-')

    return birthdate_split[0], birthdate_split[1], birthdate_split[2]
