// Copyright (c) 2023, Mohammed Alshanti and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employeee', {
	validate(frm) {
    if (frm.doc.date_of_birth >= frappe.datetime.get_today()) {
     frappe.throw('You can not select date of birth after today');
    }
    var emp_dob = moment (frappe.datetime.now_date());
    var current_date = moment(frm.doc.date_of_birth);
    frm .doc.age =  emp_dob.year()- current_date.year();
}
});
