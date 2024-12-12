from django.urls import path
from .views import RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView

urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),  # Use RecipeListView for the home page
    path('<int:user_id>/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:user_id>/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('<int:user_id>/<slug:slug>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:user_id>/<slug:slug>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
]
