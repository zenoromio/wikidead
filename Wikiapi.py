import wikipediaapi
import json

wiki_wiki = wikipediaapi.Wikipedia("en")

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
years = range(1990, 2023)
json_final = {}

# generates link for wikideaths
def genera_link(year, month):
    link = "Deaths_in_" + month + "_" + str(year)
    return link


# get dead people from one specific day
def get_exact_day(year, month, day):
    # get whole page of deaths in month of year
    page = wiki_wiki.page(genera_link(year, month)).sections[0].sections

    # divide page in arrays of strings with people's information from that day
    page_array = page[day - 1].text.split("\n")

    # divide information for each person with a comma
    splitted_array = [p.split(", ") for p in page_array]

    # select just the first two items (name and age)
    name_age_array = [a[0:2] for a in splitted_array]

    # check that there are just two items and age is an int
    final_array = [a for a in name_age_array if len(a) == 2 and a[1].isdigit()]

    # create a dict with key = name and value = age
    dict_of_day = {}
    for person in final_array:
        dict_of_day[person[0]] = int(person[1])

    return dict_of_day

# creates json file with whole dataset
def get_json_file():
    for year in years:
        json_final[year] = {}

        for month in months:
            json_final[year][month] = {}

            wiki = wiki_wiki.page(genera_link(year, month)).sections[0].sections

            for index, day in enumerate(wiki):
                page_array = day.text.split("\n")
                splitted_array = [p.split(", ") for p in page_array]
                name_age_array = [a[0:2] for a in splitted_array]
                final_array = [a for a in name_age_array if len(a) == 2 and a[1].isdigit()]
                dict_of_day = {}
                for person in final_array:
                    dict_of_day[person[0]] = int(person[1])

                json_final[year][month][index + 1] = dict_of_day


# call the function and create dataset
get_json_file()
# save dataset to desktop (insert your own location path)
with open("necrology.json", "w") as f:
    f.write(json.dumps(json_final))

'''
# extra 
# code to load your data and search people
with open("/Users/zenoromio/Desktop/necrology.json", "r") as f:
    file = json.load(f)

print(file["1995"]["February"]["8"]["Józef Maria Bocheński"])
'''