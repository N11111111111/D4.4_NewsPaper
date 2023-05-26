from django.views.generic import ListView,  DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    gueryset = Post.objects.order_by('-id')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        context['categories'] = Category.objects.all()

        return context

#найти новость или статью, фильтрация, пагинация

class SearchPosts(ListView):
    paginate_by = 3
    model = Post
    ordering = '-dateCreation'
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = PostFilter(self.request.GET, queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


#подробности о статье или новости:
class PostDetail(DetailView):
    model = Post
    template_name = 'id.news.html'
    context_object_name = 'post'


# создаем:
class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm
    context_object_name = 'post_create'
    success_url = '/news/'


# редактируем
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    context_object_name = 'post_edit'
    success_url = '/news/'


# удаляем
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)




