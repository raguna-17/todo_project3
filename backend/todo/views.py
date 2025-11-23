# todo/views.py
import logging
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer, UserSerializer
from .filters import TodoFilter

logger = logging.getLogger(__name__)

# -------------------------
# ユーザー登録
# -------------------------
class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'id': user.id, 'username': user.username}, status=201)

# -------------------------
# Todo API
# -------------------------
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = TodoFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except Exception as e:
            logger.exception("Failed to create Todo")
            raise

# -------------------------
# ログアウト (refresh トークンをブラックリスト化)
# -------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    クライアントから refresh トークンを受け取りブラックリスト化する（ログアウト）
    POST body: {"refresh": "<refresh_token>"}
    """
    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logged out"}, status=205)
    except Exception as e:
        logger.exception("Failed to blacklist refresh token")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
