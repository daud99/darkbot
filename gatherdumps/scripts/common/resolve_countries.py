from iso3166 import countries

def name_to_alpha3(query):
    country = None
    try:
        country = countries.get(query)
    except Exception as e:
        country = None
    
    if (country):
        return country.alpha3
    else:
        return None

if __name__ == "__main__":
    print(name_to_alpha3('GBR'))
    st = "AB09GGf"
    print(st.lower())

    