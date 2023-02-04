# Copyright (c) 2023, Mohammed Alshanti and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	time_diff_in_seconds,
	time_diff_in_hours,
	cint,
	get_time_str,
	to_timedelta,
)
from datetime import datetime, timedelta

class Attendance(Document):
	def on_submit(self):
		self.add_value_work_hours_and_late_hours()



	def add_value_work_hours_and_late_hours(self, is_validate=False):
		status = "Present"
		req_hours = 0
		late_hours = 0
		settings = frappe.get_single("Attendance Settings")
		working_hours_threshold_for_absent = cint(
			settings.working_hours_threshold_for_absent
		)

		# late_entry_grace_period = 30
		# early_exit_grace_period = 15
		status = "Present"
		req_hours = 0
		late_hours = 0
		settings = frappe.get_single("Attendance Settings")
		working_hours_threshold_for_absent = int(settings.working_hours_threshold_for_absent)

		# Add Grace period
		check_in = self.check_in
		check_out = self.check_out
		if (int(settings.late_entry_grace_period) == 0 and int(settings.early_exit_grace_period) == 0):
			check_in = self.check_in
			check_out = self.check_out
			working_hours = time_diff_in_hours(check_out, check_in)
		elif (int(settings.late_entry_grace_period) > 0 and int(settings.early_exit_grace_period) == 0):
			check_in = get_time_str(to_timedelta(self.check_in) - timedelta(minutes=settings.late_entry_grace_period))
			working_hours = time_diff_in_hours(check_out, check_in)
		elif (int(settings.late_entry_grace_period) == 0 and int(settings.early_exit_grace_period) > 0):
			check_out = get_time_str(to_timedelta(self.check_out) + timedelta(minutes=settings.early_exit_grace_period))
			working_hours = time_diff_in_hours(check_out, check_in)
		else:
			check_in = get_time_str(to_timedelta(self.check_in) - timedelta(minutes=settings.late_entry_grace_period))
			check_out = get_time_str(to_timedelta(self.check_out) + timedelta(minutes=settings.early_exit_grace_period))
			working_hours = time_diff_in_hours(check_out, check_in)


		if settings.start_time and settings.end_time:
			req_hours = time_diff_in_hours(settings.end_time, settings.start_time)

		if req_hours > 0 and req_hours > working_hours:
			late_hours = req_hours - working_hours

		if working_hours < working_hours_threshold_for_absent:
			status = "Absent"


		if is_validate:
			self.work_hours = working_hours
			self.late_hours = late_hours
			self.status = status
		else:
			self.db_set("work_hours", working_hours)
			self.db_set("late_hours", late_hours)
			self.db_set("status", status)







