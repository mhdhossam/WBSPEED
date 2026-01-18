
from django.urls import path
from .views import WasmGateway, RegisterView, LoginView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
   
    path("wasm_gateway/", WasmGateway.as_view(), name="wasm-gateway"),
]
