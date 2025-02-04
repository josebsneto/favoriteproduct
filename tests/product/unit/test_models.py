def test_equals_products(get_product):
    product_a = get_product()
    product_b = get_product()
    product_b.title = "other_title"
    product_a.brand = "other_brand"

    assert product_a == product_b
    assert hash(product_a) == hash(product_b)
