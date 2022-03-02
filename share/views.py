from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from share.models import Ekip, Expense, Share, Friends, User, MemberAmount
from share.serializers import EkipSerializer, ExpenseSerializer, ShareSerializer, FriendSerializer, \
    FriendsSerializer, UserSerializer, MemberAmountSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, Http404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate, forms
from django.views.decorators.csrf import csrf_exempt


class AccountApiView(APIView):
    def get(self, request):
        query = User.objects.all()
        serializer = UserSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.filter(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializer = UserSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = User.objects.filter(pk=pk).first()
        serializer = UserSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchAccount(APIView):
    def get_object(self, search):
        return User.objects.filter(Q(first_name__contains=search) | Q(last_name__contains=search))

    def get(self, request, search):
        query = self.get_object(search)
        serializers = UserSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


# Api to get all ekips of an account
class AccountEkips(APIView):
    def get_object(self, pk):
        return Ekip.objects.filter(member__id=pk)

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = EkipSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class FriendsApiView(APIView):
    def post(self, request):
        serializer = FriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnFriend(APIView):
    def get_object(self, pk, accid):
        try:
            myaccount = User.objects.get(pk=accid)
            myfriend = User.objects.get(pk=pk)
            return Friends.objects.get(account=myaccount, friends=myfriend)
        except Friends.DoesNotExist:
            raise Http404

    def get(self, request, pk, accid):
        query = self.get_object(pk, accid)
        serializers = FriendSerializer(query)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, accid):
        query = self.get_object(pk, accid)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountFriendsApi(APIView):
    def get(self, request, pk):
        account = User.objects.get(pk=pk)
        friends = Friends.objects.filter(account=account)
        serializers = FriendsSerializer(friends, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class EkipApiView(APIView):
    def get(self, request):
        query = Ekip.objects.all()
        serializer = EkipSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EkipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EkipDetail(APIView):
    def get_object(self, pk):
        try:
            return Ekip.objects.filter(pk=pk)
        except Ekip.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializer = EkipSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = Ekip.objects.filter(pk=pk).first()
        serializer = EkipSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Api to get all expenses of an ekip
class EkipExpenseApi(APIView):
    def get_object(self, pk):
        return Expense.objects.filter(ekip=pk)

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ExpenseSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


class ExpenseApiView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetail(APIView):
    def get_object(self, pk):
        try:
            return Expense.objects.filter(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializer = ExpenseSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        expense = Expense.objects.filter(pk=pk).first()
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            old_amount = expense.amount
            new_amount = request.data['amount']
            new_debtor = new_amount / expense.ekip.member.count()
            new_debtor = round(new_debtor, 2)
            change_amount = (new_amount - old_amount) / expense.ekip.member.count()
            new_payer_id = request.data['payer']
            new_payer = User.objects.get(pk=new_payer_id)
            ekip = expense.ekip
            if expense.equal_share == True:
                if new_payer == expense.payer:
                    for member in ekip.member.all():
                        if member == new_payer:
                            continue
                        else:
                            if not Share.objects.filter(account=member, creditor=new_payer, ekip=ekip) and \
                                    not Share.objects.filter(account=new_payer, creditor=member, ekip=ekip):
                                share = Share.objects.create(account=member, creditor=new_payer, ekip=ekip,
                                                             debtor=new_debtor)
                                share.save()
                            elif Share.objects.filter(account=member, creditor=new_payer, ekip=ekip):
                                share1 = Share.objects.get(account=member, creditor=new_payer, ekip=ekip)
                                share1.debtor += change_amount
                                if share1.debtor == 0:
                                    share1.delete()
                                elif share1.debtor < 0:
                                    share1.account = new_payer
                                    share1.creditor = member
                                    share1.debtor = -share1.debtor
                                    share1.save()
                                share1.save()
                            elif Share.objects.filter(account=new_payer, creditor=member, ekip=ekip):
                                share2 = Share.objects.get(account=new_payer, creditor=member, ekip=ekip)
                                share2.debtor -= change_amount
                                if share2.debtor == 0:
                                    share2.delete()
                                elif share2.debtor < 0:
                                    share2.account = member
                                    share2.creditor = new_payer
                                    share2.debtor = -share2.debtor
                                    share2.save()
                                share2.save()
                elif new_payer != expense.payer:
                    for member in expense.ekip.member.all():
                        if member == expense.payer:
                            continue
                        elif member != expense.payer:
                            old_debtor = expense.amount / ekip.member.count()
                            if not Share.objects.filter(account=member, creditor=expense.payer, ekip=ekip) and \
                                    not Share.objects.filter(account=expense.payer, creditor=member, ekip=ekip):
                                share = Share.objects.create(account=expense.payer, creditor=member, debtor=old_debtor,
                                                             ekip=ekip)
                                share.save()
                            elif Share.objects.filter(account=member, creditor=expense.payer, ekip=expense.ekip):
                                share1 = Share.objects.get(account=member, creditor=expense.payer, ekip=expense.ekip)
                                share1.debtor -= old_debtor
                                if share1.debtor < 0:
                                    share1.account = expense.payer
                                    share1.creditor = member
                                    share1.debtor = -share1.debtor
                                    share1.save()
                                if share1.debtor == 0:
                                    share1.delete()
                            elif Share.objects.filter(account=expense.payer, creditor=member, ekip=expense.ekip):
                                share2 = Share.objects.get(account=expense.payer, creditor=member, ekip=expense.ekip)
                                share2.debtor += old_debtor
                                share2.save()
                    for member in expense.ekip.member.all():
                        if member == new_payer:
                            continue
                        elif member != new_payer:
                            if not Share.objects.filter(account=member, creditor=new_payer, ekip=ekip) and \
                                    not Share.objects.filter(account=new_payer, creditor=member, ekip=ekip):
                                share = Share.objects.create(account=member, creditor=new_payer, ekip=ekip,
                                                             debtor=new_debtor)
                                share.save()
                            elif Share.objects.filter(account=member, creditor=new_payer, ekip=ekip):
                                share = Share.objects.get(account=member, creditor=new_payer, ekip=ekip)
                                share.debtor += new_debtor
                                share.save()
                            elif Share.objects.filter(account=new_payer, creditor=member, ekip=ekip):
                                share1 = Share.objects.get(account=new_payer, creditor=member, ekip=ekip)
                                share1.debtor -= new_debtor
                                if share1.debtor == 0:
                                    share1.delete()
                                elif share1.debtor < 0:
                                    share1.account = member
                                    share1.creditor = new_payer
                                    share1.debtor = -share1.debtor
                                    share1.save()
                                share1.save()
            elif expense.equal_share == False:
                shares = MemberAmount.objects.filter(expense=expense)
                for share in shares:
                    if not Share.objects.filter(account=share.account, creditor=share.expense.payer, ekip=ekip) and \
                            not Share.objects.filter(account=share.expense.payer, creditor=share.account, ekip=ekip):
                        sharee = Share.objects.create(account=share.expense.payer, creditor=share.account,
                                                      debtor=share.amount, ekip=ekip)
                        sharee.save()
                    elif Share.objects.filter(account=share.account, creditor=share.expense.payer, ekip=ekip):
                        share1 = Share.objects.get(account=share.account, creditor=share.expense.payer, ekip=ekip)
                        share1.debtor -= share.amount
                        if share1.debtor < 0:
                            share1.account = share.expense.payer
                            share1.creditor = share.account
                            share1.debtor = -share1.debtor
                            share1.save()
                        elif share1.debtor == 0:
                            share1.delete()
                    elif Share.objects.filter(account=share.expense.payer, creditor=share.account, ekip=ekip):
                        share2 = Share.objects.get(account=share.expense.payer, creditor=share.account, ekip=ekip)
                        share2.debtor += share.amount
                        share2.save()
                    share.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = Expense.objects.get(pk=pk)
        member_count = expense.ekip.member.count()
        member_debtor = expense.amount / member_count
        if expense.equal_share == True:
            for member in expense.ekip.member.all():
                if member == expense.payer:
                    continue
                elif member != expense.payer:
                    if not Share.objects.filter(account=member, creditor=expense.payer, ekip=expense.ekip) and \
                            not Share.objects.filter(account=expense.payer, creditor=member, ekip=expense.ekip):
                        share = Share.objects.create(account=expense.payer, creditor=member, debtor=member_debtor,
                                                     ekip=expense.ekip)
                        share.save()
                    elif Share.objects.filter(account=member, creditor=expense.payer, ekip=expense.ekip):
                        share1 = Share.objects.get(account=member, creditor=expense.payer, ekip=expense.ekip)
                        share1.debtor -= member_debtor
                        if share1.debtor < 0:
                            share1.account = expense.payer
                            share1.creditor = member
                            share1.debtor = -share1.debtor
                            share1.save()
                        if share1.debtor == 0:
                            share1.delete()
                    elif Share.objects.filter(account=expense.payer, creditor=member, ekip=expense.ekip):
                        share2 = Share.objects.get(account=expense.payer, creditor=member, ekip=expense.ekip)
                        share2.debtor += member_debtor
                        share2.save()
            expense.delete()
        elif expense.equal_share == False:
            shares = MemberAmount.objects.filter(expense=expense)
            for share in shares:
                if share.account == share.expense.payer:
                    continue
                else:
                    if not Share.objects.filter(account=share.account, creditor=share.expense.payer,
                                                ekip=share.expense.ekip) and \
                            not Share.objects.filter(account=share.expense.payer, creditor=share.account,
                                                     ekip=share.expense.ekip):
                        sharee = Share.objects.create(account=share.expense.payer, creditor=share.account,
                                                      debtor=share.amount, ekip=share.expense.ekip)
                        sharee.save()
                    elif Share.objects.filter(account=share.account, creditor=share.expense.payer,
                                              ekip=share.expense.ekip):
                        share1 = Share.objects.get(account=share.account, creditor=share.expense.payer,
                                                   ekip=share.expense.ekip)
                        share1.debtor -= share.amount
                        if share1.debtor < 0:
                            share1.account = share.expense.payer
                            share1.creditor = share.account
                            share1.debtor = -share1.debtor
                            share1.save()
                        elif share1.debtor == 0:
                            share1.delete()
                    elif Share.objects.filter(account=share.expense.payer, creditor=share.account,
                                              ekip=share.expense.ekip):
                        share2 = Share.objects.get(account=share.expense.payer, creditor=share.account,
                                                   ekip=share.expense.ekip)
                        share2.debtor += share.amount
                        share2.save()
            expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShareDetail(APIView):
    def get_object(self, pk):
        try:
            return Share.objects.filter(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializer = ShareSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = Share.objects.filter(pk=pk).first()
        serializer = ShareSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        share = Share.objects.get(pk=pk)
        ekip = Ekip.objects.get(pk=share.ekip_id)
        ekip.unpaid -= share.debtor
        ekip.save()
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Api to get all Shares of an account
class AccountShareApi(APIView):
    def get_object(self, pk):
        account = User.objects.get(pk=pk)
        return Share.objects.filter(account=account)

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ShareSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


# Api to get all Shares of an ekip
class EkipShareApi(APIView):
    def get_object(self, pk):
        ekip = Ekip.objects.get(pk=pk)
        return Share.objects.filter(ekip=ekip)

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ShareSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


# Api to get all Creditor of an account
class AccountCreditorApi(APIView):
    def get_object(self, pk):
        account = User.objects.get(pk=pk)
        return Share.objects.filter(creditor=account)

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = ShareSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


# Api to get all Members of an ekip
class EkipMemberApi(APIView):
    def get_object(self, pk):
        ekip = Ekip.objects.get(pk=pk)
        return ekip.member

    def get(self, request, pk):
        query = self.get_object(pk)
        serializers = UserSerializer(query, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)


# Api to get Creditor of an account
class Creditor(APIView):
    def get(self, request, pk):
        ekipsmembers = []
        friends = []
        response = []
        myaccount = User.objects.get(pk=pk)
        ekips = Ekip.objects.all()
        for ekip in ekips:
            for member in ekip.member.all():
                ekipsmembers.append(member)
        for mymember in ekipsmembers:
            if mymember not in friends:
                friends.append(mymember)
        for myfriend in friends:
            query = Share.objects.filter(account=myfriend, creditor=myaccount)
            query2 = Share.objects.filter(account=myaccount, creditor=myfriend)
            sum = 0
            if query:
                for share in query:
                    sum += share.debtor
            if query2:
                for share2 in query2:
                    sum -= share2.debtor
            serializers = ShareSerializer(query, many=True, context={'request': request})
            if query2:
                if sum > 0:
                    response.append({'name': query2[0].creditor.first_name, 'lname': query2[0].creditor.last_name,
                                     'creditor': query2[0].account.first_name, 'debtor': sum,
                                     'id': query2[0].creditor.id, 'fid': query2[0].account.id})
                elif sum < 0:
                    query = Share.objects.filter(account=myfriend, creditor=myaccount)
                    response.append({'name': query2[0].account.first_name, 'lname': query2[0].account.last_name,
                                     'creditor': query2[0].creditor.first_name, 'debtor': -sum,
                                     'id': query2[0].account.id, 'fid': query2[0].creditor.id})
            elif query:
                if sum > 0:
                    response.append({'name': query[0].account.first_name, 'lname': query[0].account.last_name,
                                     'creditor': query[0].creditor.first_name, 'debtor': sum, 'id': query[0].account.id,
                                     'fid': query[0].creditor.id})
                elif sum < 0:
                    query = Share.objects.filter(account=myfriend, creditor=myaccount)
                    response.append({'name': query[0].creditor.first_name, 'lname': query[0].creditor.last_name,
                                     'creditor': query[0].account.first_name, 'debtor': -sum,
                                     'id': query[0].creditor.id, 'fid': query[0].account.id})

        return Response(response, status=status.HTTP_200_OK)


# Api to get obligor of an account
class Obligor(APIView):
    def get(self, request, pk, pk1):
        myaccount = User.objects.get(pk=pk)
        myfriend = User.objects.get(pk=pk1)
        query = Share.objects.filter(account_id=myaccount.id, creditor=myfriend)
        query2 = Share.objects.filter(account_id=myfriend.id, creditor=myaccount)
        sum = 0
        ids = []
        for share in query:
            sum += share.debtor
            ids.append(share.pk)
        for share2 in query2:
            sum -= share2.debtor
            ids.append(share2.pk)

        serializers = ShareSerializer(query, many=True, context={'request': request})
        if sum < 0:
            return Response({'name': query[0].account.first_name, 'lname': query[0].account.last_name,
                             'creditor': query[0].creditor.first_name, 'debtor': -sum, 'ids': ids},
                            status=status.HTTP_200_OK)
        if sum > 0:
            return Response({'name': query[0].creditor.first_name, 'lname': query[0].creditor.last_name,
                             'creditor': query[0].account.first_name, 'debtor': sum, 'ids': ids},
                            status=status.HTTP_200_OK)


# for pay all debtor to a account
class PayDebtor(APIView):
    def get(self, request, pk, pk1):
        myaccount = User.objects.get(pk=pk)
        myfriend = User.objects.get(pk=pk1)

        query = Share.objects.filter(Q(account=myaccount, creditor=myfriend) |
                                     Q(account=myfriend, creditor=myaccount))
        for share in query:
            share.ekip.unpaid -= share.debtor
            share.ekip.save()
        query.delete()
        return Response({'pay': 'done'}, status=status.HTTP_204_NO_CONTENT)


# for invite to Ekip
class EkipInvite(APIView):
    def get(self, request, pk, token):
        myaccount = User.objects.get(pk=pk)
        ekip = Ekip.objects.get(token=token)
        ekip.member.add(myaccount)
        return Response({'addmember': 'done'}, status=status.HTTP_200_OK)


class Invielink(APIView):
    def get(self, request, token):
        user = request.user
        if user.id:
            ekip = Ekip.objects.get(token=token)
            ekip.member.add(user)
            return redirect(
                'http://127.0.0.1:3000/ekip/all/' + str(user.id))
        else:
            return redirect('http://127.0.0.1:8000/login')


class MemberAmountApiView(APIView):
    def get(self, request):
        query = MemberAmount.objects.all()
        serializer = MemberAmountSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MemberAmountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberAmountDetail(APIView):
    def get_object(self, pk):
        try:
            return MemberAmount.objects.filter(pk=pk)
        except MemberAmount.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        query = self.get_object(pk)
        serializer = MemberAmountSerializer(query, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = MemberAmount.objects.filter(pk=pk).first()
        serializer = MemberAmountSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = self.get_object(pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def SignUpView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('http://127.0.0.1:3000/account/create' + '/?acid=' + str(user.id) + '&n=' + user.username)
    elif request.method == 'GET':
        form = UserCreationForm()
    return render(request, 'share/signup.html', {'form': form})


@csrf_exempt
def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('http://127.0.0.1:3000/account/' + str(user.id))
    elif request.method == 'GET':
        form = AuthenticationForm()
    return render(request, 'share/base.html', {'form': form})


@csrf_exempt
def LogoutView(request):
    if request.method == 'GET':
        logout(request)
        return redirect('http://127.0.0.1:3000')
    elif request.method == 'POST':
        logout(request)
        return redirect('http://127.0.0.1:3000')
