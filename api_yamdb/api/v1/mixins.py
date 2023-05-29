from rest_framework import mixins, viewsets


class MixinVeiew(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    pass
