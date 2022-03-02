from django.contrib import admin
from django.urls import path, include
from share.models import MemberAmount
from share.views import AccountApiView, AccountDetail, SearchAccount, AccountEkips, EkipApiView, EkipDetail, \
    EkipExpenseApi, ExpenseApiView, ExpenseDetail, ShareDetail, AccountShareApi, EkipShareApi, SignUpView, LoginView, \
    LogoutView, EkipMemberApi, AccountFriendsApi, FriendsApiView, UnFriend, AccountCreditorApi, Creditor, Obligor, \
    PayDebtor, EkipInvite, Invielink, MemberAmountApiView, MemberAmountDetail

app_name = 'share'
urlpatterns = [
    path('signup', SignUpView, name='signup'),
    path('login', LoginView, name='login'),
    path('logout', LogoutView, name='logout'),

    path('account', AccountApiView.as_view(), name='AccountApi'),
    path('account/<int:pk>/', AccountDetail.as_view(), name='AccountDetail'),
    path('search/<str:search>/', SearchAccount.as_view(), name='SearchAccountApi'),
    path('account/ekip/<int:pk>/', AccountEkips.as_view(), name='AccountEkips'),
    path('account/share/<int:pk>/', AccountShareApi.as_view(), name='AccountShares'),
    path('account/creditor/<int:pk>/', AccountCreditorApi.as_view(), name='AccountCreditor'),
    path('account/friends/<int:pk>/', AccountFriendsApi.as_view(), name='AccountFriends'),
    path('debtor/pay/<int:pk>/<int:pk1>/', PayDebtor.as_view(), name='payAllDebtor'),
    path('invite/ekip/<int:pk>/<str:token>/', EkipInvite.as_view(), name='EkipInvite'),

    path('friends', FriendsApiView.as_view(), name='FriendsApi'),
    path('unfriend/<int:pk>/<int:accid>/', UnFriend.as_view(), name='unfriend'),
    path('creditor/<int:pk>/', Creditor.as_view(), name='creditor'),
    path('obligor/<int:pk>/<int:pk1>/', Obligor.as_view(), name='obligor'),

    path('ekip', EkipApiView.as_view(), name='EkipApi'),
    path('ekip/<int:pk>/', EkipDetail.as_view(), name='EkipDetailView'),
    path('ekip/share/<int:pk>/', EkipShareApi.as_view(), name='EkipShares'),
    path('ekip/member/<int:pk>/', EkipMemberApi.as_view(), name='Ekipmembers'),

    path('expense', ExpenseApiView.as_view(), name='ExpenseApi'),
    path('expense/ekip/<int:pk>/', EkipExpenseApi.as_view(), name='EkipExpenses'),
    path('expense/<int:pk>/', ExpenseDetail.as_view(), name='ExpensesDetail'),

    path('share/<int:pk>/', ShareDetail.as_view(), name='ShareDetail'),
    path('invite/<str:token>/', Invielink.as_view(), name='invite'),

    path('membershare', MemberAmountApiView.as_view(), name='MemberAmountApi'),
    path('membershare/<int:pk>/', MemberAmountDetail.as_view(), name='MemberAmountDetail'),

]
