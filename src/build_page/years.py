#------------------------------------------------------------------------------#

from datetime import date

#------------------------------------------------------------------------------#
def create_years(years_path):
    """
    Create a file to list all dissertation of year
    """

    last_year = date.today().year + 1

    for year in range(2013, last_year):

        with open(years_path / f"{year}.md", "w", encoding="utf-8") as f:

            f.write(f"# Dissertações Defendidas no Ano {year}\n\n")


#------------------------------------------------------------------------------#
def add_to_year(years_path, data, entry_path):
    """
    Add dissertation to year file
    """

    year  = data["year"]
    title = data["title"]

    file_path = years_path / f"{year}.md"

    with open(file_path, "a", encoding="utf-8") as f:

        f.write(f"- [{title}]({entry_path})\n")


#------------------------------------------------------------------------------#