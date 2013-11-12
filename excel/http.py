import datetime

from django.db.models.query import QuerySet, ValuesQuerySet
from django.http import HttpResponse

def valid_sheet_data(data):
    # Make sure we've got the right type of data to work with
    valid_data = False
    if isinstance(data, ValuesQuerySet):
        data = list(data)
    elif isinstance(data, QuerySet):
        data = list(data.values())
    if hasattr(data, '__getitem__'):
        if isinstance(data[0], dict):
            headers = data[0].keys()
            data = [[row[col] for col in headers] for row in data]
            data.insert(0, headers)
        if hasattr(data[0], '__getitem__'):
            valid_data = True
    assert valid_data is True, "ExcelResponse requires a sequence of sequences"

    return valid_data

def get_sheet_data(data, headers=None):
    # Make sure we've got the right type of data to work with
    valid_data = False
    if isinstance(data, ValuesQuerySet):
        data = list(data)
    elif isinstance(data, QuerySet):
        data = list(data.values())
    if hasattr(data, '__getitem__'):
        if isinstance(data[0], dict):
            if headers is None:
                headers = data[0].keys()
            data = [[row[col] for col in headers] for row in data]
            data.insert(0, headers)
        if hasattr(data[0], '__getitem__'):
            valid_data = True
    assert valid_data is True, "ExcelResponse requires a sequence of sequences"

    if valid_data:
        return data

def get_output(book_data, force_csv, encoding):
    # Calculates the total lenght
    lenght = 0
    for sheet_data in book_data:
        lenght = lenght + len(sheet_data)

    # check if the excel lib is install
    # https://pypi.python.org/pypi/xlwt
    # And if the excel file can support the ammount of data
    if lenght <= 65536 and force_csv is not True:
        try:
            import xlwt
        except ImportError:
            pass
        else:
            use_xls = True

    # Lets render the book
    import StringIO
    output = StringIO.StringIO()
    if use_xls:
        book = xlwt.Workbook(encoding=encoding)

        count=0
        for sheet_data in book_data:
            count = count + 1
            sheet = book.add_sheet('Sheet ' + str(count))
            styles = {
            'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
            'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
            'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
            'default': xlwt.Style.default_style
            }
            for x, row in enumerate(sheet_data):
                for y, value in enumerate(row):
                    if isinstance(value, datetime.datetime):
                        cell_style = styles['datetime']
                    elif isinstance(value, datetime.date):
                        cell_style = styles['date']
                    elif isinstance(value, datetime.time):
                        cell_style = styles['time']
                    else:
                        cell_style = styles['default']
                        sheet.write(x, y, value, style=cell_style)

        book.save(output)
        mimetype = 'application/vnd.ms-excel'
        file_ext = 'xls'
    else:
        for sheet_data in book_data:
            for row in sheet_data:
                out_row = []
                for value in row:
                    if not isinstance(value, basestring):
                        value = unicode(value)
                        value = value.encode(encoding)
                        out_row.append(value.replace('"', '""'))
                output.write('"%s"\n' %
                             '";"'.join(out_row))
        mimetype = 'text/csv'
        file_ext = 'csv'

    output.seek(0)
    return {'output' : output.getvalue(), 'mimetype' : mimetype, 'file_ext' : file_ext}

class ExcelBookResponse(HttpResponse):
    def __init__(self, book, output_name='excel_book', headers=None,
                 force_csv=False, encoding='utf8'):

        book_data = []
        for sheet in book:
            if valid_sheet_data(sheet):
                book_data = book_data + [get_sheet_data(sheet)]
        output = get_output(book_data, force_csv, encoding)

        super(ExcelBookResponse, self).__init__(content=output['output'], mimetype=output['mimetype'])
        self['Content-Disposition'] = 'attachment;filename="%s.%s"' % \
            (output_name.replace('"', '\"'), output['file_ext'])

class ExcelResponse(HttpResponse):
    def __init__(self, data, output_name='excel_data', headers=None,
                 force_csv=False, encoding='utf8'):

        output = get_output((get_sheet_data(data), ), force_csv, encoding)

        super(ExcelResponse, self).__init__(content=output['output'], mimetype=output['mimetype'])
        self['Content-Disposition'] = 'attachment;filename="%s.%s"' % \
            (output_name.replace('"', '\"'), output['file_ext'])
