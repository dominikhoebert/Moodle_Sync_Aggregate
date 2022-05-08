import configparser


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.read()

    def read(self):
        self.config.read(self.filename)
        if not self.config.sections():
            self.create_default()

    def write(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def create_default(self):
        self.config['Moodle_Sync_Aggregate'] = {'qsettingscompany': 'TGM',
                                                'qsettingsapplication': 'Moodle_Sync_Grading'}
        con = self.config['Moodle_Sync_Aggregate']
        con['MoodleURL'] = 'https://elearning.tgm.ac.at'
        con['Service_name'] = 'tgm_hoedmoodlesync'
        con['Username_extension'] = '@tgm.ac.at'
        con['cache_grades'] = 'false'
        con['marksuggestions'] = 'false'
        con['competence_columns'] = 'false'
        con['negative_competences'] = 'false'
        con['competence_counter'] = 'false'
        con['wh_calculation'] = 'false'
        con['ldap_student_list_path'] = 'ldap_studentlist.csv'
        con['ldap_url'] = 'ldap://dc-01.tgm.ac.at:389'

        self.write()
