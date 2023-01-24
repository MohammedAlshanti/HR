# Copyright (c) 2023, Mohammed Alshanti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
from frappe import _

class LeaveApplication(Document):
	def validate(self):
		self.set_total_leave_days()
		self.get_total_leaves_allocated()
		self.check_balance()

	def on_submit(self):
		self.update_balance_allocation_on_submit()

	def set_total_leave_days(self):
		if self.from_date and self.to_date:
			total_leave_days= date_diff(self.to_date,self.from_date)
			if total_leave_days>=0:
				self.total_leave_days=total_leave_days+1


	def get_total_leaves_allocated(self):
		if self.employee and self.leave_type and self.from_date and self.to_date:
			leaves_allocated = frappe.db.sql(""" select total_leaves_allocated from 'tabLeave Allocation'
			 					WHERE employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
								(self.employee,self.leave_type,self.from_date,self.to_date),as_dict =1)
			if leaves_allocated:
				self.leave_balance_before_application = str(leaves_allocated[0].total_leaves_allocated)


	def check_balance(self):
		if self.total_leave_days and self.leave_balance_before_application:
			if float(self.total_leave_days)> float(self.leave_balance_before_application):
				frappe.throw(_("your balance not enough for "+self.leave_type))


	def update_balance_allocation_on_submit(self):
		new_balance_allocated = float(self.leave_balance_before_application) - float(self.total_leave_days)
		frappe.db.sql(""" UPDATE 'tabLeave Allocation' set total_leaves_allocated = %s 
					 WHERE employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
					  (new_balance_allocated,self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		frappe.db.commit()



