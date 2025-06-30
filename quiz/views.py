from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Section, SectionSubject, Question
from .serializers import SectionSerializer, QuestionSerializer, QuizSubmissionSerializer


class SectionListAPIView(APIView):
    def get(self, request):
        sections = Section.objects.prefetch_related('sectionsubject_set__subject')
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)


class SectionQuestionsAPIView(APIView):
    def get(self, request, section_id):
        section_subjects = SectionSubject.objects.filter(section_id=section_id).select_related('subject')
        result = []

        for ss in section_subjects:
            questions = Question.objects.filter(subject=ss.subject)
            serialized_questions = QuestionSerializer(questions, many=True).data

            result.append({
                "name": ss.subject.name,
                "score": ss.score,
                "questions": serialized_questions
            })

        return Response({"subjects": result})


class QuizSubmitAPIView(APIView):
    def post(self, request):
        serializer = QuizSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            result_data = serializer.save()
            return Response(result_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
