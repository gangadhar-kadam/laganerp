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
    frappe.errprint("creation site -------------------------------- ")
    res=frappe.db.sql("""select name,client_name,email_id__if_administrator from `tabSite Master` where flag=0 limit 1 """)
    if res:
        sites=''
        sites = frappe.db.sql("""select sites from  `tabUser` where name='administrator'""")
        print sites
        print 'gangadharkadam'
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
        cwd='/home/gangadhar/Documents/gnkuper/frappe-bench/'
        print cwd
        cmd="./testenv.sh "+ste
        print cwd
        qr="select email_id__if_administrator,client_name from `tabSite Master` where name='"+ste+"'"
        rs=frappe.db.sql(qr)

        frappe.errprint("hello gangadhar")
        from frappe.utils.email_lib import sendmail
        etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='Successful first purchase'")
        #frappe.errprint(etemp)
        msg=etemp[0][1].replace('first_name',rs[0][1]).replace('user_name','administrator').replace('password','admin').replace('click here',ste)
        sendmail(rs[0][0], subject=etemp[0][0], msg = msg)

        #msg1="Hello "+res[0][1]+", <br> Welcome to TailorPad! <br> Thank you for showing interest. You can use the following link and credentials for trying TailorPad:<br> 'http://"+ste+"' <br> user name :-administrator<br> password :- admin<br>In case you need any more information about our product, please visit FAQ page or write to us on support@tailorpad.com, we will be glad to assist you.<br>Best Regards,<br>Team TailorPad"
        #sendmail(rs[0][0], subject='Welcome to Tailorpad', msg = msg1)
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
        print 'creating nginx'
        nginx="""
        upstream frappe {
        server 127.0.0.1:8000 fail_timeout=0;
        }
        server {
        listen 80 ;
        client_max_body_size 4G;
        server_name stich1.tailorpad.com %s;
        keepalive_timeout 5;
        sendfile on;
        root /home/gangadhar/Documents/gnkuper/frappe-bench/sites;

        location /private/ {
            internal;
            try_files /$uri =424;
        }

        location /assets {
            try_files $uri =404;
        }

        location / {
            try_files /stich1.tailorpad.com/public/$uri @magic;
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
        print nginx
        with open("/home/gangadhar/Documents/gnkuper/frappe-bench/config/nginx.conf","w") as conf_file:
                       conf_file.write(nginx)
        cwd='/home/'
        cmd='echo indictrans | sudo service nginx reload'
        print 'nginx reloading'
        try:
               subprocess.check_call(cmd, cwd=cwd, shell=True)
        except subprocess.CalledProcessError, e:
               print "Error:", e.output
               raise
        print "nginx reloaded"
        host="""
        127.0.0.1       localhost
        127.0.1.1       gangadhar-OptiPlex-360
        127.0.0.1       %s


        # The following lines are desirable for IPv6 capable hosts
        ::1     ip6-localhost ip6-loopback
        fe00::0 ip6-localnet
        ff00::0 ip6-mcastprefix
        ff02::1 ip6-allnodes
        ff02::2 ip6-allrouters
       	"""%(sites)
        print host
        with open("/home/gangadhar/Documents/gnkuper/frappe-bench/config/hosts","w") as hosts_file:
            hosts_file.write(host)
        print 'written hosts nin setup'
        os.system('echo indictrans | sudo -S cp /home/gangadhar/Documents/gnkuper/frappe-bench/config/hosts /etc/hosts')
        print "reloaded hosts hosts"
        from frappe.utils import nowdate,add_months,cint
        en_dt=add_months(nowdate(),1)
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
        item_code = frappe.db.sql("""select b.item_code from `tabSales Invoice` a, `tabSales Invoice Item` b where a.name=b.parent and a.customer=%s """, res[0][1])
        for ic in item_code:
			qr="select no_of_users,validity from `tabItem` where name = '"+cstr(ic[0])+"'"
			pro = frappe.db.sql(qr)
			frappe.errprint(pro)
			if (pro [0][0]== 0) and (pro[0][1]>0):
				frappe.errprint("0 and >0")
				vldt={}
				vldt['validity']=pro[0][1]
				vldt['country']=cnt
				vldt['email_id_admin']=eml
				url = 'http://'+st+'/api/resource/User/Administrator'
				frappe.errprint(url)
				frappe.errprint('data='+json.dumps(vldt))
				response = requests.put(url, data='data='+json.dumps(vldt), headers=headers)
				frappe.errprint("responce")
				frappe.errprint(response.text)
			elif (pro [0][0]>0 ) and (pro[0][1]==0):
				frappe.errprint(">0 and 0")
				vldtt={}
				vldtt['no_of_users']=pro[0][0]
				vldtt['country']=cnt
				vldtt['email_id_admin']=eml
				url = 'http://'+st+'/api/resource/User/Administrator'
				frappe.errprint(url)
				frappe.errprint('data='+json.dumps(vldtt))
				response = requests.put(url, data='data='+json.dumps(vldtt), headers=headers)
				frappe.errprint("responce")
				frappe.errprint(response.text)				
			elif (pro [0][0]> 0) and (pro[0][1]>0):
				frappe.errprint(" >0 and >0")
				user_val={}
				user_val['validity']=pro [0][1]
				user_val['user_name']=pro [0][0]
				user_val['flag']='false'
				url = 'http://'+st+'/api/resource/User Validity'
				frappe.errprint(url)
				frappe.errprint('data='+json.dumps(user_val))
				response = requests.post(url, data='data='+json.dumps(user_val), headers=headers)
				frappe.errprint("responce")
				frappe.errprint(response.text)		
			else:
				frappe.errprint("0 and 0")


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


def lead_sales_followup():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='Sales follow up'")
    qry="select lead_name,email_id,date(creation) from `tabLead` where DATEDIFF(curdate(),creation) <=64 and WEEKDAY(curdate())=0 and customer is null"
    res = frappe.db.sql(qry)
    for r in res:
        #frappe.errprint(r)
        msg=etemp[0][1].replace('first_name',r[0]).replace('act_date',cstr(r[2]))
        sendmail(r[1], subject=etemp[0][0], msg = msg)



def promotional_follow():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='Promotional Followup'")
    #frappe.errprint(etemp)
    qry="select lead_name,email_id,DATE_ADD(curdate(),INTERVAL 7 DAY) from `tabLead` where DATEDIFF(curdate(),creation) >=64 and WEEKDAY(curdate())=0 and customer is null"
    res = frappe.db.sql(qry)
    #frappe.errprint(res)
    for r in res:
        msg=etemp[0][1].replace('first_name',r[0]).replace('current_date+7',cstr(r[2]))
        sendmail(r[1], subject=etemp[0][0], msg = msg)


def success_renewal(doc,method):
    pass
    # from frappe.utils.email_lib import sendmail
    # #frappe.errprint("in success_renewal")
    # etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='Successful renewal'")
    # email_qry="select email_id__if_administrator from `tabSite Master` where client_name='"+doc.customer+"'"
    # #frappe.errprint(email_qry)
    # res=frappe.db.sql(email_qry)
    # #frappe.errprint(res[0][0])
    # date_query=frappe.db.sql("""select DATE_ADD(curdate(),INTERVAL 1 year)""")
    # #frappe.errprint(res)
    # #frappe.errprint(date_query[0][0])
    # if res:
    #     msg=etemp[0][1].replace('first_name',doc.customer).replace('sub_end_date',cstr(date_query[0][0]))
    #     #frappe.errprint(msg)
    #     sendmail(res[0][0], subject=etemp[0][0], msg = msg)

    

def ticket_submission(doc,method):
    from frappe.utils.email_lib import sendmail
    frappe.errprint("ticket submission")
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='Contact us, Feedback & Ticket submission'")
    #frappe.errprint(doc.name)
    #frappe.errprint(doc.customer)
    msg=etemp[0][1].replace('first_name',doc.customer).replace('ticket_number',doc.name)
    sendmail(doc.raised_by, subject=etemp[0][0], msg = msg)

def feedback_submission(doc,method):
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='Contact us, Feedback & Ticket submission'")
    query="select client_name from `tabSite Master` where email_id__if_administrator='"+doc.raised_by+"'"
    #frappe.errprint(query)
    res=frappe.db.sql(query)
    #frappe.errprint(res[0][0])
    msg=etemp[0][1].replace('first_name',res[0][0]).replace('ticket_number',doc.name)
    sendmail(doc.raised_by, subject=etemp[0][0], msg = msg)

def before15_renewal_date():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='15 days before renewal date'")
    query="select client_name,expiry_date,email_id__if_administrator from `tabSite Master`"
    res=frappe.db.sql(query)

    for r in res:
        qr="select datediff('"+cstr(r[1])+"',curdate())"
        #frappe.errprint(qr)
        diff=frappe.db.sql(qr)
        #frappe.errprint(diff[0][0])
        if(diff[0][0]==15):
            msg=etemp[0][1].replace('first_name',r[0]).replace('renewal date',cstr(r[1]))
            sendmail(r[2], subject=etemp[0][0], msg = msg)


def before1_renewal_date():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='1 Working day before renewal date'")
    query="select client_name,expiry_date,email_id__if_administrator from `tabSite Master`"
    res=frappe.db.sql(query)
    for r in res:
        qr="select datediff('"+cstr(r[1])+"',curdate())"
        #frappe.errprint(qr)
        diff=frappe.db.sql(qr)
        #frappe.errprint(diff[0][0])
        if(diff[0][0]==1):
            msg=etemp[0][1].replace('first_name',r[0]).replace('renewal date',cstr(r[1]))
            sendmail(r[2], subject=etemp[0][0], msg = msg)


def on_renewal_date():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='On renewal date'")
    query="select client_name,expiry_date,email_id__if_administrator from `tabSite Master`"
    res=frappe.db.sql(query)
    for r in res:
        qr="select datediff('"+cstr(r[1])+"',curdate())"
        #frappe.errprint(qr)
        diff=frappe.db.sql(qr)
        #frappe.errprint(diff[0][0])
        if(diff[0][0]==0):
            msg=etemp[0][1].replace('first_name',r[0]).replace('Date',cstr(r[1]))
            sendmail(r[2], subject=etemp[0][0], msg = msg)


def after1_exp_date():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='1 working day after expiry date'")
    query="select client_name,expiry_date,email_id__if_administrator from `tabSite Master`"
    res=frappe.db.sql(query)
    for r in res:
        qr="select datediff(curdate(),'"+cstr(r[1])+"')"
        #frappe.errprint(qr)
        diff=frappe.db.sql(qr)
        #frappe.errprint(diff[0][0])
        if(diff[0][0]==(-1)):
            msg=etemp[0][1].replace('first_name',r[0])
            sendmail(r[2], subject=etemp[0][0], msg = msg)

def on_grace_date():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='On 7th grace day'")
    query="select client_name,expiry_date,email_id__if_administrator from `tabSite Master`"
    res=frappe.db.sql(query)
    for r in res:
        qr="select datediff(curdate(),'"+cstr(r[1])+"')"
        #frappe.errprint(qr)
        diff=frappe.db.sql(qr)
        #frappe.errprint(diff[0][0])
        if(diff[0][0]==(-7)):
            msg=etemp[0][1].replace('first_name',r[0])
            sendmail(r[2], subject=etemp[0][0], msg = msg)

def after_grace_date():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='On grace period expiry'")
    query="select client_name,expiry_date,email_id__if_administrator from `tabSite Master`"
    res=frappe.db.sql(query)
    for r in res:
        qr="select datediff(curdate(),'"+cstr(r[1])+"')"
        #frappe.errprint(qr)
        diff=frappe.db.sql(qr)
        #frappe.errprint(diff[0][0])
        if(diff[0][0]==(-8)):
            msg=etemp[0][1].replace('first_name',r[0])
            sendmail(r[2], subject=etemp[0][0], msg = msg)

def after_deactivation():
    from frappe.utils.email_lib import sendmail
    etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='1 working day after deactivation'")
    query="select client_name,expiry_date,email_id__if_administrator from `tabSite Master`"
    res=frappe.db.sql(query)
    for r in res:
        qr="select datediff(curdate(),'"+cstr(r[1])+"')"
        #frappe.errprint(qr)
        diff=frappe.db.sql(qr)
        #frappe.errprint(diff[0][0])
        if(diff[0][0]==(-9)):
            msg=etemp[0][1].replace('first_name',r[0]).replace('Expiry date',cstr(r[1]))
            sendmail(r[2], subject=etemp[0][0], msg = msg)


def on_success_renewal(doc,method):
    pass
    # from frappe.utils.email_lib import sendmail
    # #frappe.errprint("in on success_renewal no 2")
    # etemp=frappe.db.sql("select subject,message from `tabTemplate Types` where name='On successful renewal'")
    # query="select name from `tabSales Invoice` where customer='"+doc.customer+"'"
    # res=frappe.db.sql(query)
    # if(res[0][0]):
    #     email_qry="select email_id__if_administrator from `tabSite Master` where client_name='"+doc.customer+"'"
    #     email_result=frappe.db.sql(email_qry)
    #     date=frappe.db.sql("select DATE_ADD(curdate(),INTERVAL 1 year)")
    #     msg=etemp[0][1].replace('first_name',doc.customer).replace('expiry_date',cstr(date[0][0]))
    #     if email_result:
    #         sendmail(email_result[0][0], subject=etemp[0][0], msg = msg)








            





        

    









                                                                                                                       
