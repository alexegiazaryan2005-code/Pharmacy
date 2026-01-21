from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Product, Category

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Главная страница"""
    products_count = Product.query.count()
    categories_count = Category.query.count()

    low_stock = Product.query.filter(Product.quantity < 10).count()

    return render_template('index.html',
                           products_count=products_count,
                           categories_count=categories_count,
                           low_stock=low_stock)


@main.route('/products')
def products():
    """Список всех товаров"""
    search = request.args.get('search', '')

    if search:
        products_list = Product.query.filter(Product.name.contains(search)).all()
    else:
        products_list = Product.query.all()

    categories = Category.query.all()

    return render_template('products.html',
                           products=products_list,
                           categories=categories,
                           search=search)


@main.route('/categories')
def categories():
    """Список категорий"""
    categories_list = Category.query.all()
    return render_template('categories.html', categories=categories_list)


@main.route('/api/products')
def api_products():
    """API для получения товаров (JSON)"""
    products_list = Product.query.all()

    result = []
    for product in products_list:
        result.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'category': product.category.name if product.category else 'Без категории',
            'manufacturer': product.manufacturer
        })

    return jsonify(result)


@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """Добавление нового товара"""
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        price = float(request.form.get('price'))
        quantity = int(request.form.get('quantity'))
        category_id = int(request.form.get('category_id'))
        manufacturer = request.form.get('manufacturer')
        barcode = request.form.get('barcode')

        # Создаем новый товар
        new_product = Product(
            name=name,
            price=price,
            quantity=quantity,
            category_id=category_id,
            manufacturer=manufacturer,
            barcode=barcode
        )

        # Сохраняем в базу данных
        db.session.add(new_product)
        db.session.commit()

        flash('Товар успешно добавлен!', 'success')
        return redirect(url_for('main.products'))

    # Если GET запрос - показываем форму
    categories_list = Category.query.all()
    return render_template('add_product.html', categories=categories_list)


@main.route('/add_category', methods=['GET', 'POST'])
def add_category():
    """Добавление новой категории"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        new_category = Category(name=name, description=description)
        db.session.add(new_category)
        db.session.commit()

        flash('Категория успешно добавлена!', 'success')
        return redirect(url_for('main.categories'))

    return render_template('add_category.html')