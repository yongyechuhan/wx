from django.db import models

class NoticerInfo(models.Model):
    open_id = models.CharField(max_length=50,primary_key=True)
    nick_name = models.CharField(max_length=60)
    user_head_img = models.CharField(max_length=80)
    user_local_addr = models.CharField(max_length=100)

class PaintingInfo(models.Model):
    open_id = models.ForeignKey(NoticerInfo)
    pic_name = models.CharField(max_length=60)
    pic_src = models.CharField(max_length=60)
    share_time = models.DateTimeField()



