app_name = "erpnext"
app_title = "TailorPad"
app_publisher = "TailorPad and Contributors"
app_description = "Open Source Enterprise Resource Planning for Small and Midsized Organizations"
app_icon = "icon-th"
app_color = "#e74c3c"
app_version = "4.4.0"

error_report_email = "support@tailorpad.com"

app_include_js = ["assets/js/erpnext.min.js","assets/js/chart.js"]
app_include_css = "assets/css/erpnext.css"
web_include_js = "assets/js/erpnext-web.min.js"

after_install = "erpnext.setup.install.after_install"

boot_session = "erpnext.startup.boot.boot_session"
notification_config = "erpnext.startup.notifications.get_notification_config"

dump_report_map = "erpnext.startup.report_data_map.data_map"
update_website_context = "erpnext.startup.webutils.update_website_context"

on_session_creation = "erpnext.startup.event_handlers.on_session_creation"
before_tests = "erpnext.setup.utils.before_tests"

website_generators = ["Item Group", "Item", "Sales Partner"]

standard_queries = "Customer:erpnext.selling.doctype.customer.customer.get_customer_list"

permission_query_conditions = {
		"Feed": "erpnext.home.doctype.feed.feed.get_permission_query_conditions",
		"Note": "erpnext.utilities.doctype.note.note.get_permission_query_conditions"
	}

has_permission = {
		"Feed": "erpnext.home.doctype.feed.feed.has_permission",
		"Note": "erpnext.utilities.doctype.note.note.has_permission"
	}


doc_events = {
	"*": {
		"on_update": "erpnext.home.update_feed",
		"on_submit": "erpnext.home.update_feed"
	},
	"Comment": {
		"on_update": "erpnext.home.make_comment_feed"
	},

	"Stock Entry": {
		"on_submit": "erpnext.stock.doctype.material_request.material_request.update_completed_qty",
		"on_cancel": "erpnext.stock.doctype.material_request.material_request.update_completed_qty"
	},
	"User": {
		"validate": [
		"erpnext.hr.doctype.employee.employee.validate_employee_role",
		"erpnext.hr.doctype.employee.employee.validate_validity"
		],
		"on_update":[ 
		"erpnext.hr.doctype.employee.employee.update_user_permissions",
		"erpnext.hr.doctype.employee.employee.update_users"
		],
	},
	"Journal Voucher":{
		"on_submit": [
		"erpnext.setup.doctype.site_master.site_master.success_renewal",
		"erpnext.setup.doctype.site_master.site_master.on_success_renewal"
		],
	},
	"Feed Back":{
		"on_update": "erpnext.setup.doctype.site_master.site_master.feedback_submission"
	},
	"Support Ticket":{
		"on_update": "erpnext.setup.doctype.site_master.site_master.ticket_submission"
	}
}

scheduler_events = {
	"all": [
		"erpnext.support.doctype.support_ticket.get_support_mails.get_support_mails",
		"erpnext.hr.doctype.job_applicant.get_job_applications.get_job_applications",
		"erpnext.setup.doctype.site_master.site_master.multitenanct"
		
		
	],
	"daily": [
		"erpnext.controllers.recurring_document.create_recurring_documents",
		"erpnext.stock.utils.reorder_item",
		"erpnext.setup.doctype.email_digest.email_digest.send",
		"erpnext.support.doctype.support_ticket.support_ticket.auto_close_tickets",
		"erpnext.setup.doctype.site_master.site_master.before15_renewal_date",
		"erpnext.setup.doctype.site_master.site_master.before1_renewal_date",
		"erpnext.setup.doctype.site_master.site_master.on_renewal_date",
		"erpnext.setup.doctype.site_master.site_master.after1_exp_date",
		"erpnext.setup.doctype.site_master.site_master.on_grace_date",
		"erpnext.setup.doctype.site_master.site_master.after_grace_date",
		"erpnext.setup.doctype.site_master.site_master.lead_sales_followup",
		"erpnext.setup.doctype.site_master.site_master.promotional_follow",
		"erpnext.setup.doctype.site_master.site_master.after_deactivation",
	],
	"daily_long": [
		"erpnext.setup.doctype.backup_manager.backup_manager.take_backups_daily"
	],
	"weekly_long": [
		"erpnext.setup.doctype.backup_manager.backup_manager.take_backups_weekly"
	]
}

