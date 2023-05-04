# WatchMe
WatchMe is a full-stack web application developed as a final project for the purpose of analyzing and implementing protection against security vulnerabilities. Built using the Django framework and MVC architecture, the primary focus of WatchMe is on security.

### Security Measures

* Protection against SQL injection attacks using Django's built-in Object Relational Mapping (ORM)
* Cross-Site Scripting (XSS) prevention using Django's built-in template engine and security middleware
* Protection against Cross-Site Request Forgery (CSRF) using Django's built-in CSRF protection middleware
* Password protection based on OWASP rules for passwords
* Access control
* Session management using Django's built-in features for session security 

### Functionalities

The app features an online store for hand watches, with functionalities for guest, user, and administrator roles.

**Guest**
* Registration and login capability
* Ability to view all products
* Ability to view product details
* Ability to search for products

**User**
* All functionalities of a guest
* Ability to add products to cart
* Ability to view products in the cart
* Ability to delete products from the cart
* Ability to change personal information
* Ability to purchase products in the cart
* Ability to leave product reviews

**Administrator**
* All functionalities of a user
* Ability to add new products, modify and delete existing ones
* Ability to delete users
* Ability to view completed purchases
