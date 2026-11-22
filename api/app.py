from api.controllers import orden_controller, review_controller

app.include_router(orden_controller.router, prefix=API)
app.include_router(review_controller.router, prefix=API)