from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from home.models import Post, Friend
from home.forms import HomeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404


#def create_post(request):
#    if not request.user.is_authenticated():
#        return render(request, 'accounts/login.html')
#    
#
#    else:
#        form = PostForm(request.POST or None, request.FILES or None)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.user = request.user
#            post.save()
#            message.success(request, "Successfully Posted")
#            return HttpResponseRedirect(post.get_absolute_url())
#
#        context = {
#            
#            "form":form,
#        }    
#        return render(request, "post_form.html", context)
#
#
#class PostDetail(DetailView):
#    template_name = 'post_detail.html' 
#   
#    def get_object(self, *args, **kwargs):
#        slug = self.kwargs.get("slug")
#        post = get_object_or_404(Post, slug=slug)
#        if post.publish > timezone.now().date() or post.draft:
#            if not request.user.is_staf or not request.user.is_superuser:
#                raise Http404
#        return post
#               
#    def get_context_data(self, *args, **kwargs):
#        context = super(PostDetail, self).get_context_data(*args, **kwargs)
#        post = context['object']
#        context['share_string'] = quote_plus(post.content)
#        return context
#
#
#
#
#def post_detail(request, slug=None):
#    post = get_object_or_404(Post, slug=slug)
#    if post.publish > timezone.now().date() or post.draft:
#        if not request.user.is_staf or not request.user.is_superuser:
#            raise Http404
#    share_string = quote_plus(post.content)
#    context = {
#        'share_string':share_string,
#        'post':post,
#        'title':post.title
#    }        
#
#    return render(request, "post_detail.html", context)
#
#
#
#def post_list(request):
#    today = timezone.now().date()
#    query_list = Post.objects.active()
#    if request.user.is_staff or request.user.is_superuser:
#        query_list = Post.objects.all()
#
#    query = request.GET.get("q")
#    if query:
#        query_list = query_list.filter(
#            Q(title__icontains=query)|
#            Q(content__icontains=query)|
#            Q(user__firstname__icontains=query)|
#            Q(user__lastname__icontains=query)
#            ).distinct() 
#    paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
#    page_request_var = "page"
#    page = request.GET.get(page_request_var)
#    try:
#        queryset = paginator.page(page)
#    except PageNotAnInteger:
#        # If page is not an integer, deliver first page.
#        queryset = paginator.page(1)
#    except EmptyPage:
#        # If page is out of range (e.g. 9999), deliver last page of results.
#        queryset = paginator.page(paginator.num_pages)
#
#
#    context = {
#        "object_list": queryset, 
#        "title": "List",
#        "page_request_var": page_request_var,
#        "today": today,
#    }
#    return render(request, "post_list.html", context)   
#
#def post_update(request, slug=None):
#    if not request.user.is_staff or request.user.is_superuser:
#        raise Http404
#    post = get_object_or_404(Post, slug=slug)
#    form = PostForm(request.POST or None or request.FILES or None, post=post)
#    if form.is_valid():
#        post=form.save(commit=False)
#        post=form.save()
#        message.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
#        return HttpResponseRedirect(post.get_absolute_url())
#    context = {
#        'title':post.title,
#        'form':form,
#        'post':post
#
#    }
#    return render(request, "post_form.html", context)
#
#
#def post_delete(request, slug=None):
#    if not request.user.is_staff or not request.user.is_superuser:
#        raise Http404
#    instance = get_object_or_404(Post, slug=slug)
#    instance.delete()
#    messages.success(request, "Successfully deleted")
#    return redirect("home:list")
#
class HomeView(TemplateView):
    template_name = 'accounts/home.html'

    def get(self, request):
        form = HomeForm()
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        args = {
            'form': form, 'posts': posts, 'users': users, 'friends': friends
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('home:home')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:home')
