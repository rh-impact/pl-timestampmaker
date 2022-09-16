
from unittest import TestCase
from unittest.mock import patch
import mock
from timestampmaker.timestampmaker import TimestampMaker
from os import mkdir, listdir, utime
from os.path import dirname, join, abspath, exists, getmtime
from shutil import rmtree, copyfile
from logging import getLogger, DEBUG


log = getLogger()
log.setLevel(DEBUG)


def mock_side_effect_move_file(options):
    """Function that will move a file from one location to the other
    if the file does not already exist in the location. A new timestamp
    is set for the file when it was able to be "moved/copied"
    """
    input_dir, output_dir = options.inputdir, options.outputdir
    
    for file in listdir(input_dir):
        
        filename = file.split("/")[-1]
        output_file = join(output_dir, filename)
        if not exists(output_file):
            # copy the file over
            copyfile(join(input_dir, file), output_file)
            
            # change the date of modification to right now
            utime(output_file)


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
        log.debug(single_files)
        log.debug(self.single_file)
 
        # this should be multiple
        multi_files = []
        for file in listdir(self.multi_file_input_dir):
            filename = file.split("/")[-1]
            if not filename.startswith("."):
                multi_files.append(filename)
        if len(multi_files) < 2:
            raise RuntimeError("should have at least 2 files in multiple file input dir")
        self.multiple_files = [data.split("/")[-1] for data in multi_files]
        
        log.debug(multi_files)
        log.debug(self.multiple_files)
        
        # Create the output directories. These will be torn down at 
        # the conclusion of the tests. 
        self.creating_single = not exists(self.single_file_output_dir)
        if self.creating_single:
            mkdir(self.single_file_output_dir)
        
        self.creating_multi = not exists(self.multi_file_output_dir)
        if self.creating_multi:
            mkdir(self.multi_file_output_dir)        

    def tearDown(self):
        # remove the directories that were created in the setup.
        if self.creating_single and exists(self.single_file_output_dir):
            rmtree(self.single_file_output_dir)
        
        if self.creating_multi and exists(self.multi_file_output_dir):
            rmtree(self.multi_file_output_dir)

    def test_01_single_file(self):
        """Test that a single file in a valid input directory will
        produce a single file in a valid output directory.
        """ 
        args = [self.single_file_input_dir, self.single_file_output_dir]
        options = self.app.parse_args(args)
        with mock.patch('timestampmaker.timestampmaker.TimestampMaker.run', side_effect=mock_side_effect_move_file):
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
        
        with mock.patch('timestampmaker.timestampmaker.TimestampMaker.run', side_effect=mock_side_effect_move_file):
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
        
        # get the time that the file was last modified.
        # this time should NOT CHANGE 
        if not exists(join(self.single_file_output_dir, self.single_file)):
            class Options:
                def __init__(self, i, o):
                    self.inputdir = i
                    self.outputdir = o
            mock_side_effect_move_file(Options(self.single_file_input_dir, self.single_file_output_dir))
        before_mod_time = getmtime(join(self.single_file_output_dir, self.single_file))
        
        # this _would_ change the time for the files
        with mock.patch('timestampmaker.timestampmaker.TimestampMaker.run', side_effect=mock_side_effect_move_file):
            self.app.run(options)
        
        for file in listdir(self.single_file_output_dir):
            filename = file.split("/")[-1]
            self.assertEqual(self.single_file, filename)
            after_mod_time = getmtime(join(self.single_file_output_dir, filename))
            self.assertAlmostEqual(before_mod_time, after_mod_time, 0)

    def test_04_multi_file_not_converted(self):
        """Test that at least one of the multiple files in a valid directory
        is NOT converted as the data already exists in the output directory.
        """
        args = [self.multi_file_input_dir, self.multi_file_output_dir]
        options = self.app.parse_args(args)

        modified_times_before = {}
        
        # get the time that the file was last modified.
        # this time should NOT CHANGE 
        class Options:
            def __init__(self, i, o):
                self.inputdir = i
                self.outputdir = o
        mock_side_effect_move_file(Options(self.multi_file_input_dir, self.multi_file_output_dir))
            
        for file in listdir(self.multi_file_output_dir):
            modified_times_before[str(file)] = getmtime(join(self.multi_file_output_dir, file))

        # this _would_ change the time for the files
        with mock.patch('timestampmaker.timestampmaker.TimestampMaker.run', side_effect=mock_side_effect_move_file):
            self.app.run(options)
        
            for file in listdir(self.multi_file_output_dir):
                filename = file.split("/")[-1]
                self.assertTrue(filename in self.multiple_files)
                self.assertAlmostEqual(
                    modified_times_before[str(file)],
                    getmtime(join(self.multi_file_output_dir, file)),
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

