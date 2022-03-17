import json
from pandas import DataFrame
from dataclasses import dataclass, field


@dataclass
class GradeBook:
    pages: list  # List of GradePages
    katalog: dict = field(repr=False)  # Dict of competence Number to Competence Name

    def __init__(self, katalog):
        self.katalog = katalog
        self.pages = []

    def add_page(self, name: str, grades: DataFrame):
        self.pages.append(GradePage(name, grades, self.katalog))


@dataclass
class GradePage:
    name: str
    grades: DataFrame = field(repr=False)
    modules: list = field(repr=False)  # list of Modules
    competences: list = field(repr=False)  # list of Competences
    katalog: dict = field(repr=False)  # Dict of competence Number to Competence Name

    def __init__(self, name: str, grades: DataFrame, katalog):
        self.name = name
        self.grades = grades
        self.modules = []
        self.competences = []
        self.katalog = katalog
        self.read_in()

    def read_in(self):
        for column_name in list(self.grades.columns):
            if column_name not in ["Schüler", 'Klasse', 'Gruppen', 'Email']:
                split = column_name.split(' ')[0].split('K')
                if len(split) > 1:
                    module_type = split[0]
                    module_number = split[1]
                    module = Module(column_name, module_number, module_type)
                    if len(module_number) >= 3:
                        competence_number = module_number[:2]
                        if competence_number in self.katalog:
                            competence = Competence(self.katalog[competence_number], competence_number)
                        else:
                            competence = Competence(
                                competence_number[0] + '.' + competence_number[1] + " Kompetenzbereich",
                                competence_number)
                        competence.modules.append(module)
                        module.competence = competence
                        self.modules.append(module)
                        self.competences.append(competence)


@dataclass
class Competence:
    name: str
    number_str: str
    modules: list = field(default_factory=list, repr=False)  # list of Modules


@dataclass
class Module:
    name: str
    number_str: str
    type: str
    competence: Competence = None


if __name__ == "__main__":
    df = DataFrame([['x', 'y', 'z', 'r']], columns=['GK321 balbla', 'EK532 asdfg', 'GEK844 jrfnn', 'asdjfj'])
    with open('modules.json', 'r') as f:
        module_names = json.load(f)
    gb = GradeBook(module_names)
    gb.add_page("1a", df)
    print(gb.pages)
    print(gb.pages[0].modules)
    print(gb.pages[0].competences)
