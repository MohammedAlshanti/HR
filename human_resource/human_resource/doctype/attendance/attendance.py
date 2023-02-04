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

		# Add Grace period
		check_in = self.check_in
		check_out = self.check_out
		if (cint(settings.late_entry_grace_period) == 0 and cint(settings.early_exit_grace_period) == 0):
			check_in = self.check_in
			check_out = self.check_out
		elif (cint(settings.late_entry_grace_period) > 0 and cint(settings.early_exit_grace_period) == 0):
			check_in = get_time_str(
				to_timedelta(self.check_in) + timedelta(minutes=cint(settings.late_entry_grace_period)))
		elif (cint(settings.late_entry_grace_period) == 0 and cint(settings.early_exit_grace_period) > 0):
			# check_in = self.check_in
			# get_time_str(
			# 	to_timedelta(self.check_in) + timedelta(minutes=cint(settings.early_exit_grace_period)))
			check_out = get_time_str(
				to_timedelta(self.check_out) - timedelta(minutes=cint(settings.early_exit_grace_period)))
		else:
			check_in = get_time_str(
				to_timedelta(self.check_in) - timedelta(minutes=cint(settings.late_entry_grace_period)))
			check_out = get_time_str(
				to_timedelta(self.check_out) + timedelta(minutes=cint(settings.early_exit_grace_period)))

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


# def time_diff_in_hours(start, end):
# 	return round((end - start).total_seconds() / 3600, 1)

# def add_value_work_hours_and_late_hours(self):
# 	if self.employee and self.attendance_date and self.check_in and self.check_out:
# 		start_time = frappe.db.get_single_value('Attendance Settings', 'start_time')
# 		start_time = str(start_time)
# 		end_time = frappe.db.get_single_value('Attendance Settings', 'end_time')
# 		end_time = str(end_time)
# 		working_hours_threshold_for_absent = frappe.db.get_single_value('Attendance Settings', 'working_hours_threshold_for_absent')
# 		late_entry_grace_period = frappe.db.get_single_value('Attendance Settings', 'working_hours_threshold_for_absent')
# 		early_exit_grace_period = frappe.db.get_single_value('Attendance Settings', 'early_exit_grace_period')
# 		start = datetime.strptime(self.check_in, '%H:%M:%S')
# 		end = datetime.strptime(self.check_out, '%H:%M:%S')
#
# 		if datetime.strptime(self.check_in, '%H:%M:%S') ==  start and datetime.strptime(self.check_out, '%H:%M:%S')  == end:
# 			delta = end - start
# 			self.work_hours = delta.seconds / 3600
# 			self.late_hours = 0


# if datetime.strptime(self.check_in, '%H:%M:%S') <= datetime.strptime(start+datetime.strptime(timedelta(minutes=early_exit_grace_period)), '%H:%M:%S') and datetime.strptime(self.check_out, '%H:%M:%S')  == end:
# 	start = start_time
# 	delta = end - start
# 	self.work_hours = delta.seconds/3600
# 	self.late_hours = 0

# def update_status_value(self):
	# 	working_hours_threshold_for_absent = frappe.db.get_single_value('Attendance Settings', 'working_hours_threshold_for_absent')
	# 	if working_hours_threshold_for_absent > self.work_hours:
	# 		self.status = 'Absent'








