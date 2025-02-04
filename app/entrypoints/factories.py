import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app import settings
from app.customer.adapters.repository import (
    CustomerMotorRepository,
    CustomerRepository,
)
from app.customer.service import CustomerService
from app.product.adapters.repository import (
    ProductCachedMotorRepository,
    ProductCachedRepository,
)
from app.product.adapters.requester import ProductAiohttpRequester
from app.user.adapters.repository import UserMotorRepository, UserRepository

_motor_connection: AsyncIOMotorClient | None = None
_http_client: aiohttp.ClientSession | None = None


async def get_http_client() -> aiohttp.ClientSession:
    global _http_client
    if _http_client:
        return _http_client

    connector = aiohttp.TCPConnector(ttl_dns_cache=300)
    _http_client = aiohttp.ClientSession(connector=connector)
    return _http_client


def clean_motor_client():
    _motor_connection.close()


def get_motor_client() -> AsyncIOMotorClient:
    global _motor_connection
    if _motor_connection:
        return _motor_connection
    _motor_connection = AsyncIOMotorClient(
        settings.DB_URL,
    )
    return _motor_connection


def get_motor_db() -> AsyncIOMotorDatabase:
    client = get_motor_client()
    return client.get_default_database()


def make_customer_motor_repository() -> CustomerRepository:
    db = get_motor_db()
    return CustomerMotorRepository(db)


def make_user_motor_repository() -> UserRepository:
    db = get_motor_db()
    return UserMotorRepository(db)


def make_product_cached_motor_repository() -> ProductCachedRepository:
    db = get_motor_db()
    return ProductCachedMotorRepository(db)


async def make_product_aiohttp_requester() -> ProductAiohttpRequester:
    client = await get_http_client()
    return ProductAiohttpRequester(client)


async def make_customer_service() -> CustomerService:
    customer_repo = make_customer_motor_repository()
    product_cached_repo = make_product_cached_motor_repository()
    product_requester = await make_product_aiohttp_requester()

    return CustomerService(
        customer_repo=customer_repo,
        product_cached_repo=product_cached_repo,
        product_requester=product_requester,
    )
