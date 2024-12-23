import os
import unittest
from unittest.mock import patch
from git_project.methods.add_student import ModifyStudents
from git_project.methods.export_students import ExportStudents


class TestModifyStudentsAndExport(unittest.TestCase):
    def setUp(self):
        self.path_csv = "test_students.csv"
        self.path_txt = "test_students.txt"
        self.students = []

    def tearDown(self):
        if os.path.exists(self.path_csv):
            os.remove(self.path_csv)
        if os.path.exists(self.path_txt):
            os.remove(self.path_txt)

    @patch("builtins.input", side_effect=["Anna", "Nowak", "ABC45"])
    def test_add_student_and_export_real_files(self, mock_input):
        # Given
        expected_csv_content = "Anna;Nowak;ABC45"
        expected_txt_content = "Anna Nowak - ABC45"

        # When
        ModifyStudents.add_student_and_export(self.path_csv, self.path_txt, self.students)

        # Then
        self.assertEqual(self.students, [{"Name": "Anna", "Surname": "Nowak", "ID": "ABC45"}])

        with open(self.path_csv, "r") as file:
            csv_content = file.read().strip()
        self.assertEqual(csv_content, expected_csv_content)

        with open(self.path_txt, "r") as file:
            txt_content = file.read().strip()
        self.assertEqual(txt_content, expected_txt_content)

    def test_export_students_directly(self):
        # Given
        students = [{"Name": "Anna", "Surname": "Nowak", "ID": "ABC45"}]
        expected_csv_content = "Anna;Nowak;ABC45"
        expected_txt_content = "Anna Nowak - ABC45"

        # When
        ExportStudents.csv(self.path_csv, students)
        ExportStudents.txt(self.path_txt, students)

        # Then: Sprawdzenie rzeczywistej zawartości pliku CSV (ignorując białe znaki)
        with open(self.path_csv, "r") as file:
            csv_content = file.read().strip()
        self.assertEqual(csv_content, expected_csv_content)

        # Sprawdzenie rzeczywistej zawartości pliku TXT (ignorując białe znaki)
        with open(self.path_txt, "r") as file:
            txt_content = file.read().strip()
        self.assertEqual(txt_content, expected_txt_content)


if __name__ == "__main__":
    unittest.main()
