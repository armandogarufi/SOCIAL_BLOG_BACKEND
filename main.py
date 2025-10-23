from fastapi import FastAPI, HTTPException, Query

from dotenv import load_dotenv
load_dotenv()
from shared.config.settings import settings

from pydantic import BaseModel, Field

from typing import List

app = FastAPI(
    title = settings.app_name,
    version = settings.api_version,
    debug = settings.debug
)


# Welcome message endpoint
class WelcomeResponse(BaseModel):
    """
    Response model for welcome message endpoint
    """
    message: str = Field(examples=["Welcome to Social Blog API"])
    version: str = Field(examples=["v1"])
    docs: str = Field(examples=["/docs"])

@app.get("/", response_model=WelcomeResponse)
def welcome_message() -> WelcomeResponse:
    """
    Root endopoint - API Welcome Message
    """
    return WelcomeResponse(
        message = "Welcome to Social Blog API",
        version = settings.api_version,
        docs = "/docs"
    )


# Health check
class HealthResponse(BaseModel):
    """
    Response model for health check endpoint
    """
    status: str = Field(examples=["ok"])
    app: str = Field(examples=["Social Blog"])

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint for monitoring
    """
    return HealthResponse(
        status = "ok",
        app = settings.app_name
    )



# Test path parameter endpoint
class UserResponse(BaseModel):
    """
    Response Model for User data
    """
    user_id: int = Field(examples=[1])
    username: str = Field(examples=["user123"])
    email: str = Field(examples=["user123@gmail.com"])


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_details(user_id: int) -> UserResponse:
    """
    User details endpoint.

    Get user details by user_id.
    """

    return UserResponse(
        user_id = user_id,
        username = f"user{user_id}",
        email = f"user{user_id}@gmail.com"
    )


# Test path parameter endpoint
class ArticleResponse(BaseModel):
    """
    Response Model for Article data
    """
    id: int = Field(examples=[1])
    author_id: int = Field(examples=[2])
    title: str = Field(examples=["Article's Title"])
    content: str = Field(examples=["Article's Content"])

@app.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article_details(article_id: int) -> ArticleResponse:
    """
    Endpoint for get article details by article_id
    """

    return ArticleResponse(
        id = article_id,
        author_id = article_id + 1,
        title = f"Article {article_id}",
        content = f"Content of article {article_id}"
    )


# Test query parameter endpoint

# Lista fake di prodotti (metti all'inizio del file, dopo imports)
FAKE_PRODUCTS = [
    {"id": 1, "name": "Laptop Dell", "category": "electronics", "price": 899.99, "in_stock": True},
    {"id": 2, "name": "Python Book", "category": "books", "price": 29.99, "in_stock": True},
    {"id": 3, "name": "T-Shirt", "category": "clothing", "price": 19.99, "in_stock": False},
    {"id": 4, "name": "iPhone 15", "category": "electronics", "price": 999.99, "in_stock": True},
    {"id": 5, "name": "FastAPI Guide", "category": "books", "price": 39.99, "in_stock": True},
    {"id": 6, "name": "Jeans", "category": "clothing", "price": 59.99, "in_stock": True},
    {"id": 7, "name": "MacBook Pro", "category": "electronics", "price": 1999.99, "in_stock": True},
    {"id": 8, "name": "Django Book", "category": "books", "price": 34.99, "in_stock": False},
    {"id": 9, "name": "Jacket", "category": "clothing", "price": 89.99, "in_stock": True},
    {"id": 10, "name": "Samsung Phone", "category": "electronics", "price": 799.99, "in_stock": True},
]


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    in_stock: bool


class ProductListResponse(BaseModel):
    total: int
    products: List[Product]
    filters_applied: dict




@app.get("/products")
def list_products(
    category: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    search_by_name: str | None = Query(default=None, min_length=2),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: str | None = Query(default=None, pattern="^(price|name)$"),
    sort_order: str | None = Query(default="asc", pattern="^(asc|desc)$"),
    in_stock: bool | None = None    
) -> ProductListResponse:
    """
    List products with filters, search, sorting and pagination
    """

    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(
                status_code = 400,
                detail = "min_price must be less than max_price"
            )



    filtered = FAKE_PRODUCTS.copy()
    
    if category:
        filtered = [p for p in filtered if p["category"] == category]
    
    if min_price is not None:
        filtered = [p for p in filtered if p["price"]  >= min_price]
    
    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]
    
    if search_by_name:
        filtered = [p for p in filtered if search_by_name.lower() in p["name"].lower()]

    if in_stock is not None:
        filtered = [p for p in filtered if p["in_stock"] == in_stock]
    
    if sort_by:
        reverse = (sort_order == "desc")
        filtered = sorted(filtered, key=lambda p: p[sort_by], reverse=reverse)

    
    total = len(filtered)
    paginated = filtered[offset: offset + limit]
    products = [Product(**p) for p in paginated]

    filters_applied = {
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "search_by_name": search_by_name,
        "limit": limit,
        "offset": offset,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "in_stock": in_stock
    }

    return ProductListResponse(
        total = total,
        products = products,
        filters_applied = filters_applied
    )



# Altro test per query parameters
class SearchResult(BaseModel):
    id: int
    name: str
    category: str
    price: float


class SearchResponseModel(BaseModel):
    query: str
    results_count: int
    results: List[SearchResult]


@app.get("/search")
def search(
    q: str = Query(..., min_length=2, max_length=50),
    category: str | None = None,
    sort: str | None = Query(default="relevance", pattern="^(price_asc|price_desc|name|relevance)$")
) -> SearchResponseModel:
    
    results = FAKE_PRODUCTS.copy()

    if category:
        results = [p for p in results if p["category"] == category]
    
    results = [p for p in results if q.lower() in p["name"].lower()]

    
    if sort == "price_asc":
        results = sorted(results, key=lambda p: p["price"])
    elif sort == "price_desc":
        results = sorted(results, key=lambda p: p["price"], reverse=True)
    elif sort == "name":
        results = sorted(results, key=lambda p: p["name"])
    
    results_count = len(results)

    search_results = [SearchResult(**p) for p in results]


    return SearchResponseModel(
        query = q,
        results_count = results_count,
        results = search_results
    )