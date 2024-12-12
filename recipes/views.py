from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, update_session_auth_hash
# from django_filters import FilterSet
from .models import Recipe
# from .filters import RecipeFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Recipe
from .forms import RecipeForm


def home(request):
    return render(request, 'home.html')






class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/home.html"
    context_object_name = "recipes"
    # paginate_by = 9  # Pagination limit per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('RecipesSearch', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(tags__name__icontains=search_query)
            ).distinct()
        return queryset
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     # Handle pagination and add it to the context
    #     paginator = context['recipes'].paginator
    #     page_number = self.request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     print("Paginated Recipes:", page_obj)

    #     context['recipes'] = page_obj  # This will pass the paginated object
    #     return context



class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_object(self):
        return get_object_or_404(
            Recipe, 
            slug=self.kwargs['slug'], 
            user_id=self.kwargs['user_id']
        )


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  # Link the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"

    def get_object(self):
        return get_object_or_404(
            Recipe, 
            slug=self.kwargs['slug'], 
            user_id=self.kwargs['user_id'], 
            user=self.request.user  # Ensure only the creator can update
        )

    def get_success_url(self):
        return reverse_lazy("home")


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/recipe_confirm_delete.html"

    def get_object(self):
        return get_object_or_404(
            Recipe, 
            slug=self.kwargs['slug'], 
            user_id=self.kwargs['user_id'], 
            user=self.request.user  # Ensure only the creator can delete
        )

    def get_success_url(self):
        return reverse_lazy("home")
