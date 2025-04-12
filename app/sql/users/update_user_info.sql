UPDATE user_info
SET
    first_name = COALESCE(%(first_name)s, nvl(first_name, '')),
    last_name = COALESCE(%(last_name)s, nvl(last_name, '')),
    age = COALESCE(%(age)s, nvl(age, '')),
    gender = COALESCE(%(gender)s, nvl(gender, '')),
    occupation = COALESCE(%(occupation)s, nvl(occupation, '')),
    income = COALESCE(%(income)s, nvl(income, '')),
    maritial_status = COALESCE(%(marital_status)s, nvl(marital_status, '')),
    has_children = COALESCE(%(has_children)s, nvl(has_children, '')),
    has_vechicles = COALESCE(%(has_vehicles)s, nvl(has_vehicles, '')),
    has_home = COALESCE(%(has_home)s, nvl(has_home, '')),
    has_mediical_conditions = COALESCE(%(has_medical_conditions)s, nvl(has_medical_conditions, '')),
    travel_frequency = COALESCE(%(travel_frequency)s, nvl(travel_frequency, ''))
WHERE id = %(id)s;

UPDATE users
SET
    name = COALESCE(%(name)s, name),
    updated_at = NOW()
WHERE id = %(id)s;