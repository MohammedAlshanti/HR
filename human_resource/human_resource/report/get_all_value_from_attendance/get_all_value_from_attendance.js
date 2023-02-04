// Copyright (c) 2023, Mohammed Alshanti and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Get All Value From Attendance"] = {
	"filters": [
	{ fieldname: 'employee', label: __('Employee'), fieldtype: 'Link', options: 'Employeee' },
	{ fieldname: 'attendance_date', label: __('Attendance Date'), fieldtype: 'Date'},
	]
};
