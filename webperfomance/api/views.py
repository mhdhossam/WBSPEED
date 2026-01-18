# gateway/views.py
import json, base64
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")  # note: client may send WASM pre-hashed password
        if not username or not password:
            return Response({"error":"username/password required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error":"invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            return Response({"error":"invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})

# WasmGateway — receive sealed packets {route, payload (base64), token}
class WasmGateway(APIView):
    permission_classes = [AllowAny]  # we validate token within the packet

    def post(self, request):
        try:
            raw = request.body.decode()
            packet = json.loads(raw)
            route = packet.get("route")
            payload_b64 = packet.get("payload")
            token = packet.get("token")  # may be None

            if not route or not payload_b64:
                return Response({"error":"invalid packet"}, status=status.HTTP_400_BAD_REQUEST)

            user_id = None
            if token:
                try:
                    access = AccessToken(token)  # will raise if invalid/expired
                    user_id = access.get("user_id")
                except Exception:
                    return Response({"error":"token_invalid_or_expired"}, status=status.HTTP_401_UNAUTHORIZED)

            # decode payload
            payload_json = base64.b64decode(payload_b64).decode()
            data = json.loads(payload_json)

            # Simple routing example — extend as needed
            if route == "/api/data/":
                name = data.get("name", "guest")
                result = {"msg": f"Hello {name}", "user_id": user_id}
            else:
                result = {"error":"unknown route"}

            response_packet = {
                "route": route,
                "payload": base64.b64encode(json.dumps(result).encode()).decode()
            }
            return Response(response_packet)

        except Exception as exc:
            return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
