import frappe
# from frappe.core.doctype.user.user import generate_keys

def generate_keys(user):
    user_details = frappe.get_doc("User", user)
    api_secret = frappe.generate_hash(length=15)

    if not user_details.api_key:
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
    else:
        api_key = user_details.api_key
    user_details.api_secret = api_secret
    user_details.save()
    frappe.db.commit()

    return api_secret, api_key

def user_generate_key(doc, method):
    # generate secret key and api key and save it to user
    if not doc.api_secret:
        generate_keys(doc.name)