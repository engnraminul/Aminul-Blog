from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView, View, TemplateView, DeleteView, ListView
from Blog_App.models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from Blog_App.forms import CommentForm


# Create your views here.


class CreatePost(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'Blog_App/create_post.html'
    fields = ('blog_title', 'blog_content', 'blog_image')


    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))

class PostList(ListView):
    context_object_name= 'posts'
    model = Blog
    template_name = 'Blog_App/Post_list.html'

@login_required
def post_details(request, slug):
    post = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=post, user= request.user)
    if already_liked:
        liked = True
    else:
        liked = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = post
            comment.save()
            return HttpResponseRedirect(reverse('Blog_App:post_details', kwargs={'slug':slug}))

    return render(request, 'Blog_App/post_details.html', context={'post':post, 'comment_form':comment_form, 'liked':liked,})


@login_required
def liked(request, pk):
    post = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=post, user=user)
    if not already_liked:
        liked_post = Likes(blog=post, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('Blog_App:post_details', kwargs={'slug':post.slug}))

@login_required
def unliked(request, pk):
    post = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=post, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('Blog_App:post_details', kwargs={'slug':post.slug}))

class EditPost(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'Blog_App/edit_post.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('Blog_App:post_details', kwargs={'slug':self.object.slug})

class DeletePost(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'Blog_App/delete_post.html'
    success_url = reverse_lazy("Login_App:profile")
