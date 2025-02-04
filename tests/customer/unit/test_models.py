from app.customer.models import Customer


def test_create_customer_empty_products(get_customer):
    customer = Customer(email="a_email", name="a_name")
    assert isinstance(customer, Customer)
    assert isinstance(customer.product_ids, list)


def test_equals_customers(get_customer):
    customer_a = get_customer()
    customer_b = get_customer()
    customer_b.name = "other name"

    assert customer_a == customer_b
    assert hash(customer_a) == hash(customer_b)


def test_add_customer_product(get_customer):
    customer = get_customer()
    assert len(customer.product_ids) == 2
    customer.add_product("as33f2r2")
    assert len(customer.product_ids) == 3


def test_not_add_same_customer_product(get_customer):
    customer = get_customer()
    assert len(customer.product_ids) == 2
    customer.add_product("dh1be31595")
    assert len(customer.product_ids) == 2


def test_get_list_lifo_customer_products(get_customer):
    customer = get_customer()
    assert len(customer.product_ids) == 2
    customer.add_product("kh13e51595")
    assert customer.product_ids[0] == "kh13e51595"
