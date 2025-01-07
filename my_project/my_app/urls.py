from django.urls import path
from .views import RegisterView, LoginView, ProfileView, CreateExpenseView,\
FetchExpenseView, DeleteExpenseView, CreateGroupView, FetchAllGroupView, UpdateGroupView, DeleteGroupView,\
CreateCategoryView, DeleteCategoryView,SettlementListView, MarkSettlementPaidView, OtpVerificationView

urlpatterns = [
    #Authentication
    path('auth/register/', RegisterView.as_view(), name = 'register'),
    path('auth/login/', LoginView.as_view(), name = 'login'),
    path('verify_otp/', OtpVerificationView.as_view(), name ='verify-otp'),
    path('fetch/profile/', ProfileView.as_view(), name = 'fetch-profile'),

    #Category
    path('add/category/', CreateCategoryView.as_view(), name = 'add-category'),
    path('remove/category/<int:id>/', DeleteCategoryView.as_view(), name = 'remove-category'),

    #Expenses
    path('create/expense/', CreateExpenseView.as_view(), name = 'create-expense'),
    path('fetch/expenses/', FetchExpenseView.as_view(), name = 'fetch-expense'),
    path('expense/delete/<int:id>/', DeleteExpenseView.as_view(), name = 'delete-expense'),

    # Group
    path('create/group/', CreateGroupView.as_view(), name = 'create-group'),
    path('fetch/groups/', FetchAllGroupView.as_view(), name = 'fetch-all-groups'),
    path('update/group/<int:id>/', UpdateGroupView.as_view(), name = 'update-group'),
    path('remove/group/<int:id>/', DeleteGroupView.as_view(), name = 'remove-group'),

    #settlement
    path('fetch/all/settlements/', SettlementListView.as_view(), name = 'get-settlements'),
    path('mark_settlement_paid/<int:id>/', MarkSettlementPaidView.as_view(), name = 'mark-settlement-paid')

]