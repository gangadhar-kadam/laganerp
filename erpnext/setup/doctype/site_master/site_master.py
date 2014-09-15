# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, cstr
import os
import sys
import subprocess
import getpass
import logging
import json
from distutils.spawn import find_executable


class SiteMaster(Document):
	def on_update(self):
		   frappe.errprint("creation site")
		   res=frappe.db.sql("""select name from `tabSite Master` where flag=0 limit 1 """)
		   frappe.errprint(res)
		   if res:
			sites=''
			sites = frappe.db.sql("""select sites from  `tabUser` where name='administrator'""")
			#print sites
			#auto_commit = not from_test
			ste=res[0][0]
			from frappe.utils import cstr  
			import os
			import sys
			import subprocess
			import getpass
			import logging
			import json
			from distutils.spawn import find_executable
			cwd= '/home/gangadhar/workspace/smarttailor/frappe-bench/'
		        cmd='bench new-site '+ste
			frappe.errprint("created new site")
			sites=cstr(sites[0][0])+' '+ste
			#print sites
			frappe.db.sql("update `tabUser` set sites= %s where name='administrator'",sites)
		    	try:
				subprocess.check_call(cmd, cwd=cwd, shell=True)
			except subprocess.CalledProcessError, e:
				print "Error:", e.output
				raise
		    	cmd='bench frappe --install_app erpnext '+ste              
		    	try:
				subprocess.check_call(cmd, cwd=cwd, shell=True)
			except subprocess.CalledProcessError, e:
				print "Error:", e.output
				raise
		    	cmd='bench frappe --install_app shopping_cart '+ste             
		    	try:
				subprocess.check_call(cmd, cwd=cwd, shell=True)
			except subprocess.CalledProcessError, e:
				print "Error:", e.output
				raise
