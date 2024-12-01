import re
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValueError("يرجى إدخال بريد إلكتروني صحيح.")

def validate_phone_number(phone_number):
    phone_regex = r'^05\d{8}$'
    if not re.match(phone_regex, phone_number):
        raise ValueError("يرجى إدخال رقم جوال سعودي صحيح (يبدأ بـ 05 ومكون من 10 أرقام).")
    

def validate_complaint(complaint_text):
    # التحقق من النص غير فارغ وطوله كافٍ
    if not complaint_text or len(complaint_text.strip()) < 10:
        raise ValueError("نص الشكوى يجب أن يحتوي على 10 أحرف على الأقل.")
    
    # التحقق من استخدام الحروف العربية فقط
    if not re.match(r'^[\u0600-\u06FF\s\d]+$', complaint_text.strip()) or complaint_text.strip().isdigit():
        raise ValueError("الرجاء استخدام الحروف العربية فقط.")
