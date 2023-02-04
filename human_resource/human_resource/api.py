import frappe

@frappe.whitelist()
def create_attendance(attendance_date, check_in, check_out):
	document_data = {
		"attendance_date": attendance_date,
		"check_in": check_in,
		"check_out": check_out,
}


