from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('name','description','price')
        extra_kwargs = {
            'name': {'required': True,},
            'description': {'required': True},
            'price': {'required': True}
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        # Create a Customer instance and associate it with the user
        customer = models.Customer(user=user)
        customer.save()
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'  # Include any additional fields

# In a view or serializer
#customer = models.Customer.objects.get(user=request.user)
#customer_profile_data = CustomerProfileSerializer(customer).data
