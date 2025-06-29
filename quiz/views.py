from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Section
from .serializers import SectionSerializer


class SectionListAPIView(APIView):
    def get(self, request):
        sections = Section.objects.prefetch_related('sectionsubject_set__subject')
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)
