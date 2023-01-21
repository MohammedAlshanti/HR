# Copyright (c) 2023, Mohammed Alshanti and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class Employeee(Document):
	def validate_mobile(self):
		if self.mobile:
			if len(self.mobile) == 10 and self.mobile.startswith('059'):
				pass
			else:
				frappe.throw("Invalid Mobile Number")

	def full_name(self):
		self.full_name = self.first_name+" "+self.middle_name+" "+self.last_name

	def validate_education(self):
		if self.emplopyee_education < 2:
			frappe.throw("required atleast 2 education levels")


	def status(self):
		if self.status == "Active" and self.age>=60:
			frappe.throw("You cann't added")




