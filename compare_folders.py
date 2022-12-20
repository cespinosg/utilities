import pathlib
import shutil


class Comparator:
    '''
    Compares the content of two folders.
    '''

    def __init__(self, a_folder, b_folder):
        self.a_folder = pathlib.Path(a_folder)
        self.b_folder = pathlib.Path(b_folder)
        self._get_diffs()

    def _get_diffs(self):
        '''
        Gets the differences.
        '''
        self.a_files = [f.name for f in self.a_folder.iterdir()]
        self.b_files = [f.name for f in self.b_folder.iterdir()]
        self.in_a_not_in_b = [f for f in self.a_files if f not in self.b_files]
        self.in_b_not_in_a = [f for f in self.b_files if f not in self.a_files]

    def write_diffs(self, out_file):
        '''
        Writes the differences to the given output file.
        '''
        lns = [f'Files in {self.a_folder} not in {self.b_folder}']
        lns += self.in_a_not_in_b
        lns += [f'\nFiles in {self.b_folder} not in {self.a_folder}']
        lns += self.in_b_not_in_a
        lns = '\n'.join(lns)
        with open(out_file, 'w') as fout:
            fout.write(lns)

    def copy_diffs(self, comp_folder):
        '''
        Copies the different files to the comparison folder.
        '''
        self.comp_folder = pathlib.Path(comp_folder)
        self._create_folders()
        self._copy_diff_files()
        self.write_diffs(self.comp_folder / 'diffs.txt')

    def _create_folders(self):
        '''
        Creates folders for copying the different files.
        '''
        if not self.comp_folder.is_dir():
            self.comp_folder.mkdir()
        self.a_not_in_b_folder = self.comp_folder / 'a_not_in_b'
        if self.a_not_in_b_folder.is_dir():
            shutil.rmtree(self.a_not_in_b_folder)
        self.a_not_in_b_folder.mkdir()
        self.b_not_in_a_folder = self.comp_folder / 'b_not_in_a'
        if self.b_not_in_a_folder.is_dir():
            shutil.rmtree(self.b_not_in_a_folder)
        self.b_not_in_a_folder.mkdir()

    def _copy_diff_files(self):
        '''
        Copies the different files.
        '''
        for f in self.in_a_not_in_b:
            src = self.a_folder / f
            dst = self.a_not_in_b_folder / f
            shutil.copy(src, dst)
        for f in self.in_b_not_in_a:
            src = self.b_folder / f
            dst = self.b_not_in_a_folder / f
            shutil.copy(src, dst)


if __name__ == '__main__':
    a_folder = 'C:/Users/Carlos/Desktop/2021'
    b_folder = 'C:/Users/Carlos/Desktop/Mobil-2021'
    comparator = Comparator(a_folder, b_folder)
    # comparator.write_diffs('diffs.txt')
    comparator.copy_diffs('comparison')
