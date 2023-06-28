import frappe
from frappe import _
import requests
from frappe.desk.reportview import get_form_params
from frappe.desk.reportview import get_count as get_filtered_count
from frappe.core.doctype.user.user import generate_keys
from frappe.utils import logger

logger.set_log_level("DEBUG")
logger = frappe.logger("custom_apis", allow_site=True, file_count=2)



import frappe


@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
        
        user = frappe.get_doc("User", usr)
        api_secret = generate_keys(user.name)
        api_key = frappe.generate_hash(length=15)
        user.api_secret = api_secret
        user.api_key = api_key
        

        
        frappe.response["message"] = {
            "success_key": 1,
            "message": "Authentication success",
            "sid": frappe.session.sid,
            "api_key": api_key,
            "api_secret": api_secret,
            "username": user.username,
            "email": user.email,
        }
        user.insert(ignore_permissions=True)
        user.save()
        frappe.db.commit()        
        
        
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["message"] = {
            "success_key": 0,
            "message": "Authentication Error!",
        }

        return



# def generate_keys(user):
#     user_details = frappe.get_doc("User", user)
#     api_secret = frappe.generate_hash(length=15)

#     if not user_details.api_key:
#         api_key = frappe.generate_hash(length=15)
#         user_details.api_key = api_key
#     else:
#         api_key = user_details.api_key
#     user_details.api_secret = api_secret
#     user_details.save()
#     frappe.db.commit()

#     return api_secret, api_key


@frappe.whitelist(allow_guest=True)
def register_user(email, password, first_name, last_name, birth_date, gender, role, mobile_no):
    try:
        # Perform user registration
        user = frappe.new_doc("User")
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.birth_date = birth_date
        user.gender = gender
        user.new_password = password
        user.mobile_no = mobile_no
        user.send_welcome_email = 0
        user.append("roles", {"role": role})
        user.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.response["message"] = {
            "success": True,
            "message": "User registered successfully.",
            "username": user.name,
            "password": password,
        }
        
    except frappe.exceptions.ValidationError as e:
        frappe.response["message"] = {
            "success": False,
            "message": _("Registration failed. {0}").format(e.message)
        }
    
    logger.info(f"register_user :: \n {frappe.response} \n")

    return




@frappe.whitelist()
def get_list_docs():
    args = get_form_params()
    docs = frappe.get_list(**args)

    frappe.local.form_dict.pop("limit_page_length", None)

    return {
        "docs": docs,
        "length": get_filtered_count(),
    }
    
    
