class HandleGlobalMode:

    def __init__(self):
        self.help_keyword = None
        self.file_name = None

    def open_help(self, keyword: str):
        """Open help for the given keyword."""
        self.help_keyword = keyword
        print(f"Help for {keyword} opened.")

    def save_as(self, file: str):
        """Save the file as the given name."""
        self.file_name = file
        print(f"File saved as {file}.")

    def close_pane(self):
        """Close the current pane."""
        print("Current pane closed.")

    def open_terminal(self):
        """Open a terminal window."""
        print("Terminal window opened.")

    def open_man_page(self, word: str):
        """Open the man page for the word under the cursor."""
        print(f"Man page for {word} opened.")