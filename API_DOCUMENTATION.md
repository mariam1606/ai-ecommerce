# AI E-Commerce API Documentation

## Authentication

### Register

POST /accounts/register/

Creates a new customer account.

### Login

POST /login/

Authenticates a customer.

### Logout

POST /logout/

Logs out the current customer.

---

## Products

### Product List

GET /

Returns available products.

Supports:

- Search
- Category filtering

Example:

GET /?q=laptop

GET /?category=1

---

### Product Details

GET /product/<id>/

Returns product information and similar products.

---

## Cart

### Cart

GET /cart/

Returns the current user's shopping cart.

### Add Product

GET /cart/add/<product_id>/

Adds a product to the cart.

### Update Cart

POST /cart/update/<item_id>/

Updates the quantity of a cart item.

### Remove Item

GET /cart/remove/<item_id>/

Removes an item from the cart.

---

## Orders

### Checkout

GET /orders/checkout/

Creates an order from the current cart.

### Order History

GET /orders/

Returns the authenticated user's orders.

### Order Details

GET /orders/<id>/

Returns details of a specific order.

---

## Recommendations

### Personalized Recommendations

GET /recommendations/

Returns personalized product recommendations based on user interactions.

### Trending Products

Returns popular products based on customer interactions.

### Similar Products

Returns products belonging to the same category as the selected product.

---

## Admin

Django Admin:

/admin/

Administrators can manage:

- Products
- Categories
- Orders
- Order status
- Users