from django.shortcuts import render,redirect,HttpResponse
from functools import wraps

# Create your views here.

#写一个装饰器,检查用户是否登录:cookie的方法
# def wrapper(func):
#     # 使被装饰的不被login的所影响
#     @wraps(func)
#     def inner(request,*args,**kwargs):
#         #校验内容
#         cookie_k = request.get_signed_cookie('k', None, salt='k1')
#         if cookie_k:
#             # 校验成功就执行下面被装饰的函数
#             ret=func(request,*args,**kwargs)
#             return ret
#         else:
#             # 相当于/home/?page=Nan,login的html也设置了<form action="{{ request.get_full_path }}" method="post">
#             next_url=request.get_full_path()
#             # 否则就跳转回这个页面（去登录）
#             return redirect('/login/?next={}'.format(next_url))
#     return inner

#写一个装饰器,检查用户是否登录:session的方法
def wrapper(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        session_k=request.session.get('user',None)
        if session_k:
            ret=func(request,*args,**kwargs)
            return ret
        else:
            return redirect('/login3/')
    return inner




def login(request):
    if request.method=='POST':
        user=request.POST.get('user')
        pwd=request.POST.get('pwd')
        if user=='anan'and pwd=='12345':
            #cookie只能用在响应对象，所以要把直接的跳转写一个rep变量来响应,此处写了cookie，index也要写来对应
            # 拿到响应对象,从网址中获取要跳转的页面的网址
            # post请求里，网址的参数需要从request.get去取
            next_url=request.GET.get('next')
            if next_url:
                rep=redirect(next_url)
            else:
                rep = redirect('/index/')
            rep.set_signed_cookie('k',user,salt='k1',max_age=6)
            return rep
    return render(request,'login.html')

# 删除（退出）cookie功能
def logout(request):
    # 同样用响应对象的方法，这个logout用作退出登录写在了home.html的a标记里
    rep = redirect('/login/')
    rep.delete_cookie('k')
    return rep


def index(request):
    cookie_k = request.get_signed_cookie('k', None, salt='k1')
    if cookie_k:
        return render(request,'index.html')
    else:
        return redirect('/login/')


@wrapper
def home(request):
    return render(request,'home.html')


#session的方法写cookie
def login2(request):
    if request.method=='POST':
        user=request.POST.get('user')
        pwd=request.POST.get('pwd')
        if user=='bobo'and pwd=='123456':
            # request.session['k1']='v1'也可,v1只是一个字符串，如果是user，index2就是bobo,如果写两个，拼接就行，数据库也会更新
            request.session['k1']=user
            request.session['k2'] ='coco'
            #可以设置为None，即默认超时时间；此次的10：浏览器10秒之后失效
            request.session.set_expiry(10)

            return redirect('/index2/')
    return render(request,'login2.html')


def index2(request):
    #从我的大字典中取出当前请求的相应的k1的值，login2设置session，此处也要接收
    value=request.session.get('k1')
    value2 = request.session.get('k2')
    #此行可以打印出session的码，即数据库django_session的session_key
    print(request.session.session_key)
    print('='*120)
    return HttpResponse(value+value2)

#面向对象的方法
from django.views import View
class LoginView(View):


    def get(self,request):
        return render(request,'login3.html')


    def post(self,request):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user == 'dada' and pwd == '123456':
            request.session['user']=user
            request.session.set_expiry(5)
            return redirect('/index3/')

#utils:工具包，decorators:和装饰器相关的库
from django.utils.decorators import method_decorator

class IndexView(View):

    #CBV里面最先执行的是dispatch方法，继承
    def dispatch(self, request, *args, **kwargs):
        #返回类似子类继承父类的方法
        return super(IndexView, self).dispatch(request,*args,**kwargs)


    # @method_decorator(wrapper)：所有的请求方法都要先做登陆验证
    @method_decorator(wrapper)
    def get(self,request):
        user=request.session.get('user','游客')
        return render(request,'index3.html',{'user':user})