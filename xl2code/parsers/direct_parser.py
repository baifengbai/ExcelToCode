# -*- coding: utf-8 -*-
import traceback
import xlsconfig
import util
from tps import tp0, convention
from base_parser import ConverterInfo, BaseParser

# 利用Excel表头描述，进行导表，不需要转换器
class DirectParser(BaseParser):

	def __init__(self, filename, module, sheet_index=0):
		super(DirectParser, self).__init__(filename, module, sheet_index)

		self.field_row_index = xlsconfig.SHEET_ROW_INDEX["field"]
		self.type_row_index = xlsconfig.SHEET_ROW_INDEX["type"]


	# 使用Excel表头提供的信息，构造转换器
	def parse_header(self, row):
		super(DirectParser, self).parse_header(row)
		
		field_index, type_index = 0, 0
		if self.is_vertical:
			field_index = util.int_to_base26(self.field_row_index)
			type_index = util.int_to_base26(self.type_row_index)
		else:
			field_index = self.field_row_index + 1
			type_index = self.type_row_index + 1

		field_row 	= [self.extract_cell_value(cell) for cell in self.worksheet[field_index]]
		type_row 	= [self.extract_cell_value(cell) for cell in self.worksheet[type_index]]

		self.key_name = field_row[0]

		for header, col in self.header_2_col.iteritems():
			field = field_row[col]

			if field == "":
				util.log_error("列名不能为空，列：%s", util.int_to_base26(col))
				continue

			type = type_row[col] or "String"
			method = None
			try:
				method = convention.type2function(type)
			except:
				util.log_error("无效的类型'%s'，列：%s", type, util.int_to_base26(col))
				continue

			self.converters[col] = ConverterInfo((header, field, method, True))
			self.sheet_types[header] = (col, field, header, type)
		return
