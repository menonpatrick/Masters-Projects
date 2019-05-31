# unit testing gedcom parser
import unittest
from Gedcom import Gedcom
import json

class TestGedcomParser(unittest.TestCase):
    
    def _check_ground_truth(self, checked_results, ground_truth_file_path):
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            if ground_truths[key] != checked_results[key]:
                print(key, ground_truths[key], checked_results)
            self.assertTrue(key in checked_results)
            self.assertEqual(ground_truths[key], checked_results[key])

    # US04 marriage before divorce
    def test_s1us04_marriage_before_divorce(self,
                                     file_path='test_files/Family.ged',
                                     ground_truth_file_path='test_files/gf.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_marriage_before_divorce()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in checked_results)
            self.assertEqual(ground_truths[key], str(checked_results[key]))
        #print("check_marriage_before_divorce test on {f} passed.".format(f=file_path))

    # US06 divorce before death
    def test_s1us06_divorce_before_death(self, 
                    file_path='test_files/Family.ged', 
                    ground_truth_file_path='test_files/divorce_before_death.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_divorce_before_death()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in checked_results)
            self.assertEqual(ground_truths[key], checked_results[key])
        #print("check_divorce_before_death test on {f} passed.".format(f=file_path))

    # testcase for user story 03:
    def test_s1us03_birth_before_death(self,
                                file_path='test_files/Family.ged',
                                ground_truth_file_path='test_files/testcase_03.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.check_birth_before_death()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            #print(ground_truths[key])
            self.assertEqual(ground_truths[key], check_results[key])
        #print("Check_Birth_Before_Death test passed on {f}".format(f=file_path))

    # testcase for user story 08:
    def test_s1us08_childbirth_before_parentsMarriage(self,
                                              file_path='test_files/Family.ged',
                                              ground_truth_file_path='test_files/testcase_08.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.check_childbirth_before_parents_marriage()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])
        #print("Check_ChildBirth_Before_ParentsMariage test passed on {f}".format(f=file_path))

    # US05 marriage before death
    def test_s1us05_marriage_before_death(self,
                    file_path='test_files/Family.ged',
                    ground_truth_file_path='test_files/marriage_before_death.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_marriage_before_death()
        # print(checked_results)
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in checked_results)
            self.assertEqual(ground_truths[key], checked_results[key])
        #print("check_marriage_before_death test on {f} passed.".format(f=file_path))

    # US10 marriage after 14
    def test_s1us10_marriage_after_fourteen(self, file_path='test_files/Family.ged', ground_truth_file_path='test_files/marriage_before_fourteen.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_marriage_after_fourteen()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in checked_results)
            self.assertEqual(ground_truths[key], checked_results[key])
        #print("check_marriage_after_fourteen test on {f} passed.".format(f=file_path))

    # testcase for user story 02:
    def test_s1us02_birth_before_marriage(self,
                                file_path='test_files/Family.ged',
                                ground_truth_file_path='test_files/testcase_02.json'):
        ged = Gedcom()
        ged.parse(file_path)
        ged.print_individuals()
        ged.print_families()
        check_results = ged.check_birth_before_marriage()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])
        #print("Check_Birth_Before_Marriage test passed on {f}".format(f=file_path))

    # testcase for user story 07:
    def test_s1us07_age_lessthan_150(self,
                                file_path='test_files/Family.ged',
                                ground_truth_file_path='test_files/testcase_07.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.check_age_lessthan_150()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])
        #print("Check_Age_LessThan_150 test passed on {f}".format(f=file_path))

    # Sprint 2
    # test US16
    def test_s2us16_male_last_names(self, file_path='test_files/Family.ged', ground_truth_file_path='test_files/male_last_names.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_male_last_names()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # testcase US 09
    def test_s2us09_old_parents(self,
                    file_path='test_files/Family.ged',
                    ground_truth_file_path='test_files/testcase_09.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.check_old_parents()
        with open(ground_truth_file_path, 'r') as f:
                ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])
        #print("Check_old_parents test passed on {f}.".format(f=file_path))

    # testcase US 12
    def test_s2us12_birth_before_death_of_parents(self,
                    file_path='test_files/Family.ged',
                    ground_truth_file_path='test_files/testcase_12.json'):
    	ged = Gedcom()
    	ged.parse(file_path)
    	check_results = ged.check_birth_before_death_of_parents()
    	with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
    	for key in ground_truths:
            #print(ground_truths[key])
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])
    	#print("Check_birth_before_death_of_parents test passed on {f}".format(f=file_path))

    # testcase US 17
    def test_s2us17_marry_descendants(self,file_path='test_files/Family.ged'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results=ged.check_marry_descendants()
        return check_results

    # Testcase US 14
    def test_s2us14_check_multiple_births(self, file_path='test_files/Family.ged',
                                    ground_truth_file_path='test_files/testcase_14.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_multiple_births()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Testcase US 15
    def test_s2us15_check_siblings_count(self, file_path='test_files/Family.ged',
                                  ground_truth_file_path='test_files/testcase_15.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_siblings_count()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    #Testcase US 21
    def test_s2us21_check_Correct_gender(self, file_path='test_files/Family.ged',
                                    ground_truth_file_path='test_files/testcase_21.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_Correct_gender()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    #Testcase US 13
    def test_s2us13_check_Siblings_Spacing(self, file_path='test_files/Family.ged',
                                    ground_truth_file_path='test_files/testcase_13.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_sibling_spacing()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Sprint 3
    # Testcase US 28
    def test_s3us28_order_siblings(self, file_path='test_files/Family.ged',
                                  ground_truth_file_path='test_files/testcase_28.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.order_siblings_by_age()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Testcase US 34
    def test_s3us34_large_age_difference(self, file_path='test_files/Family.ged',
                                  ground_truth_file_path='test_files/testcase_34.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.large_age_difference()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Testcase US 35
    def test_s3us35_recent_births(self,
                                file_path='test_files/Family.ged',
                                ground_truth_file_path='test_files/testcase_35.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.check_recent_births()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])

    # Testcase US 36
    def test_s3us36_recent_deaths(self, file_path='test_files/Family.ged',
                                  ground_truth_file_path='test_files/testcase_36.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.check_recent_deaths()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])

    # Testcase US 27
    def test_s4us27_include_ages(self, file_path='test_files/Family.ged',
                                  ground_truth_file_path='test_files/testcase_27.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.include_ages()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])
        
    #Testcase US33
    def test_s4us33_orphans(self, file_path='test_files/Family.ged',
                                  ground_truth_file_path='test_files/testcase_33.json'):
        ged = Gedcom()
        ged.parse(file_path)
        check_results = ged.check_orphans()
        with open(ground_truth_file_path, 'r') as f:
            ground_truths = json.load(f)
        for key in ground_truths:
            self.assertTrue(key in check_results)
            self.assertEqual(ground_truths[key], check_results[key])

    # Testcase US 18
    def test_s3us18_no_one_marries_sibling(self, file_path='test_files/Family.ged'):
        ged = Gedcom()
        ged.parse(file_path)
        ged.check_no_one_marries_sibling()

    # Testcase US 19
    def test_s3us19_no_one_marries_first_cousin(self, file_path='test_files/Family.ged'):
        ged = Gedcom()
        ged.parse(file_path)
        ged.check_no_one_marries_first_cousin()

    # Test case US 31
    def test_s3us31_check_list_single(self, file_path='test_files/Family.ged',ground_truth_file_path='test_files/testcase_31.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_list_single()
        self._check_ground_truth(checked_results, ground_truth_file_path)
    # Test case US 30
    def test_s3us30_check_list_married(self, file_path='test_files/Family.ged', ground_truth_file_path='test_files/testcase_30.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_list_married()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Sprint-4
    # Test case US 38:
    def test_s4us38_check_upcoming_birthdays(self, file_path='test_files/Family.ged', ground_truth_file_path=None):
        ged = Gedcom()
        ged.parse(file_path)
        ged.upcoming_birthdays()
        #self._check_ground_truth(checked_results, ground_truth_file_path)

    # Test case US 39:
    def test_s4us39_check_upcoming_anniversaries(self, file_path='test_files/Family.ged', ground_truth_file_path=None):
        ged = Gedcom()
        ged.parse(file_path)
        ged.upcoming_anniversaries()
        #self._check_ground_truth(checked_results, ground_truth_file_path)

    # Test case US 24:
    def test_s4us24_check_unique_family(self, file_path='test_files/Family.ged', ground_truth_file_path='test_files/testcase_24.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_unique_family()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Test case US 25
    def test_s4us25_check_unique_first_name_in_family(self, file_path='test_files/Family.ged', ground_truth_file_path='test_files/testcase_25.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_unique_first_name_in_family()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Test case US 01
    def test_s4us01_check_current_dates(self, file_path='test_files/Family.ged',
                                 ground_truth_file_path='test_files/testcase_01.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_current_dates()
        self._check_ground_truth(checked_results, ground_truth_file_path)

    # Test case US 29
    def test_s4us29_check_list_deaths(self, file_path='test_files/Family.ged',
                               ground_truth_file_path='test_files/testcase_29.json'):
        ged = Gedcom()
        ged.parse(file_path)
        checked_results = ged.check_list_deaths()
        self._check_ground_truth(checked_results, ground_truth_file_path)

if __name__ == "__main__":
    unittest.main()
