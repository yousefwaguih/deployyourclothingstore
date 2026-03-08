from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List
from pydantic import BaseModel
from datetime import datetime
import os

# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./clothing_store.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String)
    stock = Column(Integer, default=0)
    category = relationship("Category", back_populates="products")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create Tables
Base.metadata.create_all(bind=engine)

# Auto seed data
def seed_data():
    db = SessionLocal()
    try:
        if db.query(Category).count() == 0:
            categories = [
                Category(name="رجالي", description="ملابس رجالية"),
                Category(name="نسائي", description="ملابس نسائية"),
                Category(name="أطفال", description="ملابس أطفال"),
            ]
            db.add_all(categories)
            db.commit()

            products = [
                Product(name="قميص كلاسيك", description="قميص أنيق", price=199, category_id=1, image_url="https://via.placeholder.com/300", stock=50),
                Product(name="بنطلون جينز", description="جينز مريح", price=299, category_id=1, image_url="https://via.placeholder.com/300", stock=30),
                Product(name="فستان سهرة", description="فستان أنيق", price=450, category_id=2, image_url="https://via.placeholder.com/300", stock=20),
                Product(name="تيشيرت أطفال", description="تيشيرت ملون", price=99, category_id=3, image_url="https://via.placeholder.com/300", stock=100),
            ]
            db.add_all(products)
            db.commit()
    finally:
        db.close()

seed_data()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    image_url: str
    stock: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    image_url: str
    stock: int
    class Config:
        orm_mode = True

# FastAPI App
app = FastAPI(title="Clothing Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Category Endpoints
@app.post("/categories/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# Product Endpoints
@app.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/category/{category_id}", response_model=List[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.category_id == category_id).all()

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Health Check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# لازم يكون الـ mount في الآخر بعد كل الـ endpoints
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)