from django.shortcuts import render, redirect
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_name(self):
        name_db = self.cleaned_data["name"]
        if models.UserInfo.objects.filter(name=name_db).exists():
            raise ValidationError("用户已存在")
        return name_db


class UserEditModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_name(self):
        name_db = self.cleaned_data["name"]
        if models.UserInfo.objects.exclude(id=self.instance.pk).filter(name=name_db).exists():
            raise ValidationError("该用户名已存在")
        return name_db


class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_title(self):
        title_db = self.cleaned_data["title"]
        if models.Department.objects.filter(title=title_db).exists():
            raise ValidationError("该部门已存在")
        return title_db


class DepartmentEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ["title"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_title(self):
        title_db = self.cleaned_data["title"]
        if models.Department.objects.exclude(id=self.instance.pk).filter(title=title_db).exists():
            raise ValidationError("该部门已存在")
        return title_db


class MobileModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "格式错误")]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_mobile(self):
        mobile_db = self.cleaned_data["mobile"]
        if models.PrettyNum.objects.filter(mobile=mobile_db).exists():
            raise ValidationError("该手机号已存在")
        return mobile_db


class MobileEditModelForm(forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', "格式错误")]
    )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_mobile(self):
        mobile_db = self.cleaned_data["mobile"]
        if models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=mobile_db).exists():
            raise ValidationError("该手机号已存在")
        return mobile_db


# Create your views here.
def depart_list(request):
    data_dict = {}
    query = request.GET.get("q", "")
    if query:
        data_dict["title__contains"] = query
    datalist = models.Department.objects.filter(**data_dict)
    pageList = []
    departCount = datalist.count()
    pageSize = 10
    pageFirst, pageSecond = divmod(departCount, pageSize)
    if pageSecond > 0:
        pageFirst += 1
    for i in range(1, pageFirst + 1):
        page = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        pageList.append(mark_safe(page))  # 标记为安全的，才能显示HTMl
    page = int(request.GET.get("page", 1))
    startPage = (page - 1) * 10
    endPage = page * 10
    datalist = datalist[startPage:endPage]
    return render(request, "depart_list.html", {"datalist": datalist, "query": query, "pageList": pageList})


def depart_add(request):
    if request.method == "GET":
        form = DepartmentModelForm()
        return render(request, "depart_add.html", {"form": form})
    form = DepartmentModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/depart/list')
    return render(request, 'depart_add.html', {"form": form})


def depart_delete(request, nid):
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    # 进入修改页面
    Info = models.Department.objects.filter(id=nid).first()
    if request.method == 'GET':
        # title = models.Department.objects.filter(id=nid).first()
        # return render(request, "depart_edit.html", {"title": title})
        form = DepartmentModelForm(instance=Info)
        return render(request, "depart_edit.html", {"form": form})
    # 修改数据
    # new_title = request.POST.get("title")
    # models.Department.objects.filter(id=nid).update(title=new_title)
    # return redirect("/depart/list/")

    form = DepartmentModelForm(data=request.POST, instance=Info)
    if form.is_valid():
        form.save()
        return redirect("/depart/list")
    return render(request, "depart_edit.html", {"form": form})


def user_list(request):
    data_dict = {}
    query = request.GET.get("q", "")
    if query:
        data_dict["name__contains"] = query
    userlist = models.UserInfo.objects.filter(**data_dict).order_by("-age")
    pageList = []
    userCount = userlist.count()
    pageSize = 10
    pageFirst, pageSecond = divmod(userCount, pageSize)
    if pageSecond > 0:
        pageFirst += 1
    for i in range(1, pageFirst + 1):
        page = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        pageList.append(mark_safe(page))  # 标记为安全的，才能显示HTMl
    page = int(request.GET.get("page", 1))
    startPage = (page - 1) * 10
    endPage = page * 10
    userlist = userlist[startPage:endPage]
    return render(request, "user_list.html", {"userlist": userlist, "query": query, "pageList": pageList})


def user_add(request):
    # if request.method == 'GET':
    #     return render(request, "user_add.html")
    # name = request.POST.get("name")
    # password = request.POST.get("password")
    # age = request.POST.get("age")
    # account = request.POST.get("account")
    # create_time = request.POST.get("create_time")
    # gender = request.POST.get("gender")
    # department_id = request.POST.get("department_id")
    # models.UserInfo.objects.create(name=name, password=password, age=age, account=account, create_time=create_time,
    #                                gender=gender, department_id=department_id)
    # return redirect("/user/list")
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list")
    return render(request, "user_add.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")


def user_edit(request, nid):
    Info = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        # user_info = models.UserInfo.objects.filter(id=nid).first()
        # return render(request, "user_edit.html", {"user_info": user_info})
        form = UserEditModelForm(instance=Info)
        return render(request, 'user_edit.html', {"form": form})
    # name = request.POST.get("name")
    # password = request.POST.get("password")
    # age = request.POST.get("age")
    # account = request.POST.get("account")
    # create_time = request.POST.get("create_time")
    # gender = request.POST.get("gender")
    # if gender == "男":
    #     gender = 1
    # else:
    #     gender = 2
    # department_id = request.POST.get("department_id")
    # print("我的ID是")
    # print(department_id)
    # get_department = models.Department.objects.filter(title=department_id).first()
    # print("我的ID是")
    # print(get_department)
    # department_id = get_department.id
    # models.UserInfo.objects.filter(id=nid).update(name=name, password=password, age=age, account=account,
    #                                               create_time=create_time,
    #                                               gender=gender, department_id=department_id)
    # return redirect("/user/list")
    form = UserEditModelForm(data=request.POST, instance=Info)
    if form.is_valid():
        form.save()
        return redirect("/user/list")
    return render(request, "user_edit.html", {"form": form})


def mobile_list(request):
    data_dict = {}
    query = request.GET.get("q", "")
    if query:
        data_dict["mobile__contains"] = query

    mobilelist = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    pageList = []
    mobileCount = mobilelist.count()
    pageSize = 10
    pageFirst, pageSecond = divmod(mobileCount, pageSize)
    if pageSecond > 0:
        pageFirst += 1
    for i in range(1, pageFirst + 1):
        page = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        pageList.append(mark_safe(page))  # 标记为安全的，才能显示HTMl
    page = int(request.GET.get("page", 1))
    startPage = (page - 1) * 10
    endPage = page * 10
    mobilelist = mobilelist[startPage:endPage]
    return render(request, "mobile_list.html", {"mobilelist": mobilelist, "query": query, "pageList": pageList})


def mobile_edit(request, nid):
    Info = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = MobileEditModelForm(instance=Info)
        return render(request, "mobile_edit.html", {"form": form})
    form = MobileEditModelForm(data=request.POST, instance=Info)
    if form.is_valid():
        form.save()
        return redirect('/mobile/list')
    return render(request, "mobile_edit.html", {"form": form})


def mobile_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/mobile/list")


def mobile_add(request):
    if request.method == "GET":
        form = MobileModelForm()
        return render(request, "mobile_add.html", {"form": form})
    form = MobileModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/mobile/list")
    return render(request, "mobile_add.html", {"form": form})


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",
                               widget=forms.TextInput)
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput)


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        pass
    return render(request, "login.html", {"form": form})


def admin_list(request):
    adminList = models.Admin.objects.all()
    return render(request, "admin_list.html", {"adminList": adminList})
