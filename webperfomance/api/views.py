# gateway/views.py
import json, base64
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from webperfomance.convex_client import ConvexClient  # your merged hybrid client
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
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



# class WasmGateway(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             raw = request.body or b""
#             print("Request raw body:", raw)

#             if not raw:
#                 print("Empty request body")
#                 return Response({"error": "empty request body"}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 packet = json.loads(raw.decode())
#                 print("Decoded packet:", packet)
#             except json.JSONDecodeError as e:
#                 print("JSON decode error:", e)
#                 return Response({"error": "invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

#             route = packet.get("route")
#             payload_b64 = packet.get("payload")
#             token = packet.get("token")
#             print(f"Route: {route}, Payload (b64): {payload_b64}, Token: {token}")

#             if not route or not payload_b64:
#                 print("Missing route or payload")
#                 return Response({"error": "invalid packet"}, status=status.HTTP_400_BAD_REQUEST)

#             # JWT validation
#             user = None
#             if token:
#                 try:
#                     access = AccessToken(token)
#                     user_id = access.get("user_id")
#                     User = get_user_model()
#                     user = User.objects.get(id=user_id)
#                     print("Authenticated user:", user)
#                 except Exception as e:
#                     print("JWT validation failed:", e)
#                     return Response({"error": "token_invalid_or_expired"}, status=status.HTTP_401_UNAUTHORIZED)

#             # Decode payload
#             try:
#                 payload_json = base64.b64decode(payload_b64).decode()
#                 data = json.loads(payload_json)
#                 print("Decoded payload data:", data)
#             except Exception as e:
#                 print("Payload decode error:", e)
#                 return Response({"error": "invalid payload"}, status=status.HTTP_400_BAD_REQUEST)

#             # Initialize Convex client
#             try:
#                 convex = ConvexClient(user=user)
#                 print("Convex client initialized")
#             except Exception as e:
#                 print("Convex client initialization failed:", e)
#                 return Response({"error": "convex_client_init_failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Route mapping
#             convex_fn_map = {
#                 "/api/messages/list/": "messages:list",
#                 "/api/messages/add/": "messages:add",
#                 "/api/users/get/": "users:getProfile",
#             }
#             fn_name = convex_fn_map.get(route)
#             if not fn_name:
#                 print("Unknown route:", route)
#                 return Response({"error": "unknown route"}, status=status.HTTP_400_BAD_REQUEST)
#             print("Convex function name:", fn_name)

#             # Call Convex function
#             try:
#                 result = convex.call_function(fn_name, args=data, use_cache=True)
#                 print("Convex call result:", result)
#             except Exception as e:
#                 print("Convex call failed:", e)
#                 import traceback
#                 traceback.print_exc()
#                 return Response({"error": "convex_call_failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Encode response
#             response_packet = {
#                 "route": route,
#                 "payload": base64.b64encode(json.dumps(result).encode()).decode()
#             }
#             print("Response packet:", response_packet)
#             return Response(response_packet)

#         except Exception as exc:
#             print("Unhandled exception in WasmGateway:", exc)
#             import traceback
#             traceback.print_exc()
#             return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  # make sure this imports your class above

import json
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from webperfomance.convex_client import ConvexClient


class WasmGateway(APIView):
    permission_classes = [AllowAny]

    convex_map = {
        "/api/messages/list/": "/messages/list",
        "/api/messages/add/": "/messages/add",
    }

    def post(self, request):
        packet = json.loads(request.body.decode())

        route = packet["route"]

        payload = json.loads(
            base64.b64decode(packet["payload"]).decode()
        )

        path = self.convex_map.get(route)

        if not path:
            return Response(
                {"error": "unknown route"},
                status=400
            )

        convex = ConvexClient()

        try:
            result = convex.call_http(path, payload)

            return Response({
                "payload": base64.b64encode(
                    json.dumps(result).encode()
                ).decode()
            })

        except Exception as e:
            return Response({
                "error": "convex_call_failed",
                "details": str(e)
            }, status=500)



