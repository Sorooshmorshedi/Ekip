from django.conf import settings
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]+$',
                message='نام کاربری باید از حدوف و اعداد انگلیسی تشکیل شود'
            )
        ],
        error_messages={
            'unique': ("this username already exists."),
        },
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    profile_picture = models.ImageField(default='', upload_to='store_image/', null=True, blank=True)
    status = models.TextField(max_length=255, null=True, blank=True)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'


class Friends(models.Model):
    account = models.ForeignKey(User, on_delete=CASCADE, related_name="friend")
    friends = models.ForeignKey(User, on_delete=CASCADE, related_name="friendto")

    def __str__(self):
        return "{} friend with {}".format(self.account, self.friends)


class Ekip(models.Model):
    creater = models.ForeignKey(User, on_delete=CASCADE, related_name="ekip", null=True, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    about = models.CharField(max_length=255, null=True, blank=True)
    member = models.ManyToManyField(User, related_name="ekips")
    expense_sum = models.DecimalField(default=0, max_digits=24, decimal_places=2, null=True, blank=True)
    unpaid = models.DecimalField(default=0, max_digits=24, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def createtoken():
        from randstr import randstr
        return randstr(30)

    def save(self, *args, **kwargs):
        if not self.id:
            self.token = self.createtoken()

        super().save(*args, **kwargs)


class Share(models.Model):
    creditor = models.ForeignKey(User, on_delete=CASCADE, related_name="cshare", blank=True, null=True)
    account = models.ForeignKey(User, on_delete=CASCADE, related_name="share", blank=True, null=True)
    ekip = models.ForeignKey(Ekip, on_delete=CASCADE, related_name="share")
    debtor = models.DecimalField(default=0, max_digits=24, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return "{} debtor {} to {}".format(self.account.first_name, self.debtor, self.creditor.first_name)


class Expense(models.Model):
    title = models.CharField(max_length=55, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=24, decimal_places=2, null=True, blank=True)
    payer = models.ForeignKey(User, on_delete=CASCADE, related_name="expense", null=True, blank=True)
    ekip = models.ForeignKey(Ekip, on_delete=CASCADE, related_name="expense")
    date = models.DateTimeField(null=True, blank=True)
    equal_share = models.BooleanField(default=True)

    def __str__(self):
        return "{} for {}".format(self.amount, self.title)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = datetime.now()
            self.ekip.expense_sum += self.amount
            self.ekip.unpaid += self.amount
            self.ekip.save()
            member_count = self.ekip.member.count()
            member_debtor = self.amount / member_count
            if self.equal_share == True:
                for member in self.ekip.member.all():
                    if member == self.payer:
                        continue
                    elif member != self.payer:
                        if not Share.objects.filter(account=member, creditor=self.payer, ekip=self.ekip) and \
                                not Share.objects.filter(account=self.payer, creditor=member, ekip=self.ekip):
                            Share.objects.create(account=member, creditor=self.payer, ekip=self.ekip,
                                                 debtor=member_debtor)
                        elif Share.objects.filter(account=member, creditor=self.payer, ekip=self.ekip):
                            share = Share.objects.get(account=member, creditor=self.payer, ekip=self.ekip)
                            share.debtor += member_debtor
                            share.save()
                        elif Share.objects.filter(account=self.payer, creditor=member, ekip=self.ekip):
                            share1 = Share.objects.get(account=self.payer, creditor=member, ekip=self.ekip)
                            share1.debtor -= member_debtor
                            if share1.debtor == 0:
                                share1.delete()
                            elif share1.debtor < 0:
                                share1.account = member
                                share1.creditor = self.payer
                                share1.debtor = -share1.debtor
                                share1.save()
                            share1.save()
        super().save(*args, **kwargs)


class MemberAmount(models.Model):
    account = models.ForeignKey(User, on_delete=CASCADE, related_name="MemberAmount")
    expense = models.ForeignKey(Expense, on_delete=CASCADE, related_name="MemberAmount")
    amount = models.DecimalField(default=0, max_digits=24, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return "{} {} from {}".format(self.amount, self.account.first_name, self.expense.ekip.name)

    def save(self, *args, **kwargs):
        if self.expense.equal_share == True:
            raise ValidationError('expense is equal share')
        if not self.id:
            if self.amount != 0 and self.account != self.expense.payer:
                if MemberAmount.objects.filter(expense=self.expense, account=self.account):
                    raise ValidationError('member amount alrady exist')
                if not Share.objects.filter(account=self.expense.payer, creditor=self.account,
                                            ekip=self.expense.ekip) and \
                        not Share.objects.filter(account=self.account, creditor=self.expense.payer,
                                                 ekip=self.expense.ekip):
                    share = Share.objects.create(account=self.account, ekip=self.expense.ekip,
                                                 creditor=self.expense.payer, debtor=self.amount)
                    share.save()
                elif Share.objects.filter(account=self.expense.payer, creditor=self.account, ekip=self.expense.ekip):
                    share = Share.objects.get(account=self.expense.payer, creditor=self.account, ekip=self.expense.ekip)
                    share.debtor -= self.amount
                    if share.debtor < 0:
                        share.account = self.account
                        share.creditor = self.expense.payer
                        share.debtor = -share.debtor
                    elif share.debtor == 0:
                        share.delete()
                    share.save()
                elif Share.objects.filter(account=self.account, creditor=self.expense.payer, ekip=self.expense.ekip):
                    share = Share.objects.get(account=self.account, creditor=self.expense.payer, ekip=self.expense.ekip)
                    share.debtor += self.amount
                    share.save()
        super().save(*args, **kwargs)
