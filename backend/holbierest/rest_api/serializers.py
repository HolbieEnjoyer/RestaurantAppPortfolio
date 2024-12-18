from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Category, MenuItem, Cart, Order, OrderItem, Reservation, Review, CustomUser


# Get the custom user model
User = get_user_model()

class CustomUserSerializer(DjoserUserSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_staff', 'groups', 'bonus_earned', 'tip', 'phone_number', 'address', 'date_of_birth')

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    # category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured', 'image']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    menuitem = MenuItemSerializer()  # Use MenuItemSerializer to include all fields

    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()  # Use MenuItemSerializer to include all fields
    
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(read_only=True)
    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']
        
    def create(self, validated_data):
        # Set the user as the logged-in user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



class ReviewSerializer(serializers.ModelSerializer):
    # Display user details (id and username)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'menu_item', 'rating', 'comment', 'created_at']

    def create(self, validated_data):
        # Set the user as the logged-in user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'phone_number', 'number_of_guests', 'message']