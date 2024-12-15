from django.db import models

# Create your models here.
class Mission(models.Model):
    name = models.TextField("Название миссии")
    launch_date = models.TextField("Дата запуска")
    outcome = models.TextField("Исход")
    description = models.TextField("Описание")
    space_program = models.ForeignKey("SpaceProgram", on_delete=models.CASCADE, null = True)
    mission_type = models.ForeignKey("MissionType", on_delete=models.CASCADE, null = True)

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null = True)

    
    class Meta:
        verbose_name = "Миссия"
        verbose_name_plural = "Миссии"
    def __str__(self) -> str:
        return self.name

class SpaceProgram(models.Model):
    name = models.TextField("Название программы")
    start_date = models.TextField("Дата старта")
    end_date = models.TextField("Дата окончания")
    description = models.TextField("Описание")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null = True)

    class Meta:
        verbose_name = "Космическая программа"
        verbose_name_plural = "Космические программы"
    def __str__(self) -> str:
        return self.name
    
class MissionType(models.Model):
    name = models.TextField("Название")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null = True)

    class Meta:
        verbose_name = "Тип миссии"
        verbose_name_plural = "Типы миссий"
    def __str__(self) -> str:
        return self.name

class LaunchSite(models.Model):
    name = models.TextField("Название")
    location = models.TextField("Местоположение")

    picture = models.ImageField("Изображение", null=True, upload_to="missions")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null = True)
    
    class Meta:
        verbose_name = "Место запуска"
        verbose_name_plural = "Места запуска"
    def __str__(self) -> str:
        return self.name

class SpaceCraft(models.Model):
    name = models.TextField("Название")
    manufacturer = models.TextField("Изготовитель")
    launch_site = models.ForeignKey("LaunchSite", on_delete=models.CASCADE, null = True)
    mission = models.ForeignKey("Mission", on_delete=models.CASCADE, null = True)

    picture = models.ImageField("Изображение", null=True, upload_to="missions")

    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null = True)

    class Meta:
        verbose_name = "Космический аппарат"
        verbose_name_plural = "Космические аппараты"
    def __str__(self) -> str:
        return self.name




