# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbModel(models.Model):
    target_code = models.CharField(primary_key=True, max_length=20)
    target_num = models.IntegerField()
    model_file_name = models.CharField(max_length=100, blank=True, null=True)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    alg_name = models.CharField(max_length=100, blank=True, null=True)
    create_dtm = models.DateTimeField()
    update_dtm = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tb_model'
        unique_together = (('target_code', 'target_num'),)


class TbSmartopSum(models.Model):
    op_num = models.IntegerField(primary_key=True)
    entry_time = models.FloatField(blank=True, null=True)
    melt_start_time = models.FloatField(blank=True, null=True)
    melt_add_time = models.FloatField(blank=True, null=True)
    refine_time = models.FloatField(blank=True, null=True)
    steel_out_time = models.FloatField(blank=True, null=True)
    total_time = models.FloatField(blank=True, null=True)
    heavy_scrap_a = models.FloatField(blank=True, null=True)
    heavy_scrap_b = models.FloatField(blank=True, null=True)
    light_scrap_a = models.FloatField(blank=True, null=True)
    light_scrap_b = models.FloatField(blank=True, null=True)
    gsa = models.FloatField(blank=True, null=True)
    gsb = models.FloatField(blank=True, null=True)
    gss = models.FloatField(blank=True, null=True)
    mb = models.FloatField(blank=True, null=True)
    lathe_b = models.FloatField(blank=True, null=True)
    scrap_metal_usage = models.FloatField(blank=True, null=True)
    scrap_avg_ton = models.FloatField(blank=True, null=True)
    gravity = models.FloatField(blank=True, null=True)
    power_factor = models.FloatField(blank=True, null=True)
    electric_22kv = models.FloatField(blank=True, null=True)
    melt_first_elec_charge = models.FloatField(blank=True, null=True)
    melt_finish_elec_charge = models.FloatField(blank=True, null=True)
    refine_elec_charge = models.FloatField(blank=True, null=True)
    total_elec_charge = models.FloatField(blank=True, null=True)
    melt_elec_speed = models.FloatField(blank=True, null=True)
    melt_down_carbon_c = models.FloatField(blank=True, null=True)
    briquet_hp = models.FloatField(blank=True, null=True)
    bri_hp2 = models.FloatField(blank=True, null=True)
    elec_fumace_p = models.FloatField(blank=True, null=True)
    elec_fumace_s = models.FloatField(blank=True, null=True)
    elec_fumace_volt = models.FloatField(blank=True, null=True)
    elec_fumace_current = models.FloatField(blank=True, null=True)
    gsk = models.FloatField(blank=True, null=True)
    stain = models.FloatField(blank=True, null=True)
    oxy_bunner = models.FloatField(blank=True, null=True)
    oxy_lance = models.FloatField(blank=True, null=True)
    lance_flux = models.FloatField(blank=True, null=True)
    lance_height = models.FloatField(blank=True, null=True)
    lance_width = models.FloatField(blank=True, null=True)
    lance_til_area = models.FloatField(blank=True, null=True)
    elec_pre_air_vol = models.FloatField(blank=True, null=True)
    elec_pre_dry_degree = models.FloatField(blank=True, null=True)
    elec_pre_dir_degree = models.FloatField(blank=True, null=True)
    master_pos = models.FloatField(blank=True, null=True)
    master_move_distance = models.FloatField(blank=True, null=True)
    melt_elec_1 = models.FloatField(blank=True, null=True)
    melt_elec_2 = models.FloatField(blank=True, null=True)
    melt_elec_3 = models.FloatField(blank=True, null=True)
    elec_put_efficiency = models.FloatField(blank=True, null=True)
    steel_out_vol = models.FloatField(blank=True, null=True)
    product_vol = models.FloatField(blank=True, null=True)
    steel_out_rate = models.FloatField(blank=True, null=True)
    steel_product = models.FloatField(blank=True, null=True)
    create_dtm = models.DateTimeField(blank=True, null=True)
    update_dtm = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_smartop_sum'


class TbTargetValue(models.Model):
    target_num = models.IntegerField(primary_key=True)
    target_value_code = models.CharField(max_length=30, blank=True, null=True)
    target_value_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_target_value'


class TbVarInfo(models.Model):
    target_code = models.CharField(max_length=20, blank=True, null=True)
    target_num = models.IntegerField(blank=True, null=True)
    var_code = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_var_info'


class TbVarMap(models.Model):
    var_code = models.CharField(primary_key=True, max_length=30)
    var_name = models.CharField(max_length=50)
    seq = models.IntegerField()
    var_type = models.CharField(max_length=1, blank=True, null=True)
    is_ess = models.CharField(max_length=1, blank=True, null=True)
    create_dtm = models.DateTimeField()
    update_dtm = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_var_map'
