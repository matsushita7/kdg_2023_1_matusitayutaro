from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView,DetailView,UpdateView
from .models import Coment,Profile,Reply,CommentFavoUser
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
# from .models import YourModel
# Create your views here.


class TopPageView(ListView): #利用中
    template_name = 'sns/index.html'
    model = Coment
    
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        if q := query.get('q'):
            queryset = queryset.filter(text__icontains=q)

        return queryset.order_by('-id')


    
class ComentView(LoginRequiredMixin,CreateView): #利用中
    template_name = 'sns/coment.html'
    model = Coment
    fields = ('text','category','images')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    def get_success_url(self):
        return reverse('index')


class ReplyView(CreateView):
    template_name = 'sns/reply.html'
    model = Reply
    fields = ('text','images','comment_id')
    success_url = reverse_lazy('index') #一個前の画面に戻したい

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = Coment.objects.get(pk=self.kwargs['pk'])
        print(context)
        return context


class SettingView(LoginRequiredMixin,ListView): #利用中
    template_name = 'sns/setting.html'
    model = Coment
    


@require_POST  #利用中
def deletecomment(request,pk):
    comment = get_object_or_404(Coment,id=pk)
    comment.delete()
    print(request.user.id)

    return redirect(request.META.get('HTTP_REFERER', '/'))


def profileView(request, ids): #利用中
    comments = Coment.objects.filter(user_id = ids).order_by('-id')
    profileedit = Profile.objects.filter(user_id = ids)
    print(comments)
    context = {
        'comments' : comments,
        'profileedit': profileedit,
    }
    return render(request,'sns/profile.html',context)



class ProfileSettingView(UpdateView):
    template_name = 'sns/profilesetting.html'
    model = Profile
    fields = ('text','images','user')
    
    success_url = reverse_lazy('') # 一個前の画面に戻したい


class SearchView(ListView): #使用中。課題点→検索して絞った要素しか取り出せてないため、柔軟性がない。
    template_name = 'sns/search.html'
    model = Coment
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        query = self.request.GET

        if p := query.get('p'):
            queryset = queryset.filter(text__icontains=p)
        return queryset.order_by('-id')
    
    
class Test(ListView): #検討中。検索ワードをページが飛んでも残しておくため、そのワードを使い、別のソートをしたい。
    template_name = 'sns/test.html'
    model = Coment
    def get_queryset(self):
        query = self.request.GET.get('p','')#pの取得に失敗している？取得はできている
        commentsort = Coment.objects.filter(text__icontains=query)
        sort_by = self.request.GET.get('sort','')
        
        if sort_by == 'new':
            commentsort = commentsort.order_by('-id')
        if sort_by == 'good':
            commentsort = commentsort.order_by('-likes')
        return commentsort

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)  #独自のcontextデータを格納するための儀式
        context['query'] = self.request.GET.get('p','')
        context['commentsort'] = self.get_queryset() #get_queryset関数を呼び出して、returnで帰ってきているのはcommentsortなので、ソートされた内容がcontextに入ってくれている。
        return context
# returnはテンプレートに二つ返すことができるかどうか←できない。get_context_dataでテンプレートに詰めたい要素を集めてきて一気にcontextで返すのが良い。




def evaluationview(request, pk): #使用中。いいねは一回までしかできない。名前に数字を使われたとき不具合が起きてしまうことがある。（問題あり）
    comment = Coment.objects.get(pk=pk)
    commentuser = CommentFavoUser.objects.filter(pk=pk)
    author_name = request.user.username + str(request.user.id)
    
    if author_name in commentuser.user_record:
        comment.likes -= 1
        CommentFavoUser.objects.filter(author_name = CommentFavoUser.user_record).delete()
        comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        comment.likes = comment.likes + 1
        CommentFavoUser.user_record = comment.user_record + author_name
        comment.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class DetailView(DetailView):#アイコンにホバーした時プロフィールの言葉を浮かばせる
    template_name = 'sns/detail.html'
    model = Coment


def search_view(request):  #現在未使用
    query = request.GET.get('q', '')  # 'q'は検索ワードのクエリパラメーター名
    results = Coment.objects.filter(text__icontains=query)

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'sns/test.html', context)