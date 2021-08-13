from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

import shop
import cart
import orders
import payment
import coupon

from context_processors import CartMiddleware
from database import engine
from dependencies import env

from shop import main, models
from cart import main
from orders import main, models
from payment import main
from coupon import main,models

secret_key='cart'

middleware = [
    Middleware(SessionMiddleware,secret_key=secret_key),
    Middleware(CartMiddleware)
]

app = FastAPI(middleware=middleware)

env.globals["cart_context"]= CartMiddleware.cart

app.mount("/static",StaticFiles(directory="static"), name="static")

shop.models.Base.metadata.create_all(bind=engine)
orders.models.Base.metadata.create_all(bind=engine)
coupon.models.Base.metadata.create_all(bind=engine)

app.include_router(shop.main.router)
app.include_router(cart.main.router)
app.include_router(orders.main.router)
app.include_router(payment.main.router)
app.include_router(coupon.main.router)