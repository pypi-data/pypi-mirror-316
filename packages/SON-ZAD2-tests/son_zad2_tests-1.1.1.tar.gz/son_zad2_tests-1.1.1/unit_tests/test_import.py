"""
Unit tests for Import functionalities.
"""

import os
from git_project.methods.import_students import ImportStudents


class TestImportStudents:

    def test_csv_import(self):
        # Given
        path = "test_students_import.csv"
        student_details_structure = ["Name", "Surname", "ID"]
        file_content = """Anna;Nowak;ABC45\nGrzegorz;Boczek;XYZ78"""
        with open(path, "w") as file:
            file.write(file_content)
        want = [
            {"Name": "Anna", "Surname": "Nowak", "ID": "ABC45"},
            {"Name": "Grzegorz", "Surname": "Boczek", "ID": "XYZ78"},
        ]

        # When
        got = ImportStudents.csv(path, student_details_structure)

        # Then
        assert want == got
        os.remove(path)

    def test_txt_import(self):
        # Given
        path = "test_students_import.txt"
        student_details_structure = ["Name", "Surname", "ID"]
        file_content = """Anna Nowak ABC45\nGrzegorz Boczek XYZ78"""
        with open(path, "w") as file:
            file.write(file_content)
        want = [
            {"Name": "Anna", "Surname": "Nowak", "ID": "ABC45"},
            {"Name": "Grzegorz", "Surname": "Boczek", "ID": "XYZ78"},
        ]

        # When
        got = ImportStudents.txt(path, student_details_structure)

        # Then
        assert want == got
        os.remove(path)
