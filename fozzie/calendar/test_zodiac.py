import swisseph as swe
from datetime import date

def get_zodiac_sign(date: date) -> str:
    jd = swe.julday(date.year, date.month, date.day)
    lon = swe.calc_ut(jd, swe.SUN)[0][0]
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return signs[int(lon // 30)]

print(get_zodiac_sign(date(2025, 3, 26)))  # Should print "Aries"
