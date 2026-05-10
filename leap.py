def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
print("2000:", is_leap_year(2000))
print("1900:", is_leap_year(1900))
print("2024:", is_leap_year(2024))
print("2023:", is_leap_year(2023))
