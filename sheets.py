import gspread

class Sheets(object):
    def __init__(self, credentials, sheetname):
        self._credentials = credentials
        self._account = gspread.service_account(filename=credentials)
        self.sheet = self._account.open(sheetname).sheet1
    
    def init_sheet(self):
        self.sheet.resize(1)
        # labels
        self.sheet.update('A1', [["Team Number", "Auton Upper", "Auton Lower", "Tele-Op Upper", "Tele-Op Lower", "Hang Level", "Scoring Bonus", "Hanger Bonus", "Problems"]])

    def append_row(self, row: tuple):
        self.sheet.append_row(row)
