from ..data_access.product_repository import ProductRepository

class CatalogService:
    @staticmethod
    def get_all_products():
        return ProductRepository.get_all_products()

    @staticmethod
    def get_product(product_id):
        return ProductRepository.get_product_by_id(product_id)

    @staticmethod
    def get_products_by_category(category_id):
        return ProductRepository.get_products_by_category(category_id)

    @staticmethod
    def get_categories():
        return ProductRepository.get_all_categories()

    @staticmethod
    def update_product(product_id, data):
        return ProductRepository.update_product(product_id, data)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete_product(product_id)
