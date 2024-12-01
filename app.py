from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from Python.forms import LoginForm,RegisterForm,Decision
from flask_migrate import Migrate
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_migrate import Migrate
import traceback
from flask import session
from Python.prepar import remove_repeating_char, remove_symbols, removenonarabic, give_emoji_free_Ticket, stopwordremoval ,normalize ,remove_spaces_arabic,remove_numbers 
from Python.Validate import validate_email , validate_phone_number ,validate_complaint
import pandas as pd
import dill
import torch
import os
import re




# Initialize Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Renad0409@localhost/922_platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '922PlatformsseniorProject'

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text



# Initialize database, bcrypt, and login manager

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


with app.app_context():
    result = db.session.execute(text('SELECT DATABASE();'))
    print("Connected to database:", result.scalar())




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    id_number = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    region = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    complaint_text = db.Column(db.Text, nullable=False)
    authority = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default="جديدة")  # Defult state 
    Replay_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())


@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return db.session.get(User, int(user_id))




migrate = Migrate(app, db)

# try:
#     Matokenizer = AutoTokenizer.from_pretrained('Balanced-MARBERT')
#     Mamodel = AutoModelForSequenceClassification.from_pretrained('Balanced-MARBERT')
# except Exception as e:
#     print("Error loading Balanced-MARBERT model or tokenizer:", e)

    
# Load model and tokenizer
try:
    with open('Model/SEVERITY_CLASSIFICATION_MODEL.pkl', 'rb') as file:
        data = dill.load(file)
        model = data['model']
        tokenizer = data['tokenizer']
        authority_mapping = data['authority_mapping']
        high_severity_keywords = data['high_severity_keywords']
        medium_severity_keywords = data['medium_severity_keywords']
        low_severity_keywords = data['low_severity_keywords']
except Exception as e:
    print("Error loading models or tokenizer:", e)


import pickle
import torch
from transformers import AutoTokenizer

try:
    # Load the model and tokenizer from the pickle file
    with open('Model/arabert_model_with_tokenizer.pkl', 'rb') as file:
        data = pickle.load(file)
        model_ara = data['model']  # Load the model
        tokenizer_ara = data['tokenizer']  # Load the tokenizer

    # Ensure the model is moved to the CPU and set to evaluation mode
    model_ara.to(torch.device('cpu'))
    model_ara.eval()  # Evaluation mode disables dropout and other training-specific behaviors

    print("AraBERT model and tokenizer loaded successfully.")# Define label-to-category mapping

    label_to_category = {
    0: "بلاغ غير معالج",
    1: "شكاوى الأسواق",
    2: "شكاوى البناء والتعمير",
    3: "شكاوى البنوك والخدمات المصرفية",
    4: "شكاوى الحدائق والمرافق العامة",
    5: "شكاوى الخدمات العامة",
    6: "شكاوى الخدمات اللوجستية والشحن",
    7: "شكاوى السداد والحسابات",
    8: "شكاوى السلامة والنظافة العامة",
    9: "شكاوى الصيانة والبنية التحتية",
    10: "شكاوى العروض الوهمية والمخالفة",
    11: "شكاوى الغش التجاري",
    12: "شكاوى القروض وشركات التمويل",
    13: "شكاوى المؤسسات التجارية",
    14: "شكاوى المتاجر الإلكترونية",
    15: "شكاوى المستهلكين",
    16: "شكاوى النقل البحري",
    17: "شكاوى النقل البري",
    18: "شكاوى خدمات ما بعد البيع",
    19: "شكاوى شركات التأمين",
    20: "شكاوى شركات التقنية المالية والمدفوعات",
    21: "طلبات السجلات التجارية",
    }

    
except Exception as e:
    print("Error loading AraBERT model or tokenizer:", e)

# إعداد النصوص
def preparedatasets(Ticket):
    if pd.notna(Ticket):  # التأكد من أن النص ليس NaN
        Ticket = normalize(Ticket)  # توحيد النصوص
        Ticket = stopwordremoval(Ticket)  # إزالة الكلمات التوقف
        Ticket = give_emoji_free_Ticket(Ticket)  # إزالة الرموز التعبيرية
        Ticket = removenonarabic(Ticket)  # إزالة الأحرف غير العربية
        Ticket = remove_symbols(Ticket)  # إزالة الرموز
        Ticket = remove_repeating_char(Ticket)   
        Ticket = remove_spaces_arabic(Ticket)
        Ticket = remove_numbers(Ticket)
        return Ticket

# Helper functions
def classify_authority(text):
    
    print(text)
    
    # Tokenize the input text for Balanced-MARBERT
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128) 
    print(inputs)
    # Pass the inputs through the Balanced-MARBERT model
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the index of the predicted authority
    
    outputs.logits
    authority_index = torch.argmax(outputs.logits, dim=1).item()
    
    authority_mapping = {
            0: 'الهيئة العامة للنقل',
            1: 'ساما',
            2: 'وزارة التجارة',
            3: 'وزارة الشؤون البلدية والقروية والإسكان'
        }
    # Map the index to the corresponding authority name
    return authority_mapping.get(authority_index, "Unknown")

def determine_severity(text):
    if any(word in text for word in high_severity_keywords):
        return "مرتفع"
    elif any(word in text for word in medium_severity_keywords):
        return "متوسط"
    elif any(word in text for word in low_severity_keywords):
        return "منخفض"
    else:
        return "منخفض"
    
def determain_specialization(text):
    try:
        # Tokenize the input text
        inputs = tokenizer_ara(text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
        
        # Get predictions
        with torch.no_grad():
            outputs = model_ara(**inputs)
        
        # Get the predicted category index
        predicted_class = torch.argmax(outputs.logits, dim=1).item()
        
        # Map the index to the category
        predicted_category = label_to_category.get(predicted_class, "Unknown")
        
        return predicted_category
    except Exception as e:
        print("Error during specialization classification:", e)
        return "Unknown"


# Routes# Routes
@app.route('/predict', methods=['POST'])
def predict():
    
    try:
        # استلام البيانات من الطلب
        data = request.get_json()
        text = data.get('complaint', "").strip()
        email = data.get('email', "").strip()
        phone_number = data.get('phone', "").strip()


        print("Complaint:", text)
        print("Email:", email)
        print("Phone:", phone_number)
        
        try:
            validate_email(email)
            validate_phone_number(phone_number)
            validate_complaint(text)
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        
        
        
        # تجهيز النصوص وتحليلها
        prepared_text = preparedatasets(text)
        print(prepared_text)
        predicted_authority = classify_authority(prepared_text)
        predicted_severity = determine_severity(prepared_text)
        predicted_specialization = determain_specialization(text)

        # تخزين البيانات في الجلسة
        session['new_ticket_data'] = {
            'complaint_text': text,
            'predicted_authority': predicted_authority,
            'predicted_severity': predicted_severity,
            'predicted_specialization': predicted_specialization,
            'region': current_user.region,
            'city': current_user.city,
            'email': email,
            'phone': phone_number,
            'user_id': current_user.id
        }
        
        print("Data stored in session:", session['new_ticket_data'])

        return jsonify({
            "authority": predicted_authority,
            "severity": predicted_severity,
            "specialization": predicted_specialization,
        })
        


    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "حدث خطأ أثناء معالجة الطلب.", "details": str(e)}), 500

# مسار لتأكيد رفع التذكرة
@app.route('/confirm_ticket', methods=['POST'])
@login_required
def confirm_ticket():
    decision_form = Decision()

    if decision_form.validate_on_submit():
        if decision_form.submit.data:  # إذا تم النقر على "موافق"
            ticket_data = session.get('new_ticket_data')
            if not ticket_data:
                flash('لا توجد بيانات تذكرة لتأكيدها.', 'danger')
                return redirect(url_for('fileticketPage'))

            new_ticket = Ticket(
                user_id=ticket_data['user_id'],
                complaint_text=ticket_data['complaint_text'],
                authority=ticket_data['predicted_authority'],
                severity=ticket_data['predicted_severity'],
                specialization=ticket_data['predicted_specialization'],
                email=ticket_data['email'],
                phone=ticket_data['phone'],
                region=ticket_data['region'],
                city=ticket_data['city']
            )
            db.session.add(new_ticket)
            db.session.commit()
            session.pop('new_ticket_data', None)
            flash('تم تأكيد التذكرة بنجاح. يمكنك الآن تتبعها.', 'success')
            return redirect(url_for('fileticketPage'))

        elif decision_form.reject.data:  # إذا تم النقر على "رفض"
            session.pop('new_ticket_data', None)  # حذف البيانات
            flash('تم رفض التذكرة.', 'info')
            return redirect(url_for('fileticketPage'))

    flash('حدث خطأ أثناء معالجة القرار.', 'danger')
    return redirect(url_for('fileticketPage'))

@app.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(id_number=login_form.id_number.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            return redirect(url_for('homepage'))
        else:
            flash('بيانات تسجيل الدخول غير صحيحة.', 'danger')

    if register_form.validate_on_submit():
        if register_form.password.data != register_form.confirm_password.data:
            flash('كلمة المرور وتأكيدها لا يتطابقان.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
            new_user = User(
                first_name=register_form.first_name.data,
                last_name=register_form.last_name.data,
                id_number=register_form.id_number.data,
                password=hashed_password,
                mobile_number=register_form.mobile_number.data,
                region=register_form.region.data,
                city=register_form.city.data,
            )
            db.session.add(new_user)
            db.session.commit()
            flash('تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول.', 'success')
            return redirect(url_for('home'))

    return render_template('LoginSingupPage.html', login_form=login_form, register_form=register_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/track_ticket', methods=['GET', 'POST'])
@login_required
def track_ticket():
    user_data = {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }
    
    tickets = []
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        # استلام البيانات من نموذج البحث
        ticket_number = request.form.get('ticket_number')
        ticket_status = request.form.get('ticket_status')
        agency = request.form.get('agency')

        query = Ticket.query.filter(Ticket.user_id == current_user.id)  # قصر البحث على المستخدم الحالي
        errors = []
        if not ticket_number:
            errors.append("رقم التذكرة مطلوب.")
        elif not ticket_number.isdigit():
            errors.append("رقم التذكرة يجب أن يحتوي على أرقام فقط.")
            
        if ticket_number:
            query = query.filter(Ticket.id == ticket_number)
            
        if not ticket_status.isalpha():
            errors.append("حالة التذكرة يجب أن تحتوي على أحرف فقط.")

        if ticket_status:
            query = query.filter(Ticket.status.ilike(f"%{ticket_status}%"))
        if agency:
            query = query.filter(Ticket.authority.ilike(f"%{agency}%"))
        if errors:
            for error in errors:
                print(error, 'error')
        # تنفيذ الاستعلام
        tickets = query.all()

    return render_template('trackticket.html', tickets=tickets ,user_data=user_data)

@app.route('/ticket_details/<int:ticket_id>', methods=['GET'])
@login_required
def ticket_details(ticket_id):
    user_data = {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }
    ticket = Ticket.query.filter_by(id=ticket_id, user_id=current_user.id).first_or_404()
    return render_template('ticket_details.html', ticket=ticket, user_data=user_data)


@app.route('/922HomePage')
def homepage():
    user_data = {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }
    return render_template('Homepage.html', user_data=user_data)

@app.route('/fileTicketPage', methods=['GET', 'POST'])
@login_required
def fileticketPage():
    try:
        # بيانات المستخدم
        user_data = {
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "id_number": current_user.id_number,
            "mobile_number": current_user.mobile_number,
            "region": current_user.region,
            "city": current_user.city,
        }
        
        # إنشاء نموذج القرار
        decision_form = Decision()
        
        if request.method == 'POST':
            # عند تقديم الطلب POST
            flash('تم إنشاء التذكرة بنجاح. يمكنك الآن تتبع التذكرة في الصفحة المخصصة.', 'success')
            return render_template('fileticket.html', user_data=user_data, decision_form=decision_form)

        # عند الطلب GET
        return render_template('fileticket.html', user_data=user_data, decision_form=decision_form)
    
    except Exception as e:
        traceback.print_exc()
        flash('حدث خطأ أثناء معالجة الصفحة.', 'danger')
        print('حدث خطأ أثناء معالجة الصفحة.')
        return redirect(url_for('homepage'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)