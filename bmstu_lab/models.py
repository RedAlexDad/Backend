from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Пользователь
class Users(AbstractUser):
    username = models.CharField(max_length=255, unique=True, verbose_name="Никнейм")
    password = models.CharField(max_length=255, verbose_name="Пароль")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    def str(self):
        return self.username

# Начальник (ПРИНМАЮЩИЙ ЗАКАЗЧИКА) и Ученые (ЗАКАЗЧИК)
class Employee(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    full_name = models.CharField(max_length=255)
    post = models.CharField(max_length=255)
    name_organization = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    # Добавляем внешний ключ к другой модели
    id_user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_user',  # Имя поля в базе данных
    )
    class Meta:
        managed = False
        db_table = 'employee'

# Географический объект (услуга)
class GeographicalObject(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    feature = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    size = models.IntegerField(null=True, blank=True)
    describe = models.CharField(max_length=1000, null=True, blank=True)
    url_photo = models.CharField(max_length=1000, null=True, blank=True)
    # blank=True позволяет сохранять поле как пустое, если оно не было заполнено.
    # null=True позволяет полю принимать значение None (null), что полезно, если вы хотите, чтобы поле могло иметь отсутствующее значение.
    # editable=True позволяет редактировать это поле через административный интерфейс Django или другие методы редактирования, если это необходимо.
    photo_byte = models.BinaryField(blank=True, null=True, editable=True)
    status = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'geographical_object'

# Транспорт (доп. информация для услуги)
class Transport(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    describe = models.CharField(max_length=1000, null=True, blank=True)
    url_photo = models.CharField(max_length=1000, null=True, blank=True)
    # blank=True позволяет сохранять поле как пустое, если оно не было заполнено.
    # null=True позволяет полю принимать значение None (null), что полезно, если вы хотите, чтобы поле могло иметь отсутствующее значение.
    # editable=True позволяет редактировать это поле через административный интерфейс Django или другие методы редактирования, если это необходимо.
    photo_byte = models.BinaryField(blank=True, null=True, editable=True)
    class Meta:
        managed = False
        db_table = 'transport'

# Марсианская станция (заявка)
class MarsStation(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    type_status = models.CharField(max_length=255)
    date_create = models.DateField()
    date_form = models.DateField()
    date_close = models.DateField()
    # Добавляем внешний ключ к другой модели
    id_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_employee',  # Имя поля в базе данных
        related_name='id_employee_by_table_employee'
    )
    id_moderator = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_moderator',  # Имя поля в базе данных
        related_name='id_moderator_by_table_employee'
    )
    id_transport = models.ForeignKey(
        Transport,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_transport',  # Имя поля в базе данных
    )
    status_task = models.IntegerField()
    status_mission = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'mars_station'


# Местоположение (вспомогательная таблица)
class Location(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    # Добавляем внешний ключ к другой модели
    id_geographical_object = models.ForeignKey(
        GeographicalObject,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_geographical_object',  # Имя поля в базе данных
    )

    id_mars_station = models.ForeignKey(
        MarsStation,
        on_delete=models.CASCADE,  # Это действие, которое будет выполнено при удалении связанной записи
        db_column='id_mars_station',  # Имя поля в базе данных
        related_name='id_mars_station_location',  # Пользовательское имя
    )
    class Meta:
        managed = False
        db_table = 'location'