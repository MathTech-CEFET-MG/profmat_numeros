#------------------------------------------------------------------------------#

from schools_list import schools_list

#------------------------------------------------------------------------------#
def create_schools(schools_path):
    """
    Create a file to list all dissertation of each school
    """

    for key, school in schools_list.items():

        file_path = schools_path / f"{key.lower()}.md"

        with open(file_path, "w", encoding="utf-8") as f:

            f.write(f"# Dissertações Defendidas {school[0]}<br>{school[1]} ({key})\n\n")


#------------------------------------------------------------------------------#
def add_to_school(schools_path, data, entry_path):
    """
    Add dissertation to year file
    """

    school = data["school"].lower()
    title  = data["title"]

    file_path = schools_path / f"{school}.md"

    with open(file_path, "a", encoding="utf-8") as f:

        f.write(f"- [{title}]({entry_path})\n")

#------------------------------------------------------------------------------#