from django.db import models


# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    password = models.CharField(max_length=64, verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="账户")
    create_time = models.DateField(default=2022 - 10 - 20, verbose_name="入职时间")
    department = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE, default=1,
                                   verbose_name="部门")
    gender_chioces = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(choices=gender_chioces, default=1, verbose_name="性别")


class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
        (5, "5级")
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=1)
    status_choices = (
        (1, "未使用"),
        (2, "已使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)


class Admin(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
