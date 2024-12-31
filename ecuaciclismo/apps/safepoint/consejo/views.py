from rest_framework import generics
from .models import Consejo, Tip
from .serializers import ConsejoSerializer, TipSerializer

class ConsejoListView(generics.ListAPIView):
    queryset = Consejo.objects.all()
    serializer_class = ConsejoSerializer

class TipListView(generics.ListAPIView):
    serializer_class = TipSerializer

    def get_queryset(self):
        consejo_id = self.request.query_params.get('consejo')
        return Tip.objects.filter(consejo_id=consejo_id)
