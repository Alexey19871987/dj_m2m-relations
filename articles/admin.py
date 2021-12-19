from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, ArticleTags, Tag

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            form.cleaned_data
            print(form.cleaned_data)

            # if form.cleaned_data['is_main'] is False:
            #     raise ValidationError('Укажите основной раздел')

            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке

            # raise ValidationError('Тут всегда ошибка')
        return super().clean()  # вызываем базовый код переопределяемого метода

class RelationshipInline(admin.TabularInline):
    model = ArticleTags
    formset = RelationshipInlineFormset

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [RelationshipInline]