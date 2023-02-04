# Copyright (c) 2023, Mohammed Alshanti and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employeee(Document):

	def validate(self):
		self.validate_mobile()
		self.full_name_()
		self.validate_education()
		self.status_()

	def validate_mobile(self):
		if self.mobile:
			if len(self.mobile) == 10 and self.mobile.startswith('059'):
				pass
			else:
				frappe.throw("Invalid Mobile Number")

	def full_name_(self):
		if self.first_name and self.middle_name and self.last_name:
			self.full_name = self.first_name+" "+self.middle_name+" "+self.last_name

	def validate_education(self):
		if len (self.emplopyee_education) < 2:
			frappe.throw("required atleast 2 education levels")


	def status_(self):
		if self.status and self.age:
			if str(self.status) == 'Active' and self.age>=60:
				frappe.throw("You cann't added")




