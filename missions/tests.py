from django.test import TestCase
from rest_framework.test import APIClient
from missions.models import *
from model_bakery import baker 
# Create your tests here.
class MissionsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        prg = baker.make("missions.SpaceProgram")
        msn = baker.make("Mission", space_program=prg)
        
        r = self.client.get('/api/missions/') 
        data = r.json()

        assert msn.name == data[0]['name']
        assert msn.id == data[0]['id']
        assert msn.space_program.id == data[0]['space_program']

        assert len(data) == 1

    def test_create_mission(self):
        prg = baker.make("missions.SpaceProgram")
        mt = baker.make("missions.MissionType")

        r = self.client.post("/api/missions/", {
            "name": "Миссия",
            "launch_date": "Дата старта",
            "end_date": "Дата окончания",
            "outcome": "Исход",
            "description": "Описание",
            "space_program": prg.id,
            "mission_type": mt.id
        })
        print(r.json())
        self.assertEqual(r.status_code, 201)  # Убедимся, что объект успешно создан

        new_mission_id = r.json()['id']
        missions = Mission.objects.all()
        assert len(missions) == 1

        new_mission = Mission.objects.filter(id=new_mission_id).first()
        assert new_mission.name == 'Миссия'
        assert new_mission.space_program == prg
        assert new_mission.mission_type == mt

    def test_delete_mission(self):
        missions = baker.make("Mission", 10)
        r = self.client.get('/api/missions/')
        data = r.json()
        assert len(data) == 10

        mission_id_to_delete = missions[3].id
        self.client.delete(f'/api/missions/{mission_id_to_delete}/')

        r = self.client.get('/api/missions/')
        data = r.json()
        assert len(data) == 9

        assert mission_id_to_delete not in [i['id'] for i in data]

    def test_update_mission(self):
        prg = baker.make("missions.SpaceProgram")
        mt = baker.make("missions.MissionType")
        msns = baker.make("Mission", 10)
        msn : LaunchSite = msns[2]

        r = self.client.get(f'/api/missions/{msn.id}/')
        data = r.json()
        assert data['name'] == msn.name

        r = self.client.put(f'/api/missions/{msn.id}/', {
            "name": "Миссия",
            "launch_date": "Дата старта",
            "end_date": "Дата окончания",
            "outcome": "Исход",
            "description": "Описание",
            "space_program": prg.id,
            "mission_type": mt.id
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/missions/{msn.id}/')
        data = r.json()
        assert data['name'] == "Миссия"

        msn.refresh_from_db()
        assert data['name'] == msn.name



class SpaceProgramViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        prg = baker.make("missions.SpaceProgram")

        r = self.client.get('/api/spaceprograms/') 
        data = r.json()

        assert prg.name == data[0]['name']
        assert prg.id == data[0]['id']

        assert len(data) == 1
    def test_create_program(self):
        r = self.client.post("/api/spaceprograms/", {
            "name": "Космическая программа",
            "start_date": "Дата старта",
            "end_date": "Дата окончания",
            "description": "Исход",
        })
        self.assertEqual(r.status_code, 201)  # Убедимся, что объект успешно создан

        new_program_id = r.json()['id']
        programs = SpaceProgram.objects.all()
        assert len(programs) == 1

        new_program = SpaceProgram.objects.filter(id=new_program_id).first()
        assert new_program.name == 'Космическая программа'

    def test_delete_program(self):
        programs = baker.make("SpaceProgram", 10)
        r = self.client.get('/api/spaceprograms/')
        data = r.json()
        assert len(data) == 10

        program_id_to_delete = programs[3].id
        self.client.delete(f'/api/spaceprograms/{program_id_to_delete}/')

        r = self.client.get('/api/spaceprograms/')
        data = r.json()
        assert len(data) == 9

        assert program_id_to_delete not in [i['id'] for i in data]

    def test_update_program(self):
        programs = baker.make("SpaceProgram", 10)
        program : SpaceProgram = programs[2]

        r = self.client.get(f'/api/spaceprograms/{program.id}/')
        data = r.json()
        assert data['name'] == program.name

        r = self.client.put(f'/api/spaceprograms/{program.id}/', {
            "name": "Космическая программа",
            "start_date": "Дата старта",
            "end_date": "Дата окончания",
            "description": "Исход",
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/spaceprograms/{program.id}/')
        data = r.json()
        assert data['name'] == "Космическая программа"

        program.refresh_from_db()
        assert data['name'] == program.name


class MissionTypeViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        mt = baker.make("missions.MissionType")

        r = self.client.get('/api/missiontypes/') 
        data = r.json()

        assert mt.name == data[0]['name']
        assert mt.id == data[0]['id']

    def test_create_mission_type(self):
        r = self.client.post("/api/missiontypes/", {
            "name": "Тип миссии",
        })
        self.assertEqual(r.status_code, 201)  # Убедимся, что объект успешно создан

        new_type_id = r.json()['id']
        types = MissionType.objects.all()
        assert len(types) == 1

        new_type = MissionType.objects.filter(id=new_type_id).first()
        assert new_type.name == 'Тип миссии'

    def test_delete_mission_type(self):
        types = baker.make("MissionType", 10)
        r = self.client.get('/api/missiontypes/')
        data = r.json()
        assert len(data) == 10

        type_id_to_delete = types[3].id
        self.client.delete(f'/api/missiontypes/{type_id_to_delete}/')

        r = self.client.get('/api/missiontypes/')
        data = r.json()
        assert len(data) == 9

        assert type_id_to_delete not in [i['id'] for i in data]
        
    def test_update_type(self):
        mtypes = baker.make("MissionType", 10)
        mtype : MissionType = mtypes[2]

        r = self.client.get(f'/api/missiontypes/{mtype.id}/')
        data = r.json()
        assert data['name'] == mtype.name

        r = self.client.put(f'/api/missiontypes/{mtype.id}/', {
            "name": "Тип миссии",
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/missiontypes/{mtype.id}/')
        data = r.json()
        assert data['name'] == "Тип миссии"

        mtype.refresh_from_db()
        assert data['name'] == mtype.name

class LaunchSiteViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        ls = baker.make("missions.LaunchSite")

        r = self.client.get('/api/launchsites/') 
        data = r.json()

        assert ls.name == data[0]['name']
        assert ls.location == data[0]['location']
        assert ls.id == data[0]['id']

    def test_create_launch_site(self):
        r = self.client.post("/api/launchsites/", {
            "name": "Название места запуска",
            "location" : "Местоположение",
        })
        self.assertEqual(r.status_code, 201)  # Убедимся, что объект успешно создан

        new_site_id = r.json()['id']
        sites = LaunchSite.objects.all()
        assert len(sites) == 1

        new_site = LaunchSite.objects.filter(id=new_site_id).first()
        assert new_site.name == 'Название места запуска'
        assert new_site.location == 'Местоположение'

    def test_delete_launch_site(self):
        sites = baker.make("LaunchSite", 10)
        r = self.client.get('/api/launchsites/')
        data = r.json()
        assert len(data) == 10

        site_id_to_delete = sites[3].id
        self.client.delete(f'/api/launchsites/{site_id_to_delete}/')

        r = self.client.get('/api/launchsites/')
        data = r.json()
        assert len(data) == 9

        assert site_id_to_delete not in [i['id'] for i in data]

    def test_update_site(self):
        sites = baker.make("LaunchSite", 10)
        site : LaunchSite = sites[2]

        r = self.client.get(f'/api/launchsites/{site.id}/')
        data = r.json()
        assert data['name'] == site.name

        r = self.client.put(f'/api/launchsites/{site.id}/', {
            "name": "Место запуска",
            "location" : "Местоположение",
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/launchsites/{site.id}/')
        data = r.json()
        assert data['name'] == "Место запуска"

        site.refresh_from_db()
        assert data['name'] == site.name

class SpaceCraftViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        ls = baker.make("missions.LaunchSite")
        msn = baker.make("missions.Mission")
        sc = baker.make("SpaceCraft", launch_site = ls, mission = msn)
        
        r = self.client.get('/api/spacecrafts/') 
        data = r.json()

        assert sc.name == data[0]['name']
        assert sc.id == data[0]['id']
        assert sc.launch_site.id == data[0]['launch_site']
        assert sc.mission.id == data[0]['mission']

        assert len(data) == 1
    def test_create_craft(self):
        ls = baker.make("missions.LaunchSite")
        msn = baker.make("missions.Mission")
        r = self.client.post("/api/spacecrafts/", {
            "name": "Аппарат",
            "manufacturer" : "Изготовитель",
            "launch_site": ls.id,
            "mission": msn.id
        })
        print(r.json())
        self.assertEqual(r.status_code, 201)  # Убедимся, что объект успешно создан

        new_craft_id = r.json()['id']
        crafts = SpaceCraft.objects.all()
        assert len(crafts) == 1

        new_craft = SpaceCraft.objects.all().filter(id=new_craft_id).first()
        assert new_craft.name == 'Аппарат'
        assert new_craft.manufacturer == "Изготовитель"
        assert new_craft.launch_site == ls
        assert new_craft.mission == msn

    def test_delete_craft(self):
        crafts = baker.make("SpaceCraft", 10)
        r = self.client.get('/api/spacecrafts/')
        data = r.json()
        assert len(data) == 10

        craft_id_to_delete = crafts[3].id
        self.client.delete(f'/api/spacecrafts/{craft_id_to_delete}/')

        r = self.client.get('/api/spacecrafts/')
        data = r.json()
        assert len(data) == 9

        assert craft_id_to_delete not in [i['id'] for i in data]

    def test_update_craft(self):
        ls = baker.make("missions.LaunchSite")
        msn = baker.make("missions.Mission")
        crafts = baker.make("SpaceCraft", 10)
        craft : SpaceCraft = crafts[2]

        r = self.client.get(f'/api/spacecrafts/{craft.id}/')
        data = r.json()
        assert data['name'] == craft.name

        r = self.client.put(f'/api/spacecrafts/{craft.id}/', {
            "name": "Аппарат",
            "manufacturer" : "Изготовитель",
            "launch_site": ls.id,
            "mission": msn.id
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/spacecrafts/{craft.id}/')
        data = r.json()
        assert data['name'] == "Аппарат"

        craft.refresh_from_db()
        assert data['name'] == craft.name









        # prg = SpaceProgram.objects.create(
        #     name="Voyager Program",
        #     start_date = "1972-01-01",
        #     end_date = "Оngoing",
        #     description = "Космическая программа NASA по запуску двух автоматических межпланетных зондов 'Voyager 1' и 'Voyager 2' для исследования внешних планет Солнечной системы и межзвездного пространства. Миссии продолжаются, предоставляя данные о межзвездной среде после выхода аппаратов за пределы гелиосферы.",
        # )
        # msn = Mission.objects.create(
        #     name = "Voyager 1",
        #     launch_date = "1977-09-05",
        #     outcome = "Успешно",
        #     description = "Беспилотная межпланетная космическая миссия NASA, запущенная для исследования внешней части Солнечной системы и межзвездного пространства. 'Вояджер 1' достиг Юпитера в 1979 году и Сатурна в 1980 году, предоставив важные данные и фотографии этих планет. В 2012 году 'Вояджер 1' стал первым космическим аппаратом, вышедшим в межзвездное пространство.",
        #     space_program = prg,
        # )
        # ls = LaunchSite.objects.create(
        #     name="Космический центр Кеннеди (Kennedy Space Center)",
        #     location = "Остров Мерритт, Флорида, США",
        # )
        # sc = SpaceCraft.objects.create(
        #     name="Voyager 1",
        #     manufacturer = "Jet Propulsion Laboratory (JPL), NASA",
        #     launch_site = ls,
        #     mission = msn,
        # )
        # r = self.client.get('/api/spacecrafts/') 
        # data = r.json()
        # print(data)
        # self.assertEqual(data[0]['name'], sc.name)  # Проверяем имя SpaceCraft
        # self.assertEqual(data[0]['id'], sc.id)  # Проверяем ID SpaceCraft
        # self.assertEqual(data[0]['manufacturer'], sc.manufacturer)  # Проверяем производителя
        # self.assertEqual(data[0]['launch_site']['id'], ls.id)  # Проверяем ID LaunchSite
        # self.assertEqual(data[0]['launch_site']['name'], ls.name)  # Проверяем имя LaunchSite
        # self.assertEqual(data[0]['launch_site']['location'], ls.location)  # Проверяем местоположение LaunchSite
        # self.assertEqual(data[0]['mission'], msn.id)  # Проверяем ID Mission
        # assert len(data) == 1
        
        




# prg = SpaceProgram.objects.create(
        #     name="Название",
        #     start_date = "дата старта",
        #     end_date = "дата окончания",
        #     description = "Описание",
        # )
        # mt = MissionType.objects.create(
        #     name = "Название"
        # )


         # print(data)
        # self.assertEqual(data[0]['name'], prg.name)
        # self.assertEqual(data[0]['id'], prg.id)
        # self.assertEqual(data[0]['start_date'], prg.start_date)
        # self.assertEqual(data[0]['end_date'], prg.end_date)
        # self.assertEqual(data[0]['description'], prg.description)       


 # prg = SpaceProgram.objects.create(
        #     name="Название",
        #     start_date = "дата старта",
        #     end_date = "дата окончания",
        #     description = "Описание",
        # )
        # mt = MissionType.objects.create(
        #     name = "Название"
        # )

# self.assertEqual(data[0]['name'], msn.name)
        # self.assertEqual(data[0]['id'], msn.id)
        # self.assertEqual(data[0]['space_program']['id'], prg.id)  # Сравниваем ID вложенного объекта
        # self.assertEqual(data[0]['space_program']['name'], prg.name)

# def test_get_list(self):
    #     prg = SpaceProgram.objects.create(
    #         name="Voyager Program",
    #         start_date = "1972-01-01",
    #         end_date = "Оngoing",
    #         description = "Космическая программа NASA по запуску двух автоматических межпланетных зондов 'Voyager 1' и 'Voyager 2' для исследования внешних планет Солнечной системы и межзвездного пространства. Миссии продолжаются, предоставляя данные о межзвездной среде после выхода аппаратов за пределы гелиосферы.",
    #     )
    #     msn = Mission.objects.create(
    #         name = "Voyager 1",
    #         launch_date = "1977-09-05",
    #         outcome = "Успешно",
    #         description = "Беспилотная межпланетная космическая миссия NASA, запущенная для исследования внешней части Солнечной системы и межзвездного пространства. 'Вояджер 1' достиг Юпитера в 1979 году и Сатурна в 1980 году, предоставив важные данные и фотографии этих планет. В 2012 году 'Вояджер 1' стал первым космическим аппаратом, вышедшим в межзвездное пространство.",
    #         space_program = prg,
    #     )




        # prg = SpaceProgram.objects.create(
        #     name="Voyager Program",
        #     start_date = "1972-01-01",
        #     end_date = "Оngoing",
        #     description = "Космическая программа NASA по запуску двух автоматических межпланетных зондов 'Voyager 1' и 'Voyager 2' для исследования внешних планет Солнечной системы и межзвездного пространства. Миссии продолжаются, предоставляя данные о межзвездной среде после выхода аппаратов за пределы гелиосферы.",
        # )


        # mission_type = MissionType.objects.create(
        #     name = "Научная миссия (Scientific Mission)"
        # )
        # launch_site = LaunchSite.objects.create(
        #     name = "Космический центр Кеннеди (Kennedy Space Center)",
        #     location = "Остров Мерритт, Флорида, США",
        # )
        # space_craft = SpaceCraft.objects.create(
        #     name = "Voyager 1",
        #     manufacturer = "Jet Propulsion Laboratory (JPL), NASA",
        #     launch_site = launch_site,
        #     mission = mission,
        # )


# from django.db import models

# # Create your models here.
# class Mission(models.Model):
#     name = models.TextField("Название миссии")
#     launch_date = models.TextField("Дата запуска")
#     outcome = models.TextField("Исход")
#     description = models.TextField("Описание")
#     space_program = models.ForeignKey("SpaceProgram", on_delete=models.CASCADE, null = True)
#     mission_type = models.ForeignKey("MissionType", on_delete=models.CASCADE, null = True)
    
#     class Meta:
#         verbose_name = "Миссия"
#         verbose_name_plural = "Миссии"
#     def __str__(self) -> str:
#         return self.name

# class SpaceProgram(models.Model):
#     name = models.TextField("Название программы")
#     start_date = models.TextField("Дата старта")
#     end_date = models.TextField("Дата окончания")
#     description = models.TextField("Описание")

#     class Meta:
#         verbose_name = "Космическая программа"
#         verbose_name_plural = "Космические программы"
#     def __str__(self) -> str:
#         return self.name
    
# class MissionType(models.Model):
#     name = models.TextField("Название")
#     class Meta:
#         verbose_name = "Тип миссии"
#         verbose_name_plural = "Типы миссий"
#     def __str__(self) -> str:
#         return self.name

# class LaunchSite(models.Model):
#     name = models.TextField("Название")
#     location = models.TextField("Местоположение")
#     class Meta:
#         verbose_name = "Место запуска"
#         verbose_name_plural = "Места запуска"
#     def __str__(self) -> str:
#         return self.name

# class SpaceCraft(models.Model):
#     name = models.TextField("Название")
#     manufacturer = models.TextField("Изготовитель")
#     launch_site = models.ForeignKey("LaunchSite", on_delete=models.CASCADE, null = True)
#     mission = models.ForeignKey("Mission", on_delete=models.CASCADE, null = True)
#     class Meta:
#         verbose_name = "Космический аппарат"
#         verbose_name_plural = "Космические аппараты"
#     def __str__(self) -> str:
#         return self.name




