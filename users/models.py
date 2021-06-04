from django.db import models

# Create your models here.
class TBUsers(models.Model):
    user_id = models.CharField(max_length=20, verbose_name='사용자ID',primary_key=True)
    password = models.CharField(max_length=50,verbose_name='비밀번호',blank=False)
    user_name = models.CharField(max_length=20, verbose_name='이 름',blank=False)
    email_addr = models.EmailField(max_length=50, verbose_name='이 메일',blank=True)
    phone_number = models.CharField(max_length=20, verbose_name='전화번호',blank=False)
    user_level = models.IntegerField(default=0)

    create_id = models.CharField(max_length=20,blank=False)
    update_id = models.CharField(max_length=20,blank=False)
    create_dtm = models.DateTimeField(auto_now_add=True)
    update_dtm = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user_name, self.user_name)

    class Meta:
        managed = True
        db_table = 'tb_users'
        verbose_name = '한국철강제강 사용자'
        verbose_name_plural = '한국철강제강 사용자'