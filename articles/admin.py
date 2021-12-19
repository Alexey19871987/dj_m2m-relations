from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, ArticleTags, Tag

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        self.curent_tag = False

        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            form.cleaned_data

            if self.curent_tag and form.cleaned_data.get('is_main'):
                raise ValidationError('Главный может быть только 1')
            else:
                if form.cleaned_data.get('is_main'):
                    print(f"{form.cleaned_data.get('tag')} - главный раздел")
                    self.curent_tag = True
                else:
                    continue

        if not form.cleaned_data and not self.curent_tag:
            raise ValidationError('Не выбран главный раздел')

            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке

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