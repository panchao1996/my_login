from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from . import models
import hashlib

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'GET':
        # 用户初次进入展示登录表单
        return render(request,'login.html')

    elif request.method == 'POST':
        context =   {
            'message':''
        }
        # 用户提交表单
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 验证账户名密码
        user = models.User.objects.filter(name=username).first()
        if user:
            if _hash_password(password) == user.hash_password:
            # if user.password == password:
                context['message'] = '登陆成功'
                # 服务器设置sessionid和其他用户信息，sessionid（服务器给访问它的浏览器的身份证）自动生成。
                request.session['is_login'] = True
                request.session['username'] = user.name
                request.session['userid'] = user.id
                return redirect('/index/') # 返回的响应中包含set-cookie（sessionid='askdjfADAS'）,浏览器收到响应后会把sessionid存到cookie中
            else:
                context['message'] = '密码错误'
                return render(request,'login.html',context=context)
        else:
            context['message'] = '未注册'
            return render(request, 'login.html', context=context)
        # if not user:
        #     print('用户未注册，或密码错误')
        #     return redirect('/login/')
        # # 登录成功
        # print('注册成功')
        # return redirect('/index/')

def register(request):
    if request.method == 'GET':
        # 注册表单
        return render(request,'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # 简单后端表单验证（正则最合适）
        # if not (username.strip() and password.strip() and email.strip()):
        #     print('某个字段为空')
        #     return render('/register',context={'message':'某个字段为空'})
        # if len(username) > 20 or len(password) >20:
        #     print('用户字段或密码长度不能超过20')
            # 排除特殊字符串 eval \q &$


        # insert into login_user(name,password,email)values(%s,%s,%s)' % ('','','')
        user =models.User.objects.filter(email=email).first()
        if user:
            return render(request,'register.html',context={'message':'用户已注册'})
        # 加密密码
        hash_password = _hash_password(password)

        # 写数据库
        try:
            user = models.User(name=username,password=password,hash_password=hash_password,email=email)
            user.save()
            print('保存成功')
            return render(request,'login.html',context={'message':'注册成功，请继续登录'})
        except Exception as e:
            print('保存失败',e)   #比起用
            return redirect('/register')


def logout(request):
    """登出"""

    # 清除session 登出
    request.session.flush()       # 清除此用户sessionid对应的所有sessiondata
    return redirect('/index/')

def _hash_password(password):
    """哈希加密用户注册密码"""
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()

    salt = ''
    for i in range(4):
        salt +=chr(random.randint(60,90))
 # 查询数据库   'select * from login_user where name=%s and password=%s' %(username,password)
 #        user = models.User.objects.filter(name=username,password=password).first()
