from django.contrib.auth import logout,  get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from MMORPG.settings import DEFAULT_FROM_EMAIL
from .filters import CommentFilter
from .token import account_activation_token
from django.core.mail import EmailMessage, send_mail
from .utils import *
from .forms import *


class Home(DataMixin, ListView):
    model = Post
    template_name = 'default.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        # context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        return dict(list(context.items()) + list(c_def.items()))

    def post_user(request):
        context = {
            'posts': Post.objects.filter(author=request.user)
        }

        return render(request, 'default.html', context)


class Comments(ListView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'post_show.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


class NewComment(DataMixin, CreateView):
    form_class = CommentForm
    template_name = 'new_comment.html'
    slug_url_kwarg = 'comment_slug'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['post_slug']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['post'] = Post.objects.get(slug=self.kwargs['post_slug'])
        return context

    def post(self, request, *args, **kwargs):
        email_u = request.user.email
        send_mail(
            "Вам оставили новый комментарий",
            "Вам оставили новый комментарий,посмотреть его можно в личном кабинете по ссылке:"
            " http://127.0.0.1:8000/comment/",
            DEFAULT_FROM_EMAIL,
            [email_u],
            fail_silently=False,
        )
        return super().post(request, *args, **kwargs)


class ShowCategory(DataMixin, ListView):
    model = Post
    template_name = 'default.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    c_def = self.get_user_context(title="Регистрация")
    return dict(list(context.items()) + list(c_def.items()))


def signup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterUserForm()

    return render(request, 'register.html', context={'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class CreatePost(DataMixin, CreateView):
    template_name = 'new_post.html'
    form_class = CreateForm
    slug_url_kwarg = 'post_slug'


class ShowComment(DataMixin, UpdateView):
    model = Comment
    form_class = ButtonForm
    template_name = 'comment_show.html'
    slug_url_kwarg = 'comment_slug'
    context_object_name = 'comment'

    def post(self, request, *args, **kwargs):
        email_u = Comment.objects.get(slug=self.kwargs['comment_slug'])
        if email_u.status == False:
            send_mail(
                "Ваш комментарий приняли",
                "Ваш комментарий приняли",
                DEFAULT_FROM_EMAIL,
                [email_u],
                fail_silently=False,
            )
        return super().post(request, *args, **kwargs)
