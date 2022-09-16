
from unittest import TestCase
from unittest import mock
from timestampmaker.timestampmaker import TimestampMaker
from os import mkdir, remove
from os.path import dirname, join, abspath
from shutil import rmtree


class TimestampMakerTests(TestCase):
    """
    Test TimestampMaker.
    """
    def setUp(self):
        self.app = TimestampMaker()

        self.single_file_input_dir = join(dirname(abspath(__file__)), "test_data")
        # self.single_file_input_dir = join(dirname(abspath(__file__)), "test_data_single_input")
        self.multi_file_input_dir = join(dirname(abspath(__file__)), "test_data_multi_input")

        self.single_file_output_dir = join(dirname(abspath(__file__)), "test_data")
        # self.single_file_output_dir = join(dirname(abspath(__file__)), "test_data_single_output")
        self.multi_file_output_dir = join(dirname(abspath(__file__)), "test_data_multi_output")
        

    def test_single_file(self):
        """Test that a single file in a valid input directory will
        produce a single file in a valid output directory.
        """

    def test_multi_file(self):
        """Test that a set of files in a valid input directory will
        produce a set of files in the valid output directory. The 
        number of files should be the same in the directories, and the
        names should be relatively the same (or as expected).
        """

    def test_single_file_not_converted(self):
        """Test that a single file in a valid input directory is NOT
        converted as the data already exists in the output directory.
        """

    def test_multi_file_not_converted(self):
        """Test that at least one of the multiple files in a valid directory
        is NOT converted as the data already exists in the output directory.
        """

    def test_invalid_input_directory(self):
        """Test that the input directory is not valid."""
        args = ["random_bad_input_directory"]
        args.append(self.single_file_output_dir)
        options = self.app.parse_args(args)
        with self.assertRaises(FileNotFoundError):
            self.app.run(options)

    def test_invalid_output_directory(self):
        """Test that the output directory is not valid."""
        args = [self.single_file_input_dir]
        args.append("random_bad_output_directory")
        options = self.app.parse_args(args)
        with self.assertRaises(FileNotFoundError):
            self.app.run(options)

    """
    def test_run(self):
        '''
        Test the run code.
        '''
        args = []
        if self.app.TYPE == 'ds':
            args.append('inputdir') # you may want to change this inputdir mock
        args.append('outputdir')  # you may want to change this outputdir mock

        # you may want to add more of your custom defined optional arguments to test
        # your app with
        # eg.
        # args.append('--custom-int')
        # args.append(10)

        options = self.app.parse_args(args)
        self.app.run(options)

        # write your own assertions
        self.assertEqual(options.outputdir, 'outputdir')
    """
