import asyncio
from typing import Any

from app.customer.adapters.repository import CustomerRepository, Paginator
from app.customer.adapters.schemas import PaginatorResponse
from app.customer.exceptions import CustomerServiceGetProductsError
from app.product.adapters.repository import ProductCachedRepository
from app.product.adapters.requester import ProductRequester
from app.product.exceptions import ProductNotFoundError


class CustomerService:
    def __init__(
        self,
        customer_repo: CustomerRepository,
        product_cached_repo: ProductCachedRepository,
        product_requester: ProductRequester,
    ) -> None:
        self.customer_repo = customer_repo
        self.product_cached_repo = product_cached_repo
        self.product_requester = product_requester

    async def _get_product(self, product_id):
        """
        Retrieves a product by first checking the cache.
        If not found, it fetches the product from the API,
        stores it in the cache, and returns the result.
        Returns None if the product is unavailable or an error occurs.
        """
        if product := await self.product_cached_repo.get(product_id):
            return product
        if product := await self.product_requester.get(product_id):
            await self.product_cached_repo.upsert(product)
            return product
        return None

    async def get_products_by_customer(
        self, customer_email: str, page: Paginator
    ) -> tuple[list[dict[Any, Any]], PaginatorResponse]:
        """
        Variables:
            tasks (dict[asyncio.Task, str]): Dictionary mapping
                asynchronous tasks to their respective product IDs.
            product_list (list[dict[Any, Any] | None]): List of
                retrieved products, where None indicates a failed retrieval.
        """
        customer, paginator = await self.customer_repo.get(
            customer_email,
            page,
        )

        tasks = {
            asyncio.create_task(self._get_product(pid)): pid
            for pid in customer.product_ids
        }
        product_list = await asyncio.gather(*tasks.keys())

        if None not in product_list:
            return product_list, paginator

        none_positions = [
            i for i, item in enumerate(product_list) if item is None
        ]
        product_ids_not_found = [
            customer.product_ids[i] for i in none_positions
        ]

        raise CustomerServiceGetProductsError(
            f"Products from customer '{customer.email}' not returned "
            f"due to failure to capture some products from the "
            f"list: {product_ids_not_found}",
        )

    async def add_customer_product(self, email: str, product_id: str) -> None:
        product = await self._get_product(product_id)
        if not product:
            raise ProductNotFoundError()

        await self.customer_repo.add_product(
            email=email,
            product_id=product_id,
        )
