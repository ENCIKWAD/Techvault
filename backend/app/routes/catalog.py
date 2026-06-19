from flask import Blueprint, request, jsonify
from ..services.catalog_service import CatalogService

catalog_bp = Blueprint('catalog', __name__, url_prefix='/api/catalog')

@catalog_bp.route('/products', methods=['GET'])
def get_products():
    products = CatalogService.get_all_products()
    return jsonify([dict(p) for p in products])

@catalog_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = CatalogService.get_product(product_id)
    if product:
        return jsonify(dict(product))
    return jsonify({'error': 'Product not found'}), 404

@catalog_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = CatalogService.get_categories()
    return jsonify([dict(c) for c in categories])

@catalog_bp.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    products = CatalogService.get_products_by_category(category_id)
    return jsonify([dict(p) for p in products])

# Admin endpoints - Create/Update/Delete products
@catalog_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category_id = data.get('category_id')
    stock = data.get('stock')

    if not all([name, description, price is not None, category_id, stock is not None]):
        return jsonify({'error': 'Missing required fields'}), 400

    product_id = CatalogService.create_product(name, description, price, category_id, stock)
    if product_id:
        product = CatalogService.get_product(product_id)
        return jsonify({'success': True, 'product': dict(product)}), 201
    return jsonify({'error': 'Failed to create product'}), 400

@catalog_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    success = CatalogService.update_product(product_id, data)
    if success:
        product = CatalogService.get_product(product_id)
        return jsonify({'success': True, 'product': dict(product)})
    return jsonify({'error': 'Product not found'}), 404

@catalog_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    success = CatalogService.delete_product(product_id)
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'Product not found'}), 404
