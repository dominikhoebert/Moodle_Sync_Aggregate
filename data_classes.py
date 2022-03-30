import json
from pandas import DataFrame
from dataclasses import dataclass, field


class Module:
    pass


@dataclass
class Competence:
    name: str
    number_str: str
    modules: list[Module] = field(default_factory=list, repr=False)  # list of Modules


@dataclass
class Module:
    name: str
    number_str: str
    type: str
    competence: Competence = None
    column_letter: str = None


@dataclass
class GradePage:
    name: str
    grades: DataFrame = field(repr=False)
    modules: list[Module] = field(repr=False)  # list of Modules
    competences: list[Competence] = field(repr=False)  # list of Competences

    def __init__(self, name: str, grades: DataFrame, katalog: dict):
        self.name = name
        self.grades = grades
        self.modules = []
        self.competences = []
        self.read_in(katalog)

    def read_in(self, katalog: dict):
        for column_name in list(self.grades.columns):
            if column_name not in ["Schüler", 'Klasse', 'Gruppen', 'Email', 'Kurs']:
                split = column_name.split(' ')[0].split('K')
                if len(split) > 1:
                    module_type = split[0]
                    module_number = split[1]
                    module = Module(column_name, module_number, module_type)
                    if len(module_number) >= 3:
                        competence_number = module_number[:2]
                        if competence_number in katalog:
                            competence = Competence(katalog[competence_number], competence_number)
                        else:
                            competence = Competence(
                                competence_number[0] + '.' + competence_number[1] + " Kompetenzbereich",
                                competence_number)
                        competence.modules.append(module)
                        module.competence = competence
                        self.modules.append(module)
                        self.competences.append(competence)

    def get_module_by_name(self, name: str):
        for module in self.modules:
            if name == module.name:
                return module
        return None

    def get_modules_by_type(self, filter):
        modules = []
        for module in self.modules:
            if module.type in filter:
                modules.append(module)
        return modules


@dataclass
class GradeBook:
    pages: list[GradePage] = field(default_factory=list)  # List of GradePages
    katalog: dict = field(repr=False, default_factory=dict)  # Dict of competence Number to Competence Name

    def __init__(self, katalog: dict):
        self.katalog = katalog
        self.pages = []

    def add_page(self, name: str, grades: DataFrame):
        self.pages.append(GradePage(name, grades, self.katalog))

    def get_page_from_name(self, name: str):
        for page in self.pages:
            if page.name == name:
                return page
        return None


if __name__ == "__main__":
    df = DataFrame([['x', 'y', 'z', 'r']], columns=['GK321 balbla', 'EK532 asdfg', 'GEK844 jrfnn', 'asdjfj'])
    with open('modules.json', 'r') as f:
        module_names = json.load(f)
    # gb = GradeBook()
    gb = GradeBook(module_names)
    gb.add_page("1a", df)
    print(gb.pages)
    print(gb.pages[0].modules)
    print(gb.pages[0].competences)
