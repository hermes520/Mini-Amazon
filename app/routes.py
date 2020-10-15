from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from app import app
from app import db
from app.forms import LoginForm, AddItemForm, AddtoCart
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Item, Cart


@app.route('/')
@app.route('/index')
def index():
    items = Item.query.all()
    return render_template("index.html", title='Home Page', items=items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, price=form.price.data, quantity=form.quantity.data)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html', title='Add Item', form=form)


def get_item(item_id):
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        flash("Item doesn't exist")
    return item


@app.route('/<id>/item', methods=['GET', 'POST'])
def item(id):
    item = get_item(id)
    form = AddtoCart()
    update_cart(item, form)
    if form.validate_on_submit():
        add_to_cart(item.id, form.item_quantity.data)
    return render_template('item.html', item=item, form=form)


def update_cart(item, form):
    quantity = item.quantity
    form.item_quantity.choices = [num for num in range(1, quantity+1)]


def add_to_cart(id, quantity):
    quantity = int(quantity)
    if Cart.query.filter_by(item_id=id, buyer_id=current_user.id).first() is not None:  # item already in cart
        cart = Cart.query.get((current_user.id, id))
        cart.cart_quantity += quantity
    else:
        cart = Cart(buyer_id=current_user.id, item_id=id, cart_quantity=quantity)
    db.session.add(cart)
    db.session.commit()
    flash('Successfully added {} item to cart'.format(quantity))
    return redirect(url_for('item', id=id))


@app.route('/<item_id>/delete_from_cart', methods=['GET', 'POST'])
def delete_from_cart(item_id):
    item = Cart.query.filter_by(item_id=item_id, buyer_id=current_user.id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = db.session.query(Cart, Item).join(Item,
                                                   (Cart.item_id == Item.id)).filter(Cart.buyer_id == current_user.id).all()
    price = total_price(cart_items)
    return render_template('cart.html', cart=cart_items, price=price)


def total_price(cart_items):
    sum_price = 0
    for i in cart_items:
        sum_price += (i.Item.price * i.Cart.cart_quantity)
    return sum_price