from rest_framework import serializers
from share.models import Ekip, Expense, Share, Friends, MemberAmount, User


class FriendsSerializer(serializers.ModelSerializer):
    friend_id = serializers.CharField(source='friends.id', read_only=True)
    friend_name = serializers.CharField(source='friends.first_name', read_only=True)
    friend_lname = serializers.CharField(source='friends.last_name', read_only=True)
    friend_pic = serializers.ImageField(source='friends.profile_picture', read_only=True)
    friend_status = serializers.CharField(source='friends.status', read_only=True)

    class Meta:
        model = Friends
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = '__all__'

    def validate(self, data):
        data_account = data.get('account')
        data_friend = data.get('friends')
        if Friends.objects.filter(account=data_account,
                                  friends=data_friend):
            raise serializers.ValidationError('you already friend with this user')
        return super(FriendSerializer, self).validate(data)


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'profile_picture', 'status', 'id'


class EkipSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    creater_name = serializers.CharField(source='creater.first_name', read_only=True)

    class Meta:
        model = Ekip
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    ekip_name = serializers.CharField(source='ekip.name', read_only=True)
    payer_name = serializers.CharField(source='payer.first_name', read_only=True)
    payer_lname = serializers.CharField(source='payer.last_name', read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'


class ShareSerializer(serializers.ModelSerializer):
    account_pic = serializers.ImageField(source='account.profile_picture', read_only=True)
    account_name = serializers.CharField(source='account.first_name', read_only=True)
    ekip_name = serializers.CharField(source='ekip.name', read_only=True)
    creditor_pic = serializers.ImageField(source='creditor.profile_picture', read_only=True)
    creditor_name = serializers.CharField(source='creditor.first_name', read_only=True)

    class Meta:
        model = Share
        fields = '__all__'


class MemberAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberAmount
        fields = '__all__'

    def validate(self, data):
        amount = data.get('amount')
        expense = data.get('expense')
        account = data.get('account')

        sum_amounts = 0

        for memberAmount in MemberAmount.objects.filter(expense=expense):
            sum_amounts += memberAmount.amount
        if amount > expense.amount - sum_amounts:
            raise serializers.ValidationError("مبلغ باید بین 0 و %s باشد" % (expense.amount - sum_amounts))
        return super(MemberAmountSerializer, self).validate(data)
