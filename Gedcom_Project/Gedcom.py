# design classes
# global names
from datetime import timedelta, date
import time
import datetime
import prettytable

INFO_TAGS = {'NAME': 'Name', 'SEX': 'Gender'}
FAM_TAGS = {'FAMC': 'Child', 'FAMS': 'Spouse'}
DATE_TAGS = {'BIRT': 'Birthday', 'DEAT': 'Death'}
FAM_DATE_TAGS = {'MARR': 'Married', 'DIV': 'Divorced'}
RELATION_TAGS = {'HUSB': 'Husband_ID', 'WIFE': 'Wife_ID'}
CHILD = {'CHIL': 'Children'}
MONTHS = {
    'JAN': 1,
    'FEB': 2,
    'MAR': 3,
    'APR': 4,
    'MAY': 5,
    'JUN': 6,
    'JUL': 7,
    'AUG': 8,
    'SEP': 9,
    'OCT': 10,
    'NOV': 11,
    'DEC': 12}
INDIVIDUAL = 'INDI'
FAMILY = 'FAM'
ZERO_LEVEL_TRIVIAL_LINE_SEGMENTS_LENGTH = 2

# supporting functions
def families(gedcom):
    return list(gedcom.get_families().values())

def individuals(gedcom):
    return list(gedcom.get_individuals().values())

def divorce_date(family):
    return family.get_divorce_date()

def marriage_date(family):
    return family.get_marriage_date()

def id_(Instance):
    # this instance can either be family or individual
    return Instance.get_id()

def wife(family):
    return family.get_wife_id()

def husband(family):
    return family.get_husband_id()

def parents(individual):
    parents = []
    for _, family in individual.get_parent_families().items():
        parents.append(husband(family))
        parents.append(wife(family))
    return parents

def has_own_family(individual):
    return len(individual.get_own_families()) > 0

def children(family):
    return list(family.get_children().values())

"""
def cousins(individual):
    cousins = []
    for _, family in individual.get_parent_families().items():
        parents_ids = [husband(family), wife(family)]
        for parent_id in parents_ids:
            parent = .get_individual_by_id(parent_id)
            for sibling in parent.find_all_siblings():
                if sibling.get_own_family():
                    cousins += [x.get_id() for x in sibling.get_own_family().get_children()]
    return cousins
"""               

# Gedcom is a tree including families and individuals
class Gedcom:
    def __init__(self):
        self.__individual_dict = {}
        self.__family_dict = {}

    def parse(self, file_path):
        # read in file line by line
        # create individuals, storing in the __individual_dict
        # create families, storing in the __family_dict
        with open(file_path, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                segments = lines[i].strip().split()
                if segments[0] == '0' and len(segments) > ZERO_LEVEL_TRIVIAL_LINE_SEGMENTS_LENGTH:
                    row_dict = {'id': segments[1]}
                    if segments[2] == INDIVIDUAL:
                        row_dict, i = self.__generate_individual_dict(lines, i+1, row_dict)
                        indi = Individual()
                        indi.read_in(row_dict)
                        self.__add_an_individual(indi)
                    elif segments[2] == FAMILY:
                        row_dict, i = self.__generate_family_dict(lines, i+1, row_dict)
                        fam = Family()
                        fam.read_in(row_dict)
                        self.__add_a_family(fam)
                    else:
                        i += 1
                else:
                    #print("Warning: This line may contain incorrect format or be skipped.")
                    #print(lines[i])
                    i += 1
        self.__connect()
        self.__update_derivative_attributes()
        #self.print_individuals()
        #self.print_families()

    def __generate_individual_dict(self, lines, start_index, indi_row):
        while start_index < len(lines):
            line = lines[start_index].strip()
            if line.startswith('1'):
                segments = line.split()
                if segments[1] in INFO_TAGS:
                    indi_row[INFO_TAGS[segments[1]]] = ' '.join(segments[2:])
                elif segments[1] in DATE_TAGS:
                    start_index += 1
                    new_line = lines[start_index].strip()
                    date_ = self.__get_date(new_line)
                    indi_row[DATE_TAGS[segments[1]]] = date_
                elif segments[1] in FAM_TAGS:
                    indi_row[FAM_TAGS[segments[1]]] = indi_row.get(FAM_TAGS[segments[1]], {})
                    indi_row[FAM_TAGS[segments[1]]].update({segments[2]: None})
            elif line.startswith('0'):
                break
            else:
                raise ValueError("{} breaks the file format, check its validity.".format(line))
            start_index += 1
        # deal with derivative rows, age and alive
        if 'Birthday' not in indi_row:
            raise("Birthday is not found for the individual {id_}".format(id_=indi_row['id']))
        if 'Death' in indi_row:
            indi_row['Age'] = indi_row['Death'].year - indi_row['Birthday'].year
            indi_row['Alive'] = False
        else:
            indi_row['Age'] = date.today().year - indi_row['Birthday'].year
            indi_row['Alive'] = True
            indi_row['Death'] = None
        return indi_row, start_index

    def __generate_family_dict(self, lines, start_index, fam_row):
        while start_index < len(lines):
            line = lines[start_index].strip()
            if line.startswith('1'):
                segments = line.split()
                if segments[1] in RELATION_TAGS:
                    fam_row[RELATION_TAGS[segments[1]]] = segments[2]
                elif segments[1] in CHILD:
                    fam_row[CHILD[segments[1]]] = fam_row.get(CHILD[segments[1]], {})
                    fam_row[CHILD[segments[1]]].update({segments[2]: None})
                elif segments[1] in FAM_DATE_TAGS:
                    start_index += 1
                    new_line = lines[start_index].strip()
                    date_ = self.__get_date(new_line)
                    fam_row[FAM_DATE_TAGS[segments[1]]] = date_
            elif line.startswith('0'):
                break
            else:
                raise ValueError("{} breaks the file format, check its validity.".format(line))
            start_index += 1
        return fam_row, start_index

    @staticmethod
    def __get_date(line):
        segments = line.split()
        # check if this line's tag is DATE
        if segments[1] != 'DATE':
            raise ValueError("This line does not include the tag of DATE.")
        try:
            day, month, year = int(segments[2]), MONTHS[segments[3]], int(segments[4])
        except Exception as e:
            print("marriage date format is invalid.")
            raise e
        return date(year, month, day)

    def __connect(self):
        for key in self.__individual_dict:
            indi = self.__individual_dict[key]
            for fam_child_key in indi.list_parents_families_ids():
                fam = self.__family_dict[fam_child_key]
                indi.set_parent_family_by_id(fam_child_key, fam)
            for fam_spouse_key in indi.list_own_families_ids():
                fam = self.__family_dict[fam_spouse_key]
                indi.set_own_family_by_id(fam_spouse_key, fam)
        for key in self.__family_dict:
            fam = self.__family_dict[key]
            for child_key in fam.list_children_ids():
                child = self.__individual_dict[child_key]
                fam.set_child_by_id(child_key, child)

    def __update_derivative_attributes(self):
        for key in self.__family_dict:
            fam = self.__family_dict[key]
            try:
                wife = self.__individual_dict[fam.get_wife_id()]
                fam.set_wife_name(wife.get_name())
            except KeyError:
                print("wife of family {fam_id} is not found.".format(fam_id=key))
            try:
                husband = self.__individual_dict[fam.get_husband_id()]
                fam.set_husband_name(husband.get_name())
            except KeyError:
                print("Husband of family {fam_id} is not found.".format(fam_id=key))

    def __add_an_individual(self, indi):
        self.__individual_dict[indi.get_id()] = indi

    def __add_a_family(self, fam):
        self.__family_dict[fam.get_id()] = fam

    def print_families(self):
        family_table = prettytable.PrettyTable()
        family_table.field_names = ["ID",
                                    "Married",
                                    "Divorced",
                                    "Husband_ID",
                                    "Husband Name",
                                    "Wife Id",
                                    "Wife Name",
                                    "Children"]
        for key in self.__family_dict:
            fam = self.__family_dict[key]
            family_row = fam.get_family()
            family_row = ["NA" if x is None else x for x in family_row]
            family_table.add_row(family_row)
        print(family_table)

    def print_individuals(self):
        individual_table = prettytable.PrettyTable()
        individual_table.field_names = ['ID',
                                        'Name',
                                        'Gender',
                                        'Birthday',
                                        'Age',
                                        'Alive',
                                        'Death',
                                        'Spouse',
                                        'Child']
        for key in self.__individual_dict:
            individual = self.__individual_dict[key]
            individual_row = individual.get_individual()
            individual_row = ["NA" if x is None else x for x in individual_row]
            individual_table.add_row(individual_row)
        print(individual_table)

    def get_families(self):
        return self.__family_dict

    def get_individuals(self):
        return self.__individual_dict

    def get_individual_by_id(self, id_):
        return self.__individual_dict[id_]

    # Sprint 1
    # US04 Marriage before Divorce
    def check_marriage_before_divorce(self):
        results = {}
        for family in families(self):
            result = self.__compare_marriage_divorce(family)
            results[id_(family)] = result
        return results

    @staticmethod
    def __compare_marriage_divorce(family):
        if marriage_date(family) and divorce_date(family):
            if marriage_date(family) > divorce_date(family):
                print("SPRINT 1 ERROR in US04: Family {id_}'s marriage Date({m_t}) is later than the divorce date ({d_t}).".format(
                    id_=family.get_id(), m_t=marriage_date(family), d_t=divorce_date(family)))
                return False
        elif marriage_date(family) is None:
            if divorce_date(family):
                print("SPRINT 1 ERROR in US04: Family {id_} has divorce date ({d_t}) but no marriage date.".format(
                    id_=id_(family), d_t=divorce_date(family)))
                return False
            else:
                print("SPRINT 1 ERROR in US04: Family {id_} does not have marriage date".format(id_=id_(family)))
                return False
        return True

    # US06 Divorce before death
    def check_divorce_before_death(self):
        individuals = self.get_individuals()
        checked_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            death_date = individual.get_death()
            indi_id = individual.get_id()
            own_families = individual.get_own_families()
            if death_date is None or len(own_families) == 0:
                checked_results[indi_id] = "NA"
                continue
            for fam_key in own_families:
                own_family = own_families[fam_key]
                fam_id = own_family.get_id()
                divorce_date = own_family.get_divorce_date()
                result = self.__compare_divorce_death(divorce_date, death_date, indi_id, fam_id, checked_results)
                checked_results[indi_id] = result
        return checked_results

    @staticmethod
    def __compare_divorce_death(divorce_date, death_date, indi_id, fam_id, checked_results):
        if divorce_date:
            if divorce_date > death_date:
                print("SPRINT 1 ERROR US06: Individual {i_id} of Family {f_id} has a divorce date {div_d} after the date of death {d_d}.".format(
                    i_id=indi_id,
                    f_id = fam_id,
                    div_d=divorce_date.strftime("%Y-%m-%d"),
                    d_d=death_date.strftime("%Y-%m-%d")))
                return "No"
            else:
                return "Yes"
        else:
            if indi_id in checked_results:
                return checked_results[indi_id]
            return "Yes"

    # US05 Marriage before Death
    def check_marriage_before_death(self):
        individuals = self.get_individuals()
        checked_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            death_date = individual.get_death()
            indi_id = individual.get_id()
            own_families = individual.get_own_families()
            if death_date is None or len(own_families) == 0:
                checked_results[indi_id] = "NA"
                continue
            for fam_key in own_families:
                own_family = own_families[fam_key]
                marriage_date = own_family.get_marriage_date()
                result = self.__compare_marriage_death(marriage_date, death_date, indi_id)
                checked_results[indi_id] = result
        return checked_results

    @staticmethod
    def __compare_marriage_death(marriage_date, death_date, indi_id):
        if marriage_date:
            if marriage_date > death_date:
                print("SPRINT 1 ERROR US05: Individual {i_id} has a marriage date {div_d} after the date of death {d_d}.".format(
                    i_id=indi_id,
                    div_d=marriage_date.strftime("%Y-%m-%d"),
                    d_d=death_date.strftime("%Y-%m-%d")))
                return "No"
            else:
                return "Yes"
        else:
            return "Yes"

    # US10 Marriage after age fourteen
    def check_marriage_after_fourteen(self):
        individuals = self.get_individuals()
        checked_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            birth_date = individual.get_birth()
            indi_id = individual.get_id()
            own_families = individual.get_own_families()
            for fam_key in own_families:
                own_family = own_families[fam_key]
                marriage_date = own_family.get_marriage_date()
                result = self.__compare_marriage_age(marriage_date, birth_date, indi_id)
                checked_results[indi_id] = result
        return checked_results

    @staticmethod
    def __compare_marriage_age(marriage_date, birth_date, indi_id):
        if marriage_date:
            diff = abs(marriage_date.year - birth_date.year)
            if diff < 14:
                print("SPRINT 1 ERROR US10: Individual {i_id} has a marriage date {div_d} before the age of fourteen.".format(
                    i_id=indi_id,
                    div_d=marriage_date.strftime("%Y-%m-%d")))
                return "No"
            else:
                return "Yes"
        else:
            return "Yes"

    # US 03 Individual birth after death
    def check_birth_before_death(self):
        individuals = self.get_individuals()
        check_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            birth_date = individual.get_birth()
            death_date = individual.get_death()
            indi_id = individual.get_id()
            if death_date is not None and birth_date is not None:
                if birth_date > death_date:
                    check_results[indi_id] = "error"
                    print("SPRINT 1 ERROR in US03: Individual {i_id} has birth date after death date".format(i_id=indi_id))
                else:
                    check_results[indi_id] = "N/A"
            else:
                check_results[indi_id] = "N/A"
        return check_results

    # US 08 Child birth before Parents Marriage
    def check_childbirth_before_parents_marriage(self):
        families = self.get_families()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            fam_marriage_date = family.get_marriage_date()
            fam_children = family.list_children_ids()
            for key in fam_children:
                child = self.get_individual_by_id(key)
                child_birthday = child.get_birth()
                if fam_marriage_date is not None and child_birthday is not None:
                    if fam_marriage_date < child_birthday:
                        check_results[fam_id + "-" + child.get_id()] = "no"
                    else:
                        check_results[fam_id + "-" + child.get_id()] = "yes"
                        print("SPRINT 1 ERROR in US08: Found a child {c_id}'s birthday {c_birth} before the marriage date {m_d} of {c_id}'s parent family {f_id}.".format(
                            c_id=child.get_id(), m_d=fam_marriage_date, c_birth=child_birthday, f_id=fam_id))
        return check_results

    #US 02 Birth before Marriage
    def check_birth_before_marriage(self):
        individuals = self.get_individuals()
        checked_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            birth_date = individual.get_birth()
            indi_id = individual.get_id()
            own_families = individual.get_own_families()
            for fam_key in own_families:
                own_family = own_families[fam_key]
                marriage_date = own_family.get_marriage_date()
                result = self.__compare_marriage_birth(marriage_date, birth_date, indi_id)
                checked_results[indi_id] = result
        return checked_results

    @staticmethod
    def __compare_marriage_birth(marriage_date, birth_date, indi_id):
        if marriage_date:
            if marriage_date < birth_date:
                print("SPRINT 1 ERROR in US02: Individual {i_id} has a marriage date {div_d} before the individual is born.".format(
                    i_id=indi_id,
                    div_d=marriage_date.strftime("%Y-%m-%d")))
                return "No"
            else:
                return "Yes"
        else:
            return "N/A"

    #US 07 Less than 150 years old
    def check_age_lessthan_150(self):
        individuals = self.get_individuals()
        check_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            birth_date = individual.get_birth()
            death_date = individual.get_death()
            indi_id = individual.get_id()
            present_date = date.today()
            limit = timedelta(days=150*365)
            if death_date:
                if death_date - birth_date >= limit:
                    check_results[indi_id] = "Error"
                    print("SPRINT 1 ERROR in US07: Individual {i_id} age is more than 150 which is not possible".format(i_id=indi_id))
                else:
                    check_results[indi_id] = "Yes"
            else:
                if present_date - birth_date >= limit:
                    check_results[indi_id] = "Error"
                    print("SPRINT 1 ERROR in US07: Individual {i_id} age is more than 150 which is not possible".format(i_id=indi_id))
                else:
                    check_results[indi_id] = "Yes"
        return check_results

    # Sprint 2
    # US16 Male last names
    def check_male_last_names(self):
        families = self.get_families()
        checked_results = {}
        for fam_key in families:
            family = families[fam_key]
            fam_id = family.get_id()
            husband = self.__individual_dict[family.get_husband_id()]
            last_name = husband.get_name().split(" ")[1].strip()
            wife = self.__individual_dict[family.get_wife_id()]
            wife_last_name = wife.get_name().split(" ")[1].strip()
            if wife_last_name != last_name:
                print("SPRINT 2 ERROR in US16: Individual {i_id}'s last name {i_ln} does not match family {f_id}'s name {f_n}.".format(
                    i_id=wife.get_id(),i_ln=wife_last_name,f_id=fam_id,f_n=last_name))
                checked_results[fam_id] = "No"
            children = family.get_children()
            for _, child in children.items():
                child_last_name = child.get_name().split(" ")[1].strip()
                if child_last_name != last_name:
                    print("SPRINT 2 ERROR in US16: Individual {i_id}'s last name {i_ln} does not match family {f_id}'s name {f_n}.".format(
                                    i_id=child.get_id(),
                                    i_ln=child_last_name,
                                    f_id=fam_id,
                                    f_n=last_name))
                    checked_results[fam_id] = "No"
            if fam_id not in checked_results:
                checked_results[fam_id] = "Yes"
        return checked_results

    # US17 No marriages to descendants
    def check_marry_descendants(self):
        results = {}
        for individual in individuals(self):
            # get all descendants ids
            children_ids = set(individual.find_all_descendants())
            spouse_ids = individual.find_spouse_ids()
            spouse_is_a_descendant = False
            for spouse_id in spouse_ids:
                if spouse_id in children_ids:
                    print("SPRINT 2 ERROR in US17: Individual {i_id} married descendant {s_id}.".format(i_id=id_(individual), s_id=spouse_id))
                    results[id_(individual)] = "Error"
                    spouse_is_a_descendant = True
            if not spouse_is_a_descendant:
                results[id_(individual)] = "Correct"
        return results

    # US 09 Check for old parents
    def check_old_parents(self):
        families = self.get_families()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            husband_id = family.get_husband_id()
            wife_id = family.get_wife_id()

            husb = self.get_individual_by_id(husband_id)
            wife = self.get_individual_by_id(wife_id)

            husb_birth = husb.get_birth()
            wife_birth = wife.get_birth()

            if(husb_birth and wife_birth):
                if(date.today().year - husb_birth.year > 100 or date.today().year - wife_birth.year > 100):
                    check_results[fam_id] = "yes"
                    print("SPRINT 2 ERROR in US12: The husband or the wife or both in family {f} are too old".format(f=fam_id))
                else:
                    check_results[fam_id] = "no"
            else:
                check_results[fam_id] = "no"
                print("SPRINT 2 ERROR in US12: The birth date of husband or wife is missing!")
        return check_results

    # US 12 Check birth before death of parents
    def check_birth_before_death_of_parents(self):
        families = self.get_families()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            husband_id = family.get_husband_id()
            wife_id = family.get_wife_id()

            husb = self.get_individual_by_id(husband_id)
            wife = self.get_individual_by_id(wife_id)

            husb_birth = husb.get_birth()
            husb_death = husb.get_death()
            wife_birth = wife.get_birth()
            wife_death = wife.get_death()

            if(husb_death is not None):
                if(husb_birth.year < husb_death.year):
                    #print("1. ",husb_birth,"\t\t",husb_death)
                    check_results[fam_id] = "yes"
                else:
                    #print("2. ",husb_birth,"\t\t",husb_death)
                    check_results[fam_id] = "no"
                    print("SPRINT 2 ERROR in US09: In family {f_id}, the Father with {h_id} has a death date before birth".format(f_id=fam_id,h_id=husband_id))
            elif(wife_death is not None):
                if(wife_birth.year < wife_death.year):
                    #print("1. ",husb_birth,"\t\t",husb_death)
                    check_results[fam_id] = "yes"
                else:
                    #print("2. ",husb_birth,"\t\t",husb_death)
                    check_results[fam_id] = "no"
                    print("SPRINT 2 ERROR in US09: In family {f_id}, the Mother with {w_id} has a death date before birth".format(f_id=fam_id,w_id=wife_id))
            else:
                #print("3. ",husb_birth,"\t\t",husb_death)
                check_results[fam_id] = "yes"
        return check_results

    # US 14: Multiple births <= 5
    def check_multiple_births(self):
        checked_results = {}
        for family in families(self):
            if len(children(family)) <= 0:
                checked_results[id_(family)] = "Yes"
                continue
            same_birth_dict = {}
            for child in children(family):
                same_birth_dict[child.get_birth()] = same_birth_dict.get(child.get_birth(), 0) + 1
                if same_birth_dict[child.get_birth()] == 5:
                    print("SPRINT 2 ERROR in US14: Found multiple births at the same time greater than five in family {f}".format(f=id_(family)))
                    checked_results[id_(family)] = "No"
            if id_(family) not in checked_results:
                checked_results[id_(family)] = "Yes"
        return checked_results

    # US 15: Fewer than 15 siblings
    def check_siblings_count(self):
        families = self.get_families()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            fam_children = family.list_children_ids()

            if len(fam_children) >= 15:
                check_results[fam_id] = "No"
                print("SPRINT 2 ERROR in US15: More than 15 siblings in in family {f}".format(f=fam_id))
            else:
                check_results[fam_id] = "Yes"

        return check_results

    # US21 Correct gender for role
    def check_Correct_gender(self): 
        families = self.get_families()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            husband_id = family.get_husband_id()
            wife_id = family.get_wife_id()

            husb = self.get_individual_by_id(husband_id)
            wife = self.get_individual_by_id(wife_id)

            husb_gender = husb.get_gender()
            wife_gender = wife.get_gender()

            if(husb_gender != 'M'):
                check_results[husband_id] = "Error"
                print("SPRINT 2 ERROR in US21: The husband {h} in the family {f} violates correct gender".format(h=husband_id, f=fam_id))
            else:
                check_results[husband_id] = "Yes"

            if(wife_gender != 'F'):
                check_results[wife_id] = "Error"
                print("SPRINT 2 ERROR in US21: The Wife {w} in the family {f} violates correct gender".format(w=wife_id, f=fam_id))
            else:
                check_results[wife_id] = "Yes"

        return check_results

    #Siblings Spacing US 13
    def check_sibling_spacing(self):
        families = self.get_families()
        #individuals = self.get_individuals()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            fam_children = family.list_children_ids()
            #print("list of children", fam_children)
            children_birth = []
            if len(list(fam_children)) < 2:
                #print("US 13: There are no childs or one child in family {f}".format(f=fam_id))
                check_results[fam_id] = "N/A"
            else:
                for key in fam_children:
                    child = self.get_individual_by_id(key)
                    children_birth.append(child.get_birth())
                    children_birth = sorted(children_birth, reverse=False)
                    for x, y in zip(children_birth[::],children_birth[1::]):
                        #print ("for loop", x, y, fam_id)
                        diff = y - x
                        if (diff > timedelta(days=2) and diff < timedelta(days=243)):
                            print("SPRINT 2 ERROR in US 13: Difference in sibling age is not possible in family {f}".format(f=fam_id))
                            check_results[fam_id] = "Error"
                        else:
                            check_results[fam_id] = "Yes"
        #print(check_results)
        return check_results

    # Sprint 3

    # US 28 Order siblings by age
    def order_siblings_by_age(self):
        families = self.get_families()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            fam_children = family.list_children_ids()
            children_birth = []
            if len(list(fam_children)) < 2:
                print("SPRINT 3 ERROR in US 28: There are not enough children to sort in family {f}".format(f=fam_id))
                check_results[fam_id] = "No" # indicates that there is only 1 child
            else:
                check_results[fam_id] = "Yes"
                for key in fam_children:
                    child = self.get_individual_by_id(key)
                    children_birth.append(child.get_birth().year)
                    children_birth = sorted(children_birth, reverse=True)
        #print(children_birth)
        return check_results

    # US 34 large age difference between couple when married
    def large_age_difference(self):
        families = self.get_families()
        check_results = {}
        large_age_difference = []
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            fam_marriage_date = family.get_marriage_date()

            if fam_marriage_date is not None:
                fam_marriage_date = fam_marriage_date.year
                subtract = date.today().year - fam_marriage_date # to find the #of years to be subtracted to get the age when married

                husband_id = family.get_husband_id()
                wife_id = family.get_wife_id()

                husb = self.get_individual_by_id(husband_id)
                wife = self.get_individual_by_id(wife_id)

                husb_age = date.today().year - husb.get_birth().year
                husb_age_when_married = husb_age - subtract

                wife_age = date.today().year - wife.get_birth().year
                wife_age_when_married = wife_age - subtract

                if(husb_age_when_married >= wife_age_when_married*2 or wife_age_when_married >= husb_age_when_married*2):
                    check_results[fam_id] = 'Yes'
                    large_age_difference.append(fam_id)
                    print("SPRINT 3 ERROR in US 34: Either the Husband or the wife in family {f} had an age twice or more than the other".format(f=fam_id))
                else:
                    check_results[fam_id] = 'No'
            else:
                check_results[fam_id] = 'No'
        #print(large_age_difference)
        return check_results

    #US35 List recent births
    def check_recent_births(self):
        individuals = self.get_individuals()
        check_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            birth_date = individual.get_birth()
            #print("birth", birth_date)
            indi_id = individual.get_id()
            present_date = date.today()
            limit = timedelta(days=30)
            #print(present_date - birth_date, indi_id)
            if birth_date > present_date:
                print("SPRINT 3 ERROR in US35: The person {i} birth date is invalid".format(i=indi_id))
                check_results[indi_id] = "Error"
            elif present_date - birth_date <= limit:
                check_results[indi_id] = "Yes"
            else:
                check_results[indi_id] = "No"
        #print(check_results)
        return check_results

    #US36 List recent deaths
    def check_recent_deaths(self):
        individuals = self.get_individuals()
        check_results = {}
        for indi_key in individuals:
            individual = individuals[indi_key]
            death_date = individual.get_death()
            #print("birth", birth_date)
            indi_id = individual.get_id()
            present_date = date.today()
            limit = timedelta(days=30)
            #print(present_date - birth_date, indi_id)
            if death_date:
                if death_date > present_date:
                    print("SPRINT 3 ERROR in US36: The person {i} death date is invalid".format(i=indi_id))
                    check_results[indi_id] = "Error"
                elif present_date - death_date <= limit:
                    check_results[indi_id] = "Yes"
                else:
                    check_results[indi_id] = "No"
            else:
                check_results[indi_id] = "N/A"
                #print("Error in US36: The person {i} is still alive".format(i=indi_id))
        #print(check_results)
        return check_results

    # US 18 Siblings should not marry
    def check_no_one_marries_sibling(self):
        results = {}
        for individual in individuals(self):
            # get all descendants ids
            siblings_ids = set(individual.find_all_siblings())
            spouses_ids = individual.find_spouse_ids()
            spouse_is_a_sibling = False
            for spouse_id in spouses_ids:
                if spouse_id in siblings_ids:
                    print("SPRINT 3 ERROR in US 18: Individual {i_id} married sibling {s_id}.".format(i_id=id_(individual), s_id=spouse_id))
                    results[id_(individual)] = "Error"
                    spouse_is_a_sibling = True
            if not spouse_is_a_sibling:
                results[id_(individual)] = "Correct"
        return results

    # US 19 First cousins should not marry
    def check_no_one_marries_first_cousin(self):
        results = {}
        for individual in individuals(self):
            if not has_own_family(individual):
                continue
            spouses_ids = individual.find_spouse_ids()
            spouse_is_a_cousin = False
            #print("parents", individual.get_id(), spouses_ids, parents(individual))
            for parent_id in parents(individual):
                parent = self.get_individual_by_id(parent_id)
                #print("parent siblings",individual.get_id(), spouses_ids, parent.find_all_siblings())
                for sibling_id in parent.find_all_siblings():
                    sibling = self.get_individual_by_id(sibling_id)
                    if not has_own_family(sibling):
                        continue
                    cousins_ids = set(sibling.find_all_children())
                    #print("first cousins",individual.get_id(), spouses_ids, cousins_ids)
                    for spouse_id in spouses_ids:
                        if spouse_id in cousins_ids:
                            print("SPRINT 3 ERROR in US 19: Individual {i_id} married cousin {s_id}.".format(i_id=id_(individual), s_id=spouse_id))
                            results[id_(individual)] = "Error"
                            spouse_is_a_cousin = True
                            break
            if not spouse_is_a_cousin:
                results[id_(individual)] = "Correct"
        #print(results)
        return results

        # US31: List living single
    def check_list_single(self):
        individuals = self.get_individuals()
        check_results = {}
        married_list = []
        unmarried_list = []
        for key in individuals:
            individual = individuals[key]
            indi_id = individual.get_id()
            if date.today().year - individual.get_birth().year > 30:
                if not individual.find_spouse_ids():
                    check_results[indi_id] = "Yes"
                    unmarried_list.append(indi_id)
            else:
                married_list.append(indi_id)
                check_results[indi_id] = "No"
        #print("US31: List of individuals that are single:")
        #print(*unmarried_list, sep=", ")
        print("SPRINT 3 ERROR in US31: List of individuals that are NOT single:")
        print("        ", ", ".join(married_list))
        #print(*married_list, sep=", ")
        return check_results

    # US30: List living married
    def check_list_married(self):
        check_results = {}
        married_list = []
        unmarried_list = []
        for individual in individuals(self):
            indi_id = individual.get_id()
            if date.today().year - individual.get_birth().year > 30:
                if individual.find_spouse_ids():
                    check_results[indi_id] = "Yes"
                    married_list.append(indi_id)
                else:
                    unmarried_list.append(indi_id)
                    check_results[indi_id] = "No"
            else:
                unmarried_list.append(indi_id)
                check_results[indi_id] = "No"

        #print("US30: List of individuals that are married:")
        #print(*married_list, sep=", ")

        print("SPRINT 3 ERROR in US30: List of individuals that are NOT married:")
        print("        ", ", ".join(unmarried_list))
        #print(*unmarried_list, sep=", ")
        return check_results

    #Sprint 4   
    # US 33
    def check_orphans(self):
        families = self.get_families()
        check_results = {}
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            
            husband_id = family.get_husband_id()
            wife_id = family.get_wife_id()
            
            husb = self.get_individual_by_id(husband_id)
            wife = self.get_individual_by_id(wife_id)
            fam_children = family.list_children_ids()
            
            husb_death = husb.get_death()
            wife_death = wife.get_death()
            
            for key in fam_children:
                child = self.get_individual_by_id(key)
                child_birthday = child.get_birth().strftime('%Y-%m-%d')
                childBirth = datetime.datetime.strptime(child_birthday,"%Y-%m-%d")
                child_deathday = child.get_death()
                present_date = date.today().strftime('%Y-%m-%d')
                if len(fam_children) == 0:
                    check_results[key] = "N/A"
                else:
                    if husb_death and wife_death:
                        if child_deathday:
                            check_results[key] = "Error"
                            print("SPRINT 4 ERROR in US33: The child {c} is not alive".format(c=key))
                        else:    
                            today = datetime.datetime.strptime(present_date,"%Y-%m-%d")
                            age = today.year - childBirth.year
                            if(age < 18):
                                check_results[key] = "Yes"
                            else:
                                check_results[key] = "No"
                    else: 
                        check_results[key] = "N/A"
        return check_results
    
    # US 27 Include individual ages
    def include_ages(self):
        check_results = {}
        individuals = self.get_individuals()
        for indi_key in individuals:
            individual = individuals[indi_key]
            indi_id = individual.get_id()
            birth_date = individual.get_birth().strftime('%Y-%m-%d')
            birth = datetime.datetime.strptime(birth_date,"%Y-%m-%d")
            death_date = individual.get_death()
            present_date = date.today().strftime('%Y-%m-%d')
            if death_date:
                death_date = individual.get_death().strftime('%Y-%m-%d')
                death = datetime.datetime.strptime(death_date,"%Y-%m-%d")
                age = death.year - birth.year
                if age < 0:
                    print("SPRINT 4 ERROR in US27: User {i_id} has invalid age".format(i_id=indi_id))                    
                    check_results[indi_id] = "Error"
                else:
                    check_results[indi_id] = age
            else:
                today = datetime.datetime.strptime(present_date,"%Y-%m-%d")
                age = today.year - birth.year 
                if age < 0:
                    print("SPRINT 4 ERROR in US27: User {i_id} has invalid age".format(i_id=indi_id))                    
                    check_results[indi_id] = "Error"
                else:
                    check_results[indi_id] = age
        return check_results
    
    # US38 Upcoming birthdays
    def upcoming_birthdays(self):
        individuals = self.get_individuals()
        check_results = {}
        upcoming_list = []
        for indi_key in individuals:
            individual = individuals[indi_key]
            indi_id = individual.get_id()
            birth_date = individual.get_birth()
            birth_date = str(birth_date).split('-')[1:]
            start_date = date.today() + datetime.timedelta(+30)
            start_date = str(start_date).split('-')[1:]

            if int(start_date[0]) - int(birth_date[0]) == 1 and \
                        int(start_date[1]) <= int(birth_date[1]):
                upcoming_list.append(indi_id)
                # print(int(start_date[0]), int(birth_date[0]))
                check_results[indi_id] = "Yes"
                print("SPRINT 4 ATTENTION in US38: Individual {i} will have birthday in the next 30 days".format(i=indi_id))
            elif int(start_date[0]) - int(birth_date[0]) == 0 and \
                        int(start_date[1]) >= int(birth_date[1]):
                upcoming_list.append(indi_id)
                # print(int(start_date[0]), int(birth_date[0]))
                check_results[indi_id] = "Yes"
                print("SPRINT 4 ATTENTION in US38: Individual {i} will have birthday in the next 30 days".format(i=indi_id))
            else:
                # print(False)
                check_results[indi_id] = "No"
        #print(upcoming_list)
        return check_results

    # US 39 Upcoming Marriage_anniversaries
    def upcoming_anniversaries(self):
        families = self.get_families()
        check_results = {}
        upcoming_list = []
        for key in families:
            family = families[key]
            fam_id = family.get_id()
            fam_marriage_date = family.get_marriage_date()
            fam_marriage_date = str(fam_marriage_date).split('-')[1:]
            # print(fam_marriage_date)
            start_date = date.today() + datetime.timedelta(+30)
            start_date = str(start_date).split('-')[1:]
            # print(start_date)
            if fam_marriage_date:
                if int(start_date[0]) - int(fam_marriage_date[0]) == 1 and \
                            int(start_date[1]) <= int(fam_marriage_date[1]):
                    upcoming_list.append(fam_id)
                    # print(int(start_date[0]), int(fam_marriage_date[0]))
                    check_results[fam_id] = "Yes"
                    print("SPRINT 4 ATTENTION in US39: Family {f} will have their anniversary in the next 30 days".format(f=fam_id))
                elif int(start_date[0]) - int(fam_marriage_date[0]) == 0 and \
                            int(start_date[1]) >= int(fam_marriage_date[1]):
                    upcoming_list.append(fam_id)
                    # print(int(start_date[0]), int(fam_marriage_date[0]))
                    check_results[fam_id] = "Yes"
                    print("SPRINT 4 ATTENTION in US39: Family {f} will have their anniversary in the next 30 days".format(f=fam_id))
                else:
                    # print(False)
                    check_results[fam_id] = "No"
            else:
                # print(False)
                check_results[fam_id] = "No"
        #print(upcoming_list)
        return check_results

    # US 24 Unique families by spouses
    def check_unique_family(self):
        family_dict = {}
        results = {}
        for family in families(self):
            husband_name = self.__individual_dict[husband(family)].get_name()
            #print(husband_name, "Name test")
            wife_name = self.__individual_dict[wife(family)].get_name()
            family_key = '-'.join([husband_name, wife_name])
            if family_key in family_dict:
                if family_dict[family_key][0] == marriage_date(family):
                    print('SPRINT 4 ERROR in US24: Family {f_id1} has the same marriage date and spouse names with Family {f_id2}.'.format(f_id1=id_(family),f_id2=family_dict[family_key][1]))
                    results[id_(family)] = 'Error'
                    continue
            family_dict[family_key] = [marriage_date(family), id_(family)]
            results[id_(family)] = 'OK'
        return results

    # US 25 Unique first names in families
    def check_unique_first_name_in_family(self):
        results = {}
        for family in families(self):
            first_names = set()
            husband_first_name = family.get_husband_name().split(' ')[0]
            wife_first_name = family.get_wife_name().split(' ')[0]
            children_first_names = [name.split(' ')[0] for name in family.list_children_names()]
            for first_name in [husband_first_name, wife_first_name] + children_first_names:
                if first_name not in first_names:
                    first_names.add(first_name)
                else:
                    print('SPRINT 4 ERROR IN US25: First name {name} is given to more than two members in family {f_id}.'.format(name=first_name, f_id=id_(family)))
                    results[id_(family)] = 'Error'
            if id_(family) not in results:
                results[id_(family)] = 'OK'
        return results

    # US 01 : Dates before current date
    def check_current_dates(self):
        individuals = self.get_individuals()
        check_results = {}
        for i in individuals:
            individual = individuals[i]
            indi_id = individual.get_id()
            birth_date = individual.get_birth()
            death_date = individual.get_death()
            if birth_date > date.today():
                print("SPRINT 4 ERROR in US01: Individual {i_id} has birth date {b_date} after the current date!".
                      format(i_id=indi_id, b_date=birth_date))
                check_results[indi_id] = "No"
            check_results[indi_id] = "Yes"

            if death_date:
                if death_date > date.today():
                    print("SPRINT 4 ERROR in US01: Individual {i_id} has death date {d_date} after the current date!".
                          format(i_id=indi_id, d_date=death_date))
                    check_results[indi_id] = "No"
                check_results[indi_id] = "Yes"

        families = self.get_families()
        for f in families:
            family = families[f]
            fam_id = family.get_id()
            marriage_date = family.get_marriage_date()
            divorce_date = family.get_divorce_date()

            if marriage_date:
                if marriage_date > date.today():
                    print("SPRINT 4 ERROR in US01: Family {f_id} has marriage date {m_date} after the current date!".
                          format(f_id=fam_id, m_date=marriage_date))
                    check_results[fam_id] = "No"
                check_results[fam_id] = "Yes"

            if divorce_date:
                if divorce_date > date.today():
                    print("SPRINT 4 ERROR in US01: Family {f_id} has divorce date {d_date} after the current date!".
                          format(f_id=fam_id, d_date=divorce_date))
                    check_results[fam_id] = "No"
                check_results[fam_id] = "Yes"

        return check_results

    # US 29: List deceased
    def check_list_deaths(self):
        check_results = {}
        deceased_list = []
        for individual in individuals(self):
            indi_id = individual.get_id()
            if individual.get_death():
                check_results[indi_id] = "Yes"
                deceased_list.append(indi_id)
            else:
                check_results[indi_id] = "No"

        print("SPRINT 4 ERROR in US29: List of individuals that are deceased:")
        print("        ", ", ".join(deceased_list))
        #print(*deceased_list, sep=", ")
        return check_results

# Families
class Family:
    def __init__(self):
        self.__id = None
        self.__husband_id = None
        self.__husband_name = None
        self.__wife_id = None
        self.__wife_name = None
        self.__children = {}
        self.__married = None
        self.__divorced = None

    def read_in(self, fam_dict):
        if 'id' in fam_dict:
            self.__id = fam_dict['id']
        if 'Married' in fam_dict:
            self.__married = fam_dict['Married']
        if 'Divorced' in fam_dict:
            self.__divorced = fam_dict['Divorced']
        if 'Husband_ID' in fam_dict:
            self.__husband_id = fam_dict['Husband_ID']
        if 'Wife_ID' in fam_dict:
            self.__wife_id = fam_dict['Wife_ID']
        if 'Children' in fam_dict:
            self.__children = fam_dict['Children']

    def get_family(self):
        return [self.__id, self.__married,
                self.__divorced, self.__husband_id,
                self.__husband_name, self.__wife_id,
                self.__wife_name, set([key for key in self.__children])]

    def get_id(self):
        return self.__id

    def get_husband_id(self):
        return self.__husband_id

    def set_husband_name(self, name):
        self.__husband_name = name

    def get_husband_name(self):
        return self.__husband_name

    def get_wife_id(self):
        return self.__wife_id

    def set_wife_name(self, name):
        self.__wife_name = name

    def get_wife_name(self):
        return self.__wife_name

    def list_children_names(self):
        return [indi.get_name() for indi in self.__children.values()]

    def list_children_ids(self):
        return set([key for key in self.__children])

    def set_child_by_id(self, child_key, child):
        self.__children[child_key] = child

    def get_child_by_id(self, id_):
        return self.__children[id_]

    def get_children(self):
        return self.__children

    def get_marriage_date(self):
        return self.__married

    def get_divorce_date(self):
        return self.__divorced


# Individual
class Individual:
    def __init__(self):
        self.__id = None
        self.__name = None
        self.__gender = None
        self.__birth = None
        self.__death = None
        self.__age = None
        self.__alive = None
        self.__parents_families = {}  # families where the indi is a child
        self.__own_families = {}  # families where the indi is a spouse

    def read_in(self, indi_dict):
        if 'id' in indi_dict:
            self.__id = indi_dict['id']
        if 'Name' in indi_dict:
            self.__name = indi_dict['Name']
        if 'Gender' in indi_dict:
            self.__gender = indi_dict['Gender']
        if 'Birthday' in indi_dict:
            self.__birth = indi_dict['Birthday']
        if 'Age' in indi_dict:
            self.__age = indi_dict['Age']
        if 'Alive' in indi_dict:
            self.__alive = indi_dict['Alive']
        if 'Death' in indi_dict:
            self.__death = indi_dict['Death']
        if 'Child' in indi_dict:
            self.__parents_families = indi_dict['Child']
        if 'Spouse' in indi_dict:
            self.__own_families = indi_dict['Spouse']

    def get_individual(self):
        # list all information of the indi
        return [self.__id, self.__name, self.__gender,
                self.__birth, self.__age, self.__alive, self.__death,
                set([key for key in self.__own_families]),
                set([key for key in self.__parents_families])
                ]

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

    def get_gender(self):
        return self.__gender

    def get_birth(self):
        return self.__birth

    def get_death(self):
        return self.__death

    def list_parents_families_ids(self):
        return set([key for key in self.__parents_families])

    def list_own_families_ids(self):
        return set([key for key in self.__own_families])

    def get_parent_family_by_id(self, id_):
        return self.__parents_families[id_]

    def get_parent_families(self):
        return self.__parents_families

    def get_own_family_by_id(self, id_):
        return self.__own_families[id_]

    def get_own_families(self):
        return self.__own_families

    def set_parent_family_by_id(self, fam_id, fam):
        self.__parents_families[fam_id] = fam

    def set_own_family_by_id(self, fam_id, fam):
        self.__own_families[fam_id] = fam

    def find_all_descendants(self):
        results = []
        #dfs to fetch all descendant ids
        def helper(individual, results):
            if len(list(individual.get_own_families().values())) == 0:
                return
            for family in list(individual.get_own_families().values()):
                children = family.get_children()
                results += list(children.keys())
                for child in list(children.values()):
                    helper(child, results)

        helper(self, results)
        return results

    def find_spouse_ids(self):
        own_families = list(self.get_own_families().values())
        if self.get_gender() == "M":
            results = [fam.get_wife_id() for fam in own_families]
        else:
            results = [fam.get_husband_id() for fam in own_families]
        return results
    
    def find_all_siblings(self):
        siblings = []
        for _, parent_family in self.get_parent_families().items():
            for _, child in parent_family.get_children().items():
                if child.get_id() != self.get_id():
                    siblings.append(child.get_id())
        return siblings
    
    def find_all_children(self):
        children_ids = set()
        for _, family in self.__own_families.items():
            for child_id in family.get_children():
                children_ids.add(child_id)
        return list(children_ids)