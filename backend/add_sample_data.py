from main import SessionLocal, Category, Product

db = SessionLocal()

# Add Categories
categories = [
    Category(name="Men's Clothing", description="Clothing for men"),
    Category(name="Women's Clothing", description="Clothing for women"),
    Category(name="Accessories", description="Fashion accessories"),
]
for cat in categories:
    db.add(cat)
db.commit()

# Add Products
products = [
    Product(
        name="T-Shirt",
        description="Cotton t-shirt",
        price=29.99,
        category_id=1,
        image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
        stock=50
    ),
    Product(
        name="Jeans",
        description="Blue jeans",
        price=59.99,
        category_id=1,
        image_url="https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        stock=30
    ),
    Product(
        name="Dress",
        description="Summer dress",
        price=79.99,
        category_id=2,
        image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",
        stock=20
    ),
    Product(
        name="Watch",
        description="Elegant watch",
        price=149.99,
        category_id=3,
        image_url="https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=400",
        stock=15
    ),
]
for prod in products:
    db.add(prod)
db.commit()

print("✅ Sample data added successfully!")
db.close()
