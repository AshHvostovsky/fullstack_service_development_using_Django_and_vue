from rest_framework import serializers
from missions.models import Mission, SpaceProgram, MissionType, LaunchSite, SpaceCraft
from django.contrib.auth.models import User
# Сериалайзер для космической программы
class SpaceProgramSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)  
    class Meta:
        model = SpaceProgram
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'user']

# Сериалайзер для типа миссии
class MissionTypeSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)  
    class Meta:
        model = MissionType
        fields = ['id', 'name', 'user']

# Сериалайзер для места запуска
class LaunchSiteSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)  
    class Meta:
        model = LaunchSite
        fields = ['id', 'name', 'location', "picture", "user"]

# Сериалайзер для космического аппарата
class SpaceCraftSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)  
    launch_site = serializers.PrimaryKeyRelatedField(queryset=LaunchSite.objects.all())
    mission = serializers.PrimaryKeyRelatedField(queryset=Mission.objects.all())


    # launch_site = LaunchSiteSerializer(read_only=True)
    # mission = serializers.PrimaryKeyRelatedField(queryset=Mission.objects.all())

    class Meta:
        model = SpaceCraft
        fields = ['id', 'name', 'manufacturer', 'launch_site', 'mission', "picture", "user"]

# Сериалайзер для миссии
class MissionSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        # когда в api создается сериалайзер, 
        # то заполняется специальное поле сериалайзера которое называется context
        # в него добавляется инфомрация по запросе, и доступна эта инфа
        # через self.context['request'], в частности там есть информация о пользовате
        if 'request' in self.context:
            # заполняем validated_data который используется для создания сущности в БД
            # данными из запроса
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)  
    
    space_program = serializers.PrimaryKeyRelatedField(queryset=SpaceProgram.objects.all())
    mission_type = serializers.PrimaryKeyRelatedField(queryset=MissionType.objects.all())

    # space_program = SpaceProgramSerializer(read_only=True, source='space_program_set')
    # mission_type = MissionTypeSerializer(read_only=True, source='mission_type_set')

    # space_program = SpaceProgramSerializer(many=True, read_only=True, source='space_program_set')
    # mission_type = MissionTypeSerializer(many=True, read_only=True, source='mission_type_set')

    #spacecrafts = SpaceCraftSerializer(many=True, read_only=True, source='spacecraft_set')

    class Meta:
        model = Mission
        fields = ['id', 'name', 'launch_date', 'outcome', 'description', 'space_program', 'mission_type', "user"]  #'spacecrafts'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password'] #добавил пароль


# class MissionSerializer(serializers.ModelSerializer):
#     space_program = serializers.PrimaryKeyRelatedField(queryset=SpaceProgram.objects.all(), write_only=True)
#     mission_type = serializers.PrimaryKeyRelatedField(queryset=MissionType.objects.all(), write_only=True, many=True)
#     space_program_detail = SpaceProgramSerializer(read_only=True, source='space_program')
#     mission_type_detail = MissionTypeSerializer(many=True, read_only=True, source='mission_type_set')

#     class Meta:
#         model = Mission
#         fields = ['id', 'name', 'launch_date', 'outcome', 'description', 'space_program', 'mission_type', 'space_program_detail', 'mission_type_detail']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         # Удаляем записываемые поля при получении объекта
#         data.pop('space_program', None)
#         data.pop('mission_type', None)
#         return data