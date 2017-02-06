#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2016-2017 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl

import unittest
import openpyxl
import os.path as osp
import schedula.utils as sh_utl
from formulas.excel import ExcelModel, BOOK


mydir = osp.dirname(__file__)
_filename = 'test.xlsx'
_link_filename = 'test_link.xlsx'


def _book2dict(book):
    res = {}
    for ws in book.worksheets:
        s = res[ws.title] = {}
        for k, cell in ws._cells.items():
            value = cell.value
            if value is not None:
                s[cell.coordinate] = value
    return res


class TestExcelModel(unittest.TestCase):
    def setUp(self):
        self.filename = osp.join(mydir, _filename)
        self.link_filename = osp.join(mydir, _link_filename)
        self.results = {
            _filename.upper(): _book2dict(
                openpyxl.load_workbook(self.filename, data_only=True)
            ),
            _link_filename.upper(): _book2dict(
                openpyxl.load_workbook(self.link_filename, data_only=True)
            ),
        }
        self.maxDiff = None

    def test_excel_model(self):
        xl_model = ExcelModel()
        xl_model.loads(self.filename)
        xl_model.finish()
        xl_model.calculate()
        books = xl_model.books
        books = {k: _book2dict(v[BOOK])
                 for k, v in xl_model.write(books).items()}
        self.assertEqual(books, self.results)

        books = {k: _book2dict(v[BOOK]) for k, v in xl_model.write().items()}
        res = {}
        for k, v in sh_utl.stack_nested_keys(self.results, depth=2):
            sh_utl.get_nested_dicts(res, *map(str.upper, k), default=lambda: v)
        self.assertEqual(books, res)
