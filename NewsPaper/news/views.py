from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter
from django.contrib.auth.models import Group


class PostDetail(DetailView):

    model = Post

    template_name = 'post.html'

    context_object_name = 'post'


class PostList(ListView):

    model = Post

    ordering = '-date_time'

    template_name = 'news.html'

    context_object_name = 'news'
    paginate_by = 10


class PostFilterList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

   # def form_valid(self, form):
    #    post = form.save(commit=False)
    #    post.category_type = 'NEWS'
     #   return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

   # def form_valid(self, form):
    #    post = form.save(commit=False)
    #    post.category_type = 'NW'
    #    return super().form_valid(form)



class PostDelete(DeleteView):

    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by("-date_time")
        print()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribes.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribes.add(user)
    message = "Вы подписаны на новости категории"
    return render(request, 'subscribe.html', {'category': category, 'message': message})

