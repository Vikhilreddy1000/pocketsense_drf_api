from rest_framework import serializers
from .models import CustomUser, Expense, Group, Category, Settlement

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','username','first_name','last_name', 'college', 'semester', 'default_payment_methods', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',  'email', 'username', 'first_name', 'last_name', 'college', 'semester', 'default_payment_methods']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']



class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'category', 'split_type', 'group', 'receipt_image', 'created_by', 'created_at']

        
class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ['id', 'payment_status', 'settlement_method', 'due_date', 'expense', 'settled_by']

class FetchExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'category', 'split_type', 'group', 'created_by']


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

        def create(self, validated_data):
            members = validated_data.pop('members', [])
            group = Group.objects.create(**validated_data)
            group.members.set(members)
            return group


