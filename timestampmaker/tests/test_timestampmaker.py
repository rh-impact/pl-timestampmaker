
from unittest import TestCase
from unittest import mock
from timestampmaker.timestampmaker import TimestampMaker
from os import mkdir, remove, listdir
from os.path import dirname, join, abspath, exists, getmtime
from shutil import rmtree


class TimestampMakerTests(TestCase):
    """
    Test TimestampMaker.
    """
    def setUp(self):
        self.app = TimestampMaker()

        self.single_file_input_dir = join(dirname(abspath(__file__)), "test_data_single_input")
        self.multi_file_input_dir = join(dirname(abspath(__file__)), "test_data_multi_input")

        self.single_file_output_dir = join(dirname(abspath(__file__)), "test_data_single_output")
        self.multi_file_output_dir = join(dirname(abspath(__file__)), "test_data_multi_output")
        
        # this should only be 1
        single_files = []
        for file in listdir(self.single_file_input_dir):
            filename = file.split("/")[-1]
            if not filename.startswith("."):
                single_files.append(filename)
        if len(single_files) != 1:
            raise RuntimeError("should only have one file in the single input dir")
        self.single_file = single_files[0].split("/")[-1]
 
        # this should be multiple
        multi_files = []
        for file in listdir(self.multi_file_input_dir):
            filename = file.split("/")[-1]
            if not filename.startswith("."):
                multi_files.append(filename)
        if len(multi_files) < 2:
            raise RuntimeError("should have at least 2 files in multiple file input dir")
        self.multiple_files = [data.split("/")[-1] for data in multi_files]
        
        # Create the output directories. These will be torn down at 
        # the conclusion of the tests. 
        mkdir(self.single_file_output_dir)
        mkdir(self.multi_file_output_dir)        

    def tearDown(self):
        # remove the directories that were created in the setup.
        if exists(self.single_file_output_dir):
            rmtree(self.single_file_output_dir)
        
        if exists(self.multi_file_output_dir):
            rmtree(self.multi_file_output_dir)
        
    def test_01_single_file(self):
        """Test that a single file in a valid input directory will
        produce a single file in a valid output directory.
        """ 
        args = [self.single_file_input_dir, self.single_file_output_dir]
        options = self.app.parse_args(args)
        self.app.run(options)
        
        self.assertEqual(len(listdir(self.single_file_output_dir)), 1)
        
        for file in listdir(self.single_file_output_dir):
            filename = file.split("/")[-1]
            self.assertEqual(self.single_file, filename)

    def test_02_multi_file(self):
        """Test that a set of files in a valid input directory will
        produce a set of files in the valid output directory. The 
        number of files should be the same in the directories, and the
        names should be relatively the same (or as expected).
        """
        args = [self.multi_file_input_dir, self.multi_file_output_dir]
        options = self.app.parse_args(args)
        self.app.run(options)
        
        self.assertEqual(len(listdir(self.multi_file_output_dir)), len(self.multiple_files))
        
        for file in listdir(self.multi_file_output_dir):
            filename = file.split("/")[-1]
            self.assertTrue(filename in self.multiple_files)

    def test_03_single_file_not_converted(self):
        """Test that a single file in a valid input directory is NOT
        converted as the data already exists in the output directory.
        """
        args = [self.single_file_input_dir, self.single_file_output_dir]
        options = self.app.parse_args(args)
        
        self.assertEqual(len(listdir(self.single_file_output_dir)), 1)
        
        # get the time that the file was last modified.
        # this time should NOT CHANGE 
        before_mod_time = getmtime(join(self.single_file_output_dir, self.single_file))
        
        # this _would_ change the time for the files
        self.app.run(options)
        
        for file in listdir(self.single_file_output_dir):
            filename = file.split("/")[-1]
            self.assertEqual(self.single_file, filename)
            after_mod_time = getmtime(file)
            self.assertAlmostEqual(before_mod_time, after_mod_time, 0)

    def test_04_multi_file_not_converted(self):
        """Test that at least one of the multiple files in a valid directory
        is NOT converted as the data already exists in the output directory.
        """
        args = [self.multi_file_input_dir, self.multi_file_output_dir]
        options = self.app.parse_args(args)

        self.assertEqual(len(listdir(self.multi_file_output_dir)), len(self.multiple_files))
        
        modified_times_before = {}
        
        # get the time that the file was last modified.
        # this time should NOT CHANGE 
        for file in listdir(self.multi_file_output_dir):
            modified_times_before[file] = getmtime(file)

        # this _would_ change the time for the files
        self.app.run(options)
        
        for file in listdir(self.multi_file_output_dir):
            filename = file.split("/")[-1]
            self.assertTrue(filename in self.multiple_files)
            self.assertAlmostEqual(
                modified_times_before[file], 
                getmtime(file),
                0
            )

    def test_05_invalid_input_directory(self):
        """Test that the input directory is not valid."""
        args = ["random_bad_input_directory"]
        args.append(self.single_file_output_dir)
        options = self.app.parse_args(args)
        with self.assertRaises(FileNotFoundError):
            self.app.run(options)

    def test_06_invalid_output_directory(self):
        """Test that the output directory is not valid."""
        args = [self.single_file_input_dir]
        args.append("random_bad_output_directory")
        options = self.app.parse_args(args)
        with self.assertRaises(FileNotFoundError):
            self.app.run(options)

