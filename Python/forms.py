from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired ,ValidationError



# Forms
class LoginForm(FlaskForm):
    id_number = StringField(validators=[
        InputRequired(), Length(min=10, max=10)], render_kw={"placeholder": "رقم الهوية"})
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "كلمة المرور"})
    submit = SubmitField('تسجيل الدخول')




class RegisterForm(FlaskForm):

    first_name = StringField(
        validators=[InputRequired(), Length(min=2, max=20)], render_kw={"placeholder": "الاسم الأول"})
    last_name = StringField(
        validators=[InputRequired(), Length(min=2, max=20)], render_kw={"placeholder": "الاسم الأخير"})
    id_number = StringField(
        validators=[InputRequired(), Length(min=10, max=10)], render_kw={"placeholder": "رقم الهوية"})
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "كلمة المرور"})
    confirm_password = PasswordField(
        validators=[InputRequired(), EqualTo('password')], render_kw={"placeholder": "تأكيد كلمة المرور"})
    mobile_number = StringField(
        validators=[InputRequired(), Length(10)], render_kw={"placeholder": "رقم الجوال"})
    region = StringField(render_kw={"placeholder": "المنطقة"})
    city = StringField(render_kw={"placeholder": "المدينة"})
    submit = SubmitField('إنشاء حساب')

    
    def validate_id_number(self, id_number):
        if not id_number.data.isdigit():
            raise ValidationError("رقم الهوية يجب أن يحتوي على أرقام فقط")

    def validate_mobile_number(self, mobile_number):
        if not mobile_number.data.isdigit():
            raise ValidationError("رقم الجوال يجب أن يحتوي على أرقام فقط")

class Decision(FlaskForm):
    submit = SubmitField('موافق')
    reject = SubmitField('رفض')
