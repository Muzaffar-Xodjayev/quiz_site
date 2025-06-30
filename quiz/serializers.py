from rest_framework import serializers
from .models import UserEntry, Result, Answer
from collections import defaultdict
from .models import Section, Subject, SectionSubject, Question


class SectionSubjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='subject.id')
    name = serializers.CharField(source='subject.name')

    class Meta:
        model = SectionSubject
        fields = ['id', 'name', 'score']


class SectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    block = serializers.CharField(source='title')
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'block', 'subjects']

    def get_subjects(self, obj):
        section_subjects = SectionSubject.objects.filter(section=obj).select_related('subject')
        return SectionSubjectSerializer(section_subjects, many=True).data


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'image', 'option_a', 'option_b', 'option_c', 'option_d']


class QuizSubmissionSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    section_id = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

    def create(self, validated_data):
        user = UserEntry.objects.create(name=validated_data['user_name'])
        section = Section.objects.get(id=validated_data['section_id'])
        answers_data = validated_data['answers']

        question_ids = [int(a['question_id']) for a in answers_data]
        questions = Question.objects.filter(id__in=question_ids).select_related('subject')
        question_map = {q.id: q for q in questions}

        result = Result.objects.create(
            user=user,
            section=section,
            total_questions=len(answers_data),
            correct_answers=0,
            score=0
        )

        # Prepare subject-wise tracking
        subject_stats = defaultdict(lambda: {
            "name": "",
            "score": 0,
            "correct_answers": 0,
            "total_questions": 0,
            "total_score": 0.0
        })

        total_score = 0
        correct_count = 0

        for answer in answers_data:
            qid = int(answer['question_id'])
            selected = answer['selected_option'].upper()

            question = question_map[qid]
            is_correct = (selected == question.correct_option)

            Answer.objects.create(
                result=result,
                question=question,
                selected_option=selected,
                is_correct=is_correct
            )

            subject = question.subject
            try:
                weight = SectionSubject.objects.get(section=section, subject=subject).score
            except SectionSubject.DoesNotExist:
                weight = 1.0  # default fallback

            # Initialize subject stats if needed
            subject_data = subject_stats[subject.id]
            subject_data["name"] = subject.name
            subject_data["score"] = float(weight)
            subject_data["total_questions"] += 1

            if is_correct:
                subject_data["correct_answers"] += 1
                subject_data["total_score"] += float(weight)
                correct_count += 1
                total_score += float(weight)

        result.correct_answers = correct_count
        result.score = round(total_score, 2)
        result.save()

        # Prepare final response format
        subject_list = []
        for stats in subject_stats.values():
            stats["total_score"] = round(stats["total_score"], 2)
            subject_list.append(stats)

        return {
            "user_name": user.name,
            "subjects": subject_list,
            "total_score": round(total_score, 2)
        }
