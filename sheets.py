import gspread

class Sheet(object):
    def __init__(self, credentials, sheetname):
        self._credentials = credentials
        self._account = gspread.service_account_from_dict(credentials)
        self.sheet = self._account.open(sheetname).sheet1
    
    def init_sheet(self):
        self.sheet.resize(1)
        # labels
        self.sheet.update('A1', [["Team Number", "Auton Upper", "Auton Lower", "Tele-Op Upper", "Tele-Op Lower", "Hang Level", "Scoring Bonus", "Hanger Bonus", "Problems"]])

    def append_row(self, row: tuple):
        self.sheet.append_row(row)

    def append_to_next_empty_row(self, row:list):
        str_list = list(filter(None, self.sheet.col_values(1)))
        next_empty_row = str(len(str_list)+1)
        print(next_empty_row)
        self.sheet.append_row(row, table_range=f'A{next_empty_row}')