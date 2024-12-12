import django_filters
from .models import Recipe
from django.forms import TextInput

class RecipeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Title',
        # widget=TextInput(attrs={
        #     'class': 'form-control',
        #     'placeholder': 'Search by title',
        # }),
    )
    description = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Description',
        # widget=TextInput(attrs={
        #     'class': 'form-control',
        #     'placeholder': 'Search by description',
        # }),
    )
    tags = django_filters.CharFilter(
        field_name='tags__name',
        lookup_expr='icontains',
        label='Tags',
        # widget=TextInput(attrs={
        #     'class': 'form-control',
        #     'placeholder': 'Search by tags',
        # }),
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'tags']
