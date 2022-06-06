import glob

class DownloadsHandler():
    def __init__(self, results_dir):
        self.results_dir = results_dir
    
    def make_book(self):
        pass

    def delete_book(self):
        pass

    def get_all_books(self):
        pass

    def _print_books(self):
        print(glob.glob(self.results_dir))