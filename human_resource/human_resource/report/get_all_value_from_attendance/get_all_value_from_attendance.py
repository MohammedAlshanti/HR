# Copyright (c) 2023, Mohammed Alshanti and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], []
	data = get_all_data(filters)
	columns = get_all_columns()
	return columns, data

def get_all_data(filters):
	return frappe.db.get_all('Attendance',['employee', 'full_name', 'attendance_date', 'department', 'status', 'check_in', 'check_out', 'work_hours', 'late_hours'],filters=filters)

def get_all_columns():
	columns = [
		{'fieldname': 'employee', 'label': _('Employee'), 'fieldtype': 'Link', 'options': 'Employeee'},
		{'fieldname': 'full_name', 'label': _('Full Name'), 'fieldtype': 'Data'},
		{'fieldname': 'attendance_date', 'label': _('Attendance Date'), 'fieldtype': 'Data'},
		{'fieldname': 'department', 'label': _('Department'), 'fieldtype': 'Link', 'options': 'Department'},
		{'fieldname': 'status', 'label': _('Status'), 'fieldtype': 'Select', 'options': ['Present','Absent','Half Day']},
		{'fieldname': 'check_in', 'label': _('Check In'), 'fieldtype': 'Time'},
		{'fieldname': 'check_out', 'label': _('Check Out'), 'fieldtype': 'Time'},
		{'fieldname': 'work_hours', 'label': _('Work Hours'), 'fieldtype': 'Float'},
		{'fieldname': 'late_hours', 'label': _('Late Hours '), 'fieldtype': 'Float'},
	]
	return columns


