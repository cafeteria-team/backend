from django.db import models
from core.models import TimeStampModel
from users.models import User


class Notice(TimeStampModel):
    subject = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    view = models.BooleanField(verbose_name="공개 여부")
    deleted = models.BooleanField(default=False, verbose_name="삭제여부")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="생성자")

    class Meta:
        db_table = "notice"
        verbose_name_plural = "notice"


class NoticeAdmin(TimeStampModel):
    subject = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    view = models.BooleanField(verbose_name="공개 여부")
    deleted = models.BooleanField(default=False, verbose_name="삭제여부")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="생성자")

    class Meta:
        db_table = "notice_admin"
        verbose_name_plural = "notice_admin"
