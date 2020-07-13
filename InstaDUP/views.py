from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
#from django.contrib.auth.forms import UserCreationForm
from InstaDUP.forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from InstaDUP.models import Post, Like, InstaUser, UserConnection


class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostView(ListView):
    model = Post
    template_name = "index.html"

    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

class PostDetailView(DetailView):
    model = Post 
    template_name = "post_detail.html"

class UserDetailView(DeleteView):
    model = InstaUser
    template_name = "user_detail.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    fields = "__all__"
    login_url = "login"

class PostUpdateView(UpdateView):
    model = Post 
    template_name = "post_update.html"
    fields = ["title"]

class PostDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = "sign_up.html"
    success_url = reverse_lazy("login")

@ajax_request #addLike函数只用来响应ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save() #if (post, user) already exists, will not save, but go to exception
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }