from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.customer.adapters.repository import CustomerRepository, Paginator
from app.customer.exceptions import (
    CustomerAlreadyExistError,
    CustomerDatabaseError,
    CustomerNotDeletedError,
    CustomerNotFoundError,
    CustomerNotUpdatedError,
    CustomerServiceGetProductsError,
)
from app.customer.models import Customer
from app.customer.service import CustomerService
from app.entrypoints.factories import (
    make_customer_motor_repository,
    make_customer_service,
)
from app.entrypoints.fastapi.endpoints.customers.v1.schema import (
    CustomerCreate,
    CustomerGetResponse,
    CustomerUpdate,
    ProductCreate,
    ProductGetResponse,
)
from app.product.exceptions import ProductNotFoundError

router = APIRouter()


@router.get(
    "/{email}",
    summary="Retrieve customer and a list product ids",
)
async def get(
    email: str,
    page: int = Query(1, gt=0),
    repo: CustomerRepository = Depends(make_customer_motor_repository),
) -> CustomerGetResponse:
    try:
        customer, paginator = await repo.get(email, Paginator(page=page))
        return CustomerGetResponse(
            item=customer, paginator_product_ids=paginator
        )
    except CustomerNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )
    except CustomerDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a customer without list of favorite products",
)
async def create(
    customer: CustomerCreate,
    repo: CustomerRepository = Depends(make_customer_motor_repository),
) -> None:
    try:
        await repo.create(Customer(**customer.model_dump()))
    except CustomerAlreadyExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer already exists.",
        )
    except CustomerDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/{email}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update customer",
)
async def update(
    email: str,
    customer: CustomerUpdate,
    repo: CustomerRepository = Depends(make_customer_motor_repository),
) -> None:
    try:
        await repo.update(email=email, name=customer.name)
    except CustomerNotUpdatedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer not found.",
        )
    except CustomerDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{email}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete customer and their favorites list",
)
async def delete(
    email: str,
    repo: CustomerRepository = Depends(make_customer_motor_repository),
) -> None:
    try:
        await repo.delete(email)
    except CustomerNotDeletedError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )
    except CustomerDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/{email}/products",
    summary="Retrieve favorite products list "
    "containing all product information",
)
async def get_customer_products(
    email: str,
    page: int = Query(1, gt=0),
    service: CustomerService = Depends(make_customer_service),
) -> ProductGetResponse:
    try:
        product_list, paginator = await service.get_products_by_customer(
            email, Paginator(page=page)
        )
        return ProductGetResponse(items=product_list, paginator=paginator)
    except CustomerNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )
    except CustomerServiceGetProductsError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found.",
        )
    except CustomerDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/{email}/products",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Add product ids to favorite products list",
)
async def add_customer_product(
    email: str,
    product: ProductCreate,
    service: CustomerService = Depends(make_customer_service),
) -> None:
    try:
        await service.add_customer_product(
            email=email, product_id=product.product_id
        )
    except ProductNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )
    except CustomerNotUpdatedError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found or product already exists.",
        )
    except CustomerDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
