from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from .models import CustomUser, Group, Expense, Category, Settlement
from .serializers import RegisterSerializer, ProfileSerializer, ExpenseSerializer,FetchExpenseSerializer,\
GroupSerializer, SettlementSerializer, CategorySerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from PIL import Image, ImageDraw, ImageFont
import os
from django.core.files.base import ContentFile
import io
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import random


# Create your views here.

def send_otp_to_mail(email, fname, lname):
    body_msg = otp_func()
    subject = 'OTP'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, body_msg, email_from, [email])
    print('mail sent opt')
    return body_msg

def otp_func():
    otp = ''.join(str(random.randint(0, 9)) for _ in range(4))
    timestamp = timezone.now() + timedelta(seconds=30)
    return otp

#Register
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            password = request.data.get("password")
            confirm_password = request.data.get("confirm_password")
            if password != confirm_password:
                return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                "email": request.data.get("email"), 
                "username": request.data.get("username"),
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
                "password": make_password(password),
                "college": request.data.get("college"),
                "semester": request.data.get("semester"),
                "default_payment_methods": request.data.get("default_payment_methods")
            }
            print(data,"data======")
            user_exists = CustomUser.objects.filter(email=data['email']).exists()
            print(user_exists,"=======")
            if user_exists:
                return Response({"message": "USER IS ALREADY EXIST"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                student_data = serializer.save()
                serialized_data = serializer.data
                student_data.otp = send_otp_to_mail(serialized_data['email'], serialized_data['first_name'], serialized_data['last_name'])
                student_data.save()
                return Response({"message": "Signup Successfully and otp sent to your mail please verify"}, status=status.HTTP_201_CREATED)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError as e:
            return Response(
                {"message": "Missing required field", "field": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
#otp verification
class OtpVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request,format=None):
        email = request.data.get("email")
        otp=request.data.get('otp')
        try:
            user_obj= CustomUser.objects.get(email=email)
        except:
            return Response({"message":"USER NOT EXIST"}, status=status.HTTP_400_BAD_REQUEST)
        if otp == user_obj.otp:
            user_obj.otp_verification=True
            user_obj.save()
            return Response({"message":"ACCOUNT VERIFIED"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"WRONG OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
#login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                return Response(
                    {"message": "Username and password are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(email=email, password=password)
            if user is None:
                return Response(
                    {"message": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Fetch profile
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = ProfileSerializer(user)
            return Response(
                {"message": "Profile fetched successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create category
class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = {
                "name": request.data.get("name")
            }
            category = Category.objects.filter(name = data["name"]).exists()
            if category:
                return Response({"message": "category Is Already Exist"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = CategorySerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Category created sucessfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response(
                {"message": "Missing required field", "field": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
#Delete category
class DeleteCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id): 
        try:
            category = Category.objects.get(id=id)
            if not category:
                return Response({"message": "Category is not found"}, status=status.HTTP_404_NOT_FOUND)
            category.delete()
            return Response({"messge": "Category is successfully deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Expense view
class CreateExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def generate_receipt_image(self, expense):
       
        img = Image.new('RGB', (500, 300), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Define text content
        title = f"Expense Receipt"
        details = [
            f"Title: {expense.title}",
            f"Amount: ${expense.amount}",
            f"Category: {expense.category.name}",
            f"Split Type: {expense.split_type}",
            f"Date: {expense.created_at}",
            f"Paid By: {expense.created_by.first_name}",
        ]
        draw.text((20, 20), title, fill=(0, 0, 0)) 
        for i, detail in enumerate(details):
            draw.text((20, 60 + i * 30), detail, fill=(0, 0, 0))

        image_buffer = io.BytesIO()
        img.save(image_buffer, format='PNG')
        image_buffer.seek(0)

        return ContentFile(image_buffer.read(), name=f"receipt_{expense.id}.png")


    def post(self, request):
        try:
            current_user = request.user
            data = {
                "title": request.data.get("title"), 
                "amount": request.data.get("amount"),
                "category": request.data.get("category"),
                "split_type": request.data.get("split_type"),
                "group": request.data.get("group")
            }
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    raise ValueError("Amount should be greater than zero.")
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            category = Category.objects.get(id=data['category'])
            group = Group.objects.get(id=data['group'])

            expense = Expense.objects.create(
                title = data['title'],
                amount = data['amount'],
                category = category,
                split_type = data['split_type'],
                group = group,
                created_by = current_user
            )
            receipt_image = self.generate_receipt_image(expense)
            expense.receipt_image = receipt_image
            expense.save()
            settlement = Settlement.objects.create(
                payment_status = "PENDING",  
                settlement_method="ONLINE",    
                expense = expense,
                settled_by = current_user 
            )
            expense_serializer = ExpenseSerializer(expense)
            settlement_serializer = SettlementSerializer(settlement)

            return Response({
                "message": "Expense and Settlement created successfully.",
                "expense": expense_serializer.data,
                "settlement": settlement_serializer.data
            },status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response(
                {"message": "Missing required field", "field": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Get expense
class FetchExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_user = request.user
            expenses = Expense.objects.filter(created_by=current_user)
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
#Delete Expense
class DeleteExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            current_user = request.user

            expense = Expense.objects.get(id=id, created_by=current_user)
            if not expense:
                return Response(
                    {"message": "Expense does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            expense.delete()
            return Response(
                {"message": "Expense deleted successfully."},
                status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create group
class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_user = request.user
            serializer = GroupSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(created_by = current_user)
                return Response({"message": "Group created successfully.", "group": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 #get group       
class FetchAllGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            current_user = request.user
            groups = Group.objects.filter(created_by=current_user)
            serializer = GroupSerializer(groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
#update group
class UpdateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        try:
            current_user = request.user
            group = Group.objects.get(id=id, created_by=current_user)
            serializer = GroupSerializer(group, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Group updated successfully",
                    "group": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        except Group.DoesNotExist:
            return Response({"message": "Group not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            current_user = request.user

            group = Group.objects.get(id=id, created_by=current_user)
            if not group:
                return Response(
                    {"message": "Group does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            group.delete()
            return Response(
                {"message": "Group deleted successfully."},
                status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

class SettlementListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            settlements = Settlement.objects.filter(settled_by=request.user)
            serializer = SettlementSerializer(settlements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MarkSettlementPaidView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        # settlement_id = request.data.get("settlement_id")
        try:
            settlement = Settlement.objects.get(id=id, settled_by=request.user)
            settlement.payment_status = "COMPLETED"
            settlement.save()
            return Response({"message": "Settlement marked as paid."}, status=status.HTTP_200_OK)
        except Settlement.DoesNotExist:
            return Response({"error": "Settlement not found or unauthorized access."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



