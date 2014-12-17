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
		pass



def multitenanct(from_test=False):
   frappe.errprint("creation site")
   res=frappe.db.sql("""select name from `tabSite Master` where flag=0 limit 1 """)
   frappe.errprint(res)
   if res:
        sites=''
        sites = frappe.db.sql("""select sites from  `tabUser` where name='administrator'""")
        #print sites
        auto_commit = not from_test
        ste=res[0][0]
        from frappe.utils import cstr
        import os
        import sys
        import subprocess
        import getpass
        import logging
        import json
        from distutils.spawn import find_executable
        from frappe.utils.email_lib import sendmail
        cwd='/home/indictrans/'
        cmd="./testenv.sh "+ste
        qr="select email_id__if_administrator from `tabSite Master` where name='"+ste+"'"
        rs=frappe.db.sql(qr)
        msg1="Hello , <br> your site is created . following are the details of your site <br> 'http://"+ste+"' <br> user name :-administrator<br> password :- admin<br>Regards,<br>Tailorpad.com"
        sendmail(rs[0][0], subject='Welcome to Tailorpad', msg = msg1)
        import subprocess
        frappe.errprint(cmd)
        #subprocess.call(['cd /home/indictrans/webapps/tailorpad/'])
        #pass
        sites=cstr(sites[0][0])+' '+ste
        frappe.db.sql("update `tabUser` set sites= %s where name='administrator'",sites)
        try:
                subprocess.check_call(cmd, cwd=cwd, shell=True)
        except subprocess.CalledProcessError, e:
                print "Error:", e.output
                raise
        nginx="""
                upstream frappe {
                server 192.168.0.104:7893 fail_timeout=0;
                }
                server {
                        listen 80 ;
                        client_max_body_size 4G;
                        server_name stich1.tailorpad.com stitch2.tailorpad.com %s;
                        keepalive_timeout 5;
                        sendfile on;
                        root /home/indictrans/webapps/tailorpad/frappe-bench/sites;
                        location /private/ {
                                internal;
                                try_files /$uri =424;
                        }
                        location /assets {
                                try_files $uri =404;
                        }

                        location / {
                                try_files /test/public/$uri @magic;
                        }

                        location @magic {
                                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                                proxy_set_header Host $host;
                                proxy_set_header X-Use-X-Accel-Redirect True;
                                proxy_read_timeout 120;
                                proxy_redirect off;
                                proxy_pass  http://frappe;
                        }
                }"""%(sites)
        #with open("/home/indictrans/webapps/tailorpad/frappe-bench/config/nginx.conf","w") as conf_file:
        #               conf_file.write(nginx)
        #cwd='/home/'
        #cmd='echo indictrans | sudo service nginx reload'
        #try:
        #       subprocess.check_call(cmd, cwd=cwd, shell=True)
        #except subprocess.CalledProcessError, e:
        #       print "Error:", e.output
        #       raise   
        from frappe.utils import nowdate,add_months,cint
        en_dt=add_months(nowdate(),1)
        qry="update `tabSite Master` set flag=1 ,expiry_date='"+en_dt+"' where name='"+cstr(res[0][0])+"'"
        #frappe.errprint(qry)
        frappe.db.sql(qry, auto_commit=auto_commit)
	import requests
        import json
	qry="select site_name,email_id__if_administrator,country from `tabSite Master` where name='"+cstr(ste)+"'"
	frappe.errprint(qry)
        pr1 = frappe.db.sql(qry)
        st=pr1 and pr1[0][0] or ''
        eml=pr1 and pr1[0][1] or ''
        cnt=pr1 and pr1[0][2] or ''
        frappe.get_doc({
                        "doctype":"SubAdmin Info",
                        "parent": "SUB0001",
                        "parentfield": "subadmins_information",
                        "parenttype":"Admin Details",
                        "admin": eml,
                        "site_name":ste
                }).insert()
	headers = {'content-type': 'application/x-www-form-urlencoded'}
        sup={'usr':'administrator','pwd':'admin'}
        url = 'http://'+st+'/api/method/login'
        response = requests.get(url, data=sup, headers=headers)
        if st.find('.')!= -1:
                 db=st.split('.')[0][:16]
        else:
                 db=st[:16]
        vldt={}
        vldt['country']=cnt
        vldt['email_id_admin']=eml
        url = 'http://'+st+'/api/resource/User/Administrator'
        frappe.errprint(url)
        frappe.errprint('data='+json.dumps(vldt))
        response = requests.put(url, data='data='+json.dumps(vldt), headers=headers)


def assign_support():
        frappe.errprint("assign suppoert tickets")
        from frappe.utils import get_url, cstr
        if get_url()=='http://stich1.tailorpad.com':
                check_entry = frappe.db.sql("""select name,raised_by from `tabSupport Ticket` where assign_to is null and raised_by is not null and status<>'Closed'""")
                frappe.errprint(check_entry)
                for name,raised_by in check_entry :
                        frappe.errprint([name,raised_by])
                        assign_to = frappe.db.sql("""select assign_to from `tabAssing Master` where name= %s""",raised_by)
                        #frappe.errprint(assign_to[0][0])
                        if assign_to :
                                aa="update `tabSupport Ticket` set assign_to='"+cstr(assign_to[0][0])+"' where name = '"+name+"'"
                                frappe.errprint(aa)
                                frappe.db.sql(aa)
                        else :
                                aa="update `tabSupport Ticket` set assign_to='Administrator' where name = '"+name+"'"
                                frappe.errprint(aa)
                                frappe.db.sql(aa)

def create_support():
        frappe.errprint("creating suppoert tickets")
        import requests
        import json
        pr2 = frappe.db.sql("""select site_name from `tabSubAdmin Info` """)
        for site_name in pr2:
                db_name=cstr(site_name[0]).split('.')[0]
                db_name=db_name[:16]
                abx="select name from `"+cstr(db_name)+"`.`tabSupport Ticket` where flag='false'"
                #frappe.errprint(abx)
                pr3 = frappe.db.sql(abx)
                #frappe.errprint(pr3)
                for sn in pr3:
                                login_details = {'usr': 'Administrator', 'pwd': 'admin'}
                                url = "http://"+cstr(site_name[0])+"/api/method/login"
                                headers = {'content-type': 'application/x-www-form-urlencoded'}
                                response = requests.post(url, data='data='+json.dumps(login_details), headers=headers)
                                #frappe.errprint("login in site")
                                frappe.errprint(response.text)
                                test = {}
                                url="http://"+cstr(site_name[0])+"/api/resource/Support Ticket/"+cstr(sn[0])
                                #frappe.errprint("fetching suppoert ticket")
                                response = requests.get(url)
                                #frappe.errprint(response.text)
                                support_ticket = eval(response.text).get('data')
                                del support_ticket['name']
                                del support_ticket['creation']
                                del support_ticket['modified']
                                del support_ticket['company']
                                url = "http://stich1.tailorpad.com/api/method/login"
                                #frappe.errprint("login in master for ticket creation")
                                response = requests.post(url, data='data='+json.dumps(login_details), headers=headers)
                                #frappe.errprint(response.text)
                                url = 'http://stich1.tailorpad.com/api/resource/Support Ticket'
                                response = requests.post(url, data='data='+json.dumps(support_ticket), headers=headers)
                                #frappe.errprint("create support ticket")
                                #frappe.errprint(response.text)
                                url="http://"+cstr(site_name[0])+"/api/resource/Support Ticket/"+cstr(sn[0])
                                support_ticket={}
                                #frappe.errprint()
                                support_ticket['flag']='True'
                                #frappe.errprint('data='+json.dumps(support_ticket))
                                response = requests.put(url, data='data='+json.dumps(support_ticket), headers=headers)
                                frappe.errprint("updated flag")

def create_feedback():
        frappe.errprint("creating feed back")
        import requests
        import json
        pr2 = frappe.db.sql("""select site_name from `tabSubAdmin Info`""")
        for site_name in pr2:
                #frappe.errprint(site_name)
                db_name=cstr(site_name[0]).split('.')[0]
                db_name=db_name[:16]
                abx="select name from `"+cstr(db_name)+"`.`tabFeed Back` where flag='false'"
                #frappe.errprint(abx)
                pr3 = frappe.db.sql(abx)
                #frappe.errprint(pr3)
                for sn in pr3:
                                login_details = {'usr': 'Administrator', 'pwd': 'admin'}
                                url = "http://"+cstr(site_name[0])+"/api/method/login"
                                headers = {'content-type': 'application/x-www-form-urlencoded'}
                                response = requests.post(url, data='data='+json.dumps(login_details), headers=headers)
                                #frappe.errprint(response.text)
                                test = {}
                                url="http://"+cstr(site_name[0])+"/api/resource/Feed Back/"+cstr(sn[0])
                                response = requests.get(url)
                                #frappe.errprint(response.text)
                                support_ticket = eval(response.text).get('data')
                                del support_ticket['name']
                                del support_ticket['creation']
                                del support_ticket['modified']
                                #del support_ticket['company']
                                url = "http://stich1.tailorpad.com/api/method/login"
                                response = requests.post(url, data='data='+json.dumps(login_details), headers=headers)
                                frappe.errprint(response.text)
                                url = 'http://stich1.tailorpad.com/api/resource/Feed Back'
                                response = requests.post(url, data='data='+json.dumps(support_ticket), headers=headers)
                                frappe.errprint("create support ticket")
                                url="http://"+cstr(site_name[0])+"/api/resource/Feed Back/"+cstr(sn[0])
                                support_ticket={}
                                support_ticket['flag']='True'
                                frappe.errprint('data='+json.dumps(support_ticket))
                                response = requests.put(url, data='data='+json.dumps(support_ticket), headers=headers)


def add_validity():
                frappe.errprint("in add validity function")
                import requests
                import json
                from frappe.utils import nowdate, cstr,cint, flt, now, getdate, add_months
                pr1 = frappe.db.sql("""select site_name from `tabSite Master` """)
                for pr in pr1:
                        if pr[0].find('.')!= -1:
                                db=pr[0].split('.')[0][:16]
                        else:
                                db=pr[0][:16]
                        qry="select validity from `"+cstr(db)+"`.`tabUser` where name='administrator' and validity>0 "
                        #print qry
                        frappe.errprint(qry)
                        pp1 = frappe.db.sql(qry)
                        if pp1 :
                                headers = {'content-type': 'application/x-www-form-urlencoded'}
                                sup={'usr':'administrator','pwd':'admin'}
                                url = 'http://'+pr[0]+'/api/method/login'
                                response = requests.get(url, data=sup, headers=headers)
                                qry1="select name from `"+cstr(db)+"`.`tabUser` where validity_end_date <CURDATE()"
                                pp2 = frappe.db.sql(qry1)
                                for pp in pp2:
                                        dt=add_months(getdate(nowdate()), cint(pp1[0][0]))
                                        vldt={}
                                        vldt['validity_start_date']=cstr(nowdate())
                                        vldt['validity_end_date']=cstr(dt)
                                        url = 'http://'+pr[0]+'/api/resource/User/'+cstr(name)
                                        response = requests.put(url, data='data='+json.dumps(vldt), headers=headers)
                                qry2="select name,validity_end_date from `"+cstr(db)+"`.`tabUser` where validity_end_date >=CURDATE()"
                                pp3 = frappe.db.sql(qry2)
                                for name,validity_end_date in pp3:
                                        dt=add_months(getdate(validity_end_date), cint(pp1[0][0]))
                                        vldt={}
                                        vldt['validity_end_date']=cstr(dt)
                                        url = 'http://'+pr[0]+'/api/resource/User/'+cstr(name)
                                        response = requests.put(url, data='data='+json.dumps(vldt), headers=headers)
                                vldt={}
                                vldt['validity']='0'
                                url = 'http://'+pr[0]+'/api/resource/User/administrator'
                                response = requests.put(url, data='data='+json.dumps(vldt), headers=headers)

def disable_user():
        frappe.errprint("in disable user ")
        import requests
        import json
        pr2 = frappe.db.sql("""select site_name from `tabSubAdmin Info`""")
        for site_name in pr2:
                db_name=cstr(site_name[0]).split('.')[0]
                db_name=db_name[:16]
                abx="select name from `"+cstr(db_name)+"`.`tabUser` where validity_end_date<=CURDATE()"
                pr3 = frappe.db.sql(abx)
                for sn in pr3:
                                headers = {'content-type': 'application/x-www-form-urlencoded'}
                                sup={'usr':'administrator','pwd':'admin'}
                                url = 'http://'+cstr(site_name[0])+'/api/method/login'
	                        response = requests.get(url, data=sup, headers=headers)
                                url="http://"+cstr(site_name[0])+"/api/resource/User/"+cstr(sn[0])
                                support_ticket={}
                                support_ticket['enabled']=0
                                response = requests.put(url, data='data='+json.dumps(support_ticket), headers=headers)
                                                                                                                       
