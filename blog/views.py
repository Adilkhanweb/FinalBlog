from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostView, Like, Comment, Category
from .forms import PostForm, CommentForm, CategoryForm


# Create your views here.
def index(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    return render(request, "blog/home.html", {"posts": posts, "categories": categories})


class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            # Adding user as the user for that post
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect("detail", slug=post.slug)
        # If the form is not valid, also redirect to details
        return redirect("detail", slug=self.get_object().slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })
        return context

    def get_object(self, **kwargs):
        """
        This method handles the view count.
        """
        object = super().get_object(**kwargs)
        if self.request.user.is_authenticated:
            # get_or_created: if you visit the website twice,
            # it wount count two times, but it will couse error
            # to anonymous users
            PostView.objects.get_or_create(user=self.request.user, post=object)
        # Otherwise don't do anything
        return object


class PostCreateView(CreateView):
    # We need to specify the fields that we want to allow user to update
    # Here we can only specify fields or form. We cannot specify both
    form_class = PostForm
    model = Post
    template_name = "blog/create_post.html"
    success_url = '/'

    # passing context into the view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(PostCreateView, self).form_valid(form)


class CategoryCreateView(CreateView):
    form_class = CategoryForm
    model = Category
    template_name = "blog/create_category.html"
    success_url = '/'


def categoryPosts(request, slug):
    posts = Post.objects.filter(category__slug=slug)
    return render(request, "blog/home.html", {"posts": posts})


class PostUpdateView(UpdateView):
    # We need to specify the form we want to display to user
    form_class = PostForm
    model = Post
    template_name = "blog/update_post.html"
    # Redirect to following
    success_url = '/'

    # passing context into the view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


def PostDeleteView(request, slug):
    post = Post.objects.get(slug=slug)
    if post:
        post.delete()
        return redirect('index')
    return redirect('index')


# this method is going to handle the liking and disliking proccess
def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        # Unlike the post
        like_qs[0].delete()
        return redirect('detail', slug=slug)

    Like.objects.create(user=request.user, post=post)
    return redirect('detail', slug=slug)
