from django.db import models
from datetime import datetime


class Device(models.Model):
    """Оборудование"""

    class Meta:
        db_table = 'devices'
        verbose_name = 'Доступное оборудование'
        verbose_name_plural = 'Доступные оборудования'

    manufacturer = models.TextField(verbose_name='Производитель')
    model = models.TextField(verbose_name='Модель')

    def __str__(self):
        return f'{self.manufacturer} {self.model}'


class Customer(models.Model):
    """Конечные пользователи оборудования"""

    class Meta:
        db_table = 'customers'
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'

    customer_name = models.TextField(verbose_name="Наименование организации")
    customer_address = models.TextField(verbose_name="Адрес")
    customer_city = models.TextField(verbose_name="Город")

    def __str__(self):
        return f"{self.customer_name} по адресу: {self.customer_address}"


class DeviceInField(models.Model):
    """Оборудование на объекте"""

    class Meta:
        db_table = 'devices_in_fields'
        verbose_name = 'Оборудование на объекте'
        verbose_name_plural = 'Оборудование на объектах'

    serial_number = models.TextField(verbose_name="Серийный номер")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Пользователь")
    analyzer = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Оборудование")
    owner_status = models.TextField(verbose_name="Статус принадлежности")

    def __str__(self):
        return f"{self.analyzer} с/н {self.serial_number} в {self.customer}"


class Order(models.Model):
    """Описание заявки"""

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    statuses = (("open", "открыта"),
                ("closed", "закрыта"),
                ("in progress", "в работе"),
                ("need info", "нужна информация"))

    device = models.ForeignKey(DeviceInField, verbose_name="Оборудование", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="Описание")
    created_dt = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    last_updated_dt = models.DateTimeField(verbose_name="Последнее изменение", blank=True, null=True)
    order_status = models.TextField(verbose_name="Статус заявки", choices=statuses)

    def __str__(self):
        return f"Заявка №{self.id} для {self.device}"

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)
