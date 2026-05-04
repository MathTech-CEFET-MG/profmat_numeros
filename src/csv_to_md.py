#------------------------------------------------------------------------------#

import csv
import hashlib
from pathlib import Path

from years        import create_years,   add_to_year
from schools      import create_schools, add_to_school
from dissertation import create_dissertation
from Numbers      import create_numbers

# Input CVS files
csv_path = Path("csv")
# input_csv = csv_path / "teste.csv"
input_csv = csv_path / "todas_as_dissertacoes.csv"

# Output directories
docs_path          = Path("docs")
dissertations_path = docs_path / "dissertations"
schools_path       = docs_path / "schools"
years_path         = docs_path / "years"
numbers_path       = docs_path / "numbers" / "numbers.md"


#------------------------------------------------------------------------------#
def hash_row(data):
    """
    Create a hash SHA256 based on line content
    """

    row_string = "|".join(data[col] for col in data)

    return hashlib.sha256(row_string.encode("utf-8")).hexdigest()

#------------------------------------------------------------------------------#
def main():

    create_years  (years_path)
    create_schools(schools_path)

    with open(input_csv, newline="", encoding="utf-8") as csv_file:

        reader = csv.DictReader(csv_file)

        ii = 0

        for row_data in reader:

            data = {}
            data["year"]   = row_data["Ano Corrigido"]
            data["date"]   = row_data["Data Corrigida"]
            data["author"] = row_data["Nome Corrigido"]
            data["title"]  = row_data["Título Corrigido"]
            data["school"] = row_data["Instituição Corrigida"]
            data["url"]    = row_data["URL"]
            data["note"]   = row_data["Note"]

            year = data["year"]

            entry_hash    = hash_row(data)
            entry_name    = f"{year}-{entry_hash}.md"
            entry_path    = dissertations_path / entry_name
            relative_path = Path("../dissertations/") / entry_name

            create_dissertation(entry_path,    data)
            add_to_year        (years_path,    data, relative_path)
            add_to_school      (schools_path,  data, relative_path)

            ii += 1

    create_numbers(numbers_path, ii)

    print(f"{ii} arquivos gerados com sucesso")


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------#
