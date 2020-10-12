from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AddItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    price = DecimalField('Item Price', validators=[DataRequired()], places=2)
    quantity = IntegerField('Item Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Item')


class AddtoCart(FlaskForm):
    item_quantity = SelectField(u'quantity')
    submit = SubmitField('Add to Cart')

