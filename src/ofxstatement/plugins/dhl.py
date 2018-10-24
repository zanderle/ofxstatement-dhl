import csv
import re

from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import StatementLine, BankAccount

SIGNATURES = [
    "Valuta;Datum valute;Datum knjiženja;ID transakcije;Št. za reklamacijo;Prejemnik / Plačnik;Breme;Dobro;Referenca plačnika;Referenca prejemnika;Opis prejemnika",  # Oct 2018
]


class DhlCSVStatementParser(CsvStatementParser):

    date_format = "%d.%m.%Y"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';', quotechar='"')

    def parse_amount(self, value):
        if not value or not value.strip():
            return 0

        return self.parse_float(value.strip().replace('.', '').replace(',', '.'))

    def parse_record(self, line):
        try:
            stmt_line = StatementLine()
            stmt_line.date = self.parse_datetime(line[1].strip())

            # Amount
            paid_out = -self.parse_amount(line[6])
            paid_in = self.parse_amount(line[7])
            stmt_line.amount = paid_out or paid_in

            reference = line[3].strip()
            trntype = False

            if not trntype:
                trntype = 'POS'  # Default: Debit card payment

            stmt_line.payee = line[5]
            stmt_line.memo = line[10]

            return stmt_line
        except Exception as e:
            print('Something went wrong: %s' % e)
            return None


class DHLPlugin(Plugin):
    def get_parser(self, fin):
        f = open(fin, "r", encoding='windows-1250')
        line = f.readline()
        while line != '':
            line = line.strip()
            if line in SIGNATURES:
                parser = DhlCSVStatementParser(f)
                if 'account' in self.settings:
                    parser.statement.account_id = self.settings['account']
                else:
                    parser.statement.account_id = 'Delavska Hranilnica'
                if 'currency' in self.settings:
                    parser.statement.currency = self.settings['currency']
                else:
                    parser.statement.currency = 'EUR'
                parser.statement.bank_id = self.settings.get('bank', 'Delavska Hranilnica')
                return parser

            line = f.readline()

        # no plugin with matching signature was found
        raise Exception("No suitable DHL parser "
                        "found for this statement file.")
