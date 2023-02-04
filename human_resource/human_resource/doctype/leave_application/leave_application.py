# Copyright (c) 2023, Mohammed Alshanti and contributors
# For license information, please see license.txt
import datetime

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
from frappe import _

class LeaveApplication(Document):
	def validate(self):
		self.set_total_leave_days()
		self.get_total_leaves_allocated()
		self.check_balance()
		self.validate_from_date_value_after_to_date_value()

	def on_submit(self):
		self.update_balance_allocation_on_submit()

	def on_cancel1(self):
		self.update_balance_allocation_on_cancel()

	def set_total_leave_days(self):
		if self.from_date and self.to_date:
			total_leave_days= date_diff(self.to_date,self.from_date)
			if total_leave_days>=0:
				self.total_leave_days=total_leave_days+1


	def get_total_leaves_allocated(self):
		if self.employee and self.leave_type and self.from_date and self.to_date:
			leaves_allocated = frappe.db.sql("""select total_leaves_allocated from `tabLeave Allocation`
			WHERE employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
			(self.employee,self.leave_type,self.from_date,self.to_date),as_dict =1)
			if leaves_allocated:
				self.leave_balance_before_application = str(leaves_allocated[0].total_leaves_allocated)


	def check_balance(self):
		if self.total_leave_days and self.leave_balance_before_application:
			if float(self.total_leave_days)> float(self.total_leaves_allocated):
				frappe.throw(_("your balance not enough for "+self.leave_type))


	def update_balance_allocation_on_submit(self):
		new_balance_allocated = float(self.leave_balance_before_application) - float(self.total_leave_days)
		leaves_allocated = frappe.db.sql("""UPDATE `tabLeave Allocation` set total_leaves_allocated = %s
			WHERE employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
			(new_balance_allocated,self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		frappe.db.commit()


	def update_balance_allocation_on_cancel(self):
		new_balance_allocated = float(self.leave_balance_before_application) + float(self.total_leave_days)
		leaves_allocated = frappe.db.sql("""UPDATE `tabLeave Allocation` set total_leaves_allocated = %s
					WHERE employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
										 (new_balance_allocated, self.employee, self.leave_type, self.from_date,
										  self.to_date), as_dict=1)
		frappe.db.commit()
		# leaves_allocated = frappe.db.sql("""select total_leaves_allocated from `tabLeave Allocation`
		# 	WHERE employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,
		# 	(self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		# if leaves_allocated:
		# 	leave_balance_before_application = str(leaves_allocated[0].total_leaves_allocated)
		#
		# 	new_balance_allocated = float(self.total_leaves_allocated) + float(self.total_leave_days)
		# 	frappe.db.sql("""UPDATE `tabLeave Allocation` set total_leaves_allocated = %s
		# 	WHERE employee = %s and leave_type = %s and from_date between %s and  %s """,
		# 	(new_balance_allocated, self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		# 	frappe.db.commit()
	
	
	def validate_from_date_value_after_to_date_value(self):
		if self.from_date and self.to_date:
			if date_diff(self.to_date,self.from_date)<0:
				frappe.throw(_("The dates you entered are incorrect"))

	# def check_if_exist_leave_type(self):
	# 	if self.emplyee and self.leave_type and self.from_date and self.to_date:
			# frappe.db.sql(""" select leave_type from 'tabLeave Type' WHERE employee = %s and leave_type = %s and from_date = %s and to_date = %s""",(self.em))

	def max_continuous_days(self):
		if self.employee and self.leave_type and self.from_date and self.to_date:
			max_continuous_days = frappe.db.sql("""select max_continuous_days_allowed from `tabLeave Type` WHERE employee = %s and leave_type = %s and from_date <= %s and to_date >= %s """,(self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
			if float(max_continuous_days) < float(self.total_leave_days):
				frappe.throw(_("You cann't select more than"+self.max_continuous_days()))


	def allow_negative_balance(self):
		try:
			check_allow_negative_balance = frappe.db.sql("SELECT allow_negative_balance from `tabLeave Type` WHERE `leave_type` = %s", self.leave_type)
			if check_allow_negative_balance:
				total_leave_days = date_diff(self.to_date, self.from_date)
				self.total_leave_days = total_leave_days + 1
		except Exception as e:
			frappe.log_error(f"Error in allow_negative_balance: {e}")

	def applicable_after(self):
		days_applicable_after = frappe.db.sql(""" select applicable_after from 'tabLeave Type' WHERE leave_type = %s """,self.leave_type)
		if date_diff(self.from_date,datetime.date.today())<days_applicable_after:
			frappe.throw("sorry! you must apply to this leave before "+days_applicable_after+" days")



