from django.shortcuts import get_object_or_404
from rest_framework import serializers

from db.models import User, Dishes, Orders, Menu


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_id = self.initial_data['user_id']
        print(user_id)
        instance, _ = User.objects.get_or_create(**validated_data)
        return instance


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data['title']
        shortname = validated_data['shortname']
        description = validated_data['description']
        image = validated_data['image']
        image_id = validated_data['image_id']
        filename = f"media/images/dishes/{validated_data['filename']}.jpg"
        dish = Dishes.objects.create(title=title, shortname=shortname,
                                     description=description, image=image,
                                     image_id=image_id, filename=filename)
        return dish


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        depth = 1


class MenuCreateUpdateSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(many=True,
                                                read_only=False,
                                                queryset=Dishes.objects.all())

    class Meta:
        model = Menu
        fields = '__all__'


class OrdersCreateUpdateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
         queryset=User.objects.all())
    menu_id = serializers.PrimaryKeyRelatedField(
         queryset=Menu.objects.all())

    def create(self, validated_data):
        params = {
            'user': validated_data['user_id'],
            'menu': validated_data['menu_id'],
            'num_of_servings': validated_data['num_of_servings'],
            'payment_type': validated_data['payment_type'],
            'cash_change': validated_data['cash_change'],
            'delivery': validated_data['delivery'],
            'delivery_address': validated_data['delivery_address'],
            'comment': validated_data['comment']
        }
        order = Orders.objects.create(**params)
        return order

    class Meta:
        model = Orders
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menu = MenuSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = '__all__'




