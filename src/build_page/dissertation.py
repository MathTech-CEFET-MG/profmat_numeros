#------------------------------------------------------------------------------#

from biblatex import biblatex
from abnt     import abnt

#------------------------------------------------------------------------------#
def create_dissertation(file_path, data):
    """
    Create a markdown file to a dissertation
    """

    date   = data["date"]
    author = data["author"]
    title  = data["title"]
    school = data["school"]
    note   = data["note"]

    with open(file_path, "w", encoding="utf-8") as f:

        f.write(f"# {title}\n\n")
        f.write(f"Autor: __{author}__\n\n")
        f.write(f"Defendida na __{school}__ em {date}\n\n")

        if note:
            f.write(f"Observação: {note}\n\n")

        f.write('??? abstract "Como citar essa dissertação"\n')
        f.write('    __ABNT__\n\n')
        f.write(f"\n    > {abnt(data)}\n\n")
        f.write('    __BibLaTeX__\n\n')
        f.write('    ```latex\n')
        f.write(biblatex(data))
        f.write('    ```\n\n')

#------------------------------------------------------------------------------#