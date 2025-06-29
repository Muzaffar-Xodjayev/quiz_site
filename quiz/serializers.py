from rest_framework import serializers
from .models import Section, Subject, SectionSubject


class SectionSubjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='subject.id')
    name = serializers.CharField(source='subject.name')

    class Meta:
        model = SectionSubject
        fields = ['id', 'name', 'score']


class SectionSerializer(serializers.ModelSerializer):
    block = serializers.CharField(source='title')
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['block', 'subjects']

    def get_subjects(self, obj):
        section_subjects = SectionSubject.objects.filter(section=obj).select_related('subject')
        return SectionSubjectSerializer(section_subjects, many=True).data
