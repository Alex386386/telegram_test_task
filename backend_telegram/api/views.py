from rest_framework import viewsets, status, mixins, filters, pagination
from rest_framework.response import Response

from message.models import Message, BotText, CurrencyRate
from user.models import User
from .serializers import UserSerializer, MessageSerializer, BotTextSerializer, CurrencyRateSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        if user_id is not None:
            return User.objects.filter(id=user_id)
        return User.objects.filter(signed=True)


class MessageViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Message.objects.filter(user_id=user_id).order_by('-date')

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user, created = User.objects.get_or_create(
            pk=user_id, defaults={'username': request.data.get('username')}
        )

        message_data = request.data.copy()
        message_data['user'] = user.id

        serializer = self.get_serializer(data=message_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BotTextReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BotText.objects.all()
    serializer_class = BotTextSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class CurrencyRateReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer
