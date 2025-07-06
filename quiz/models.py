from django.db import models
from django.utils.html import strip_tags
from tinymce import models as tinymce_models


class UserEntry(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Section(models.Model):
    title = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject, through='SectionSubject', related_name='sections')

    def __str__(self):
        return self.title


class SectionSubject(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=3, decimal_places=1)  # like 3.1

    class Meta:
        unique_together = ('section', 'subject')

    def __str__(self):
        return f"{self.section.title} - {self.subject.name} ({self.score})"


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    image = models.FileField(upload_to="questions/", null=True, blank=True)
    text = tinymce_models.HTMLField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def text_preview(self, text):
        clean_text = strip_tags(text)
        return clean_text[:50] + ('...' if len(clean_text) > 50 else '')

    def __str__(self):
        return self.text_preview(text=self.text)


class Result(models.Model):
    user = models.ForeignKey(UserEntry, on_delete=models.CASCADE, related_name='results')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class Answer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)  # 'A', 'B', etc.
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.question} - {self.selected_option} ({'Correct' if self.is_correct else 'Wrong'})"

