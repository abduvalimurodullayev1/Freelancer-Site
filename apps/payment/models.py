from django.db import models
from apps.common.models import BaseModel
from apps.users.models import User
from django.utils import timezone
from django.conf import settings
import base64
from django.utils.translation import gettext_lazy as _


class UserCard(BaseModel):
    class CardChoices(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACITIVE = 'active', _('Active') 
        DELETED = 'deleted', _('Deleted')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    class VendorType(models.TextChoices):
        HUMO = 'humo', _('Humo')
        UZCARD = 'uzcard', _('Uzcard')
        
    status = models.CharField(max_length=20, choices=CardChoices.choices, default=CardChoices.PENDING, verbose_name=_("Status"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))    
    card_number = models.CharField(max_length=16, verbose_name=_("Card Number"))
    cid = models.CharField(max_length=3, verbose_name=_("CID"))
    expire_date = models.CharField(max_length=5, verbose_name=_("Expire Date")) 
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))
    vendor = models.CharField(max_length=10, choices=VendorType.choices, default=VendorType.HUMO, verbose_name=_("Vendor"))
    
    objects = models.Manager()
    
    
    class Meta:
        db_table = "UserCard"
        verbose_name = _("User Card")
        ordering = ['-created_at']
        unique_together = ['status', 'is_confirmed']
    
    def __str__(self):
        return self.card_number
    
    def soft_delete(self):
        self.status = self.CardChoices.DELETED
        self.is_confirmed = False
        self.save()
        
        

class Transaction(BaseModel):
    class StatusType(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        CANCELLED = 'cancelled', _('Cancelled')
        
    class PaymentType(models.TextChoices):
        CARD = 'CARD', _('CARD')
        PAYLOV = 'PAYLOV', _('PAYLOV')
        PAYME = 'PAYME', _('PAYME')

    card = models.ForeignKey(UserCard, on_delete=models.PROTECT, related_name='transactions',
                             verbose_name=_('Card id'), null=True, blank=True)
    currency = models.CharField(_('Currency'), max_length=10, default='USD')

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    status = models.CharField(_('Status'), max_length=32, choices=StatusType.choices, default=StatusType.PENDING)
    remote_id = models.CharField(_('Remote id'), max_length=255, null=True, blank=True)
    tax_amount = models.DecimalField(_('TAX Amount'), max_digits=10, decimal_places=2, default=0.0, null=True,
                                     blank=True)
    paid_at = models.DateTimeField(verbose_name=_("Paid at"), null=True, blank=True)
    canceled_at = models.DateTimeField(verbose_name=_("Canceled at"), null=True, blank=True)
    payment_type = models.CharField(_("Payment Type"), choices=PaymentType.choices)
    extra = models.JSONField(_('Extra'), null=True, blank=True)
    is_notification_sent = models.BooleanField(_('Is notification sent'), default=False)
    

    class Meta:
        db_table = 'Transaction'
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ('remote_id',)

    def __str__(self):
        return f"{self.payment_type} | {self.id}"

    def success_process(self):
        self.status = self.StatusType.ACCEPTED
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])

        self.user.update_balance()

    def cancel_process(self):
        self.status = self.StatusType.CANCELED
        self.canceled_at = timezone.now()
        self.save(update_fields=['status', 'canceled_at'])

        self.user.update_balance()

    @property
    def payment_url(self):
        payment_url = ""

        if self.payment_type == Transaction.PaymentType.PAYLOV:
            merchant_id = settings.PAYMENT_CREDENTIALS['paylov']['merchant_id']
            query = f"merchant_id={merchant_id}&amount={self.amount}&account.order_id={self.id}"
            encode_params = base64.b64encode(query.encode("utf-8"))
            encode_params = str(encode_params, "utf-8")
            payment_url = f"{settings.PAYMENT_CREDENTIALS['paylov']['callback_url']}/{encode_params}"

        elif self.payment_type == Transaction.PaymentType.PAYME:
            merchant_id = settings.PAYMENT_CREDENTIALS['payme']['merchant_id']
            params = f"m={merchant_id};ac.order_id={self.id};a={self.amount * 100};"
            encode_params = base64.b64encode(params.encode("utf-8"))
            encode_params = str(encode_params, "utf-8")
            payment_url = f"{settings.PAYMENT_CREDENTIALS['payme']['callback_url']}/{encode_params}"

        return payment_url


class MerchantRequestLog(BaseModel):
    payment_type = models.CharField(max_length=50, verbose_name=_("Payment type"),
                                    choices=Transaction.PaymentType.choices)
    method_type = models.CharField(max_length=255, verbose_name=_('Method type'), null=True, blank=True)
    request_headers = models.TextField(verbose_name=_("Request Headers"), null=True)
    request_body = models.TextField(verbose_name=_("Request Body"), null=True)

    response_headers = models.TextField(verbose_name=_("Response Headers"), null=True)
    response_body = models.TextField(verbose_name=_("Response Body"), null=True)
    response_status_code = models.PositiveSmallIntegerField(verbose_name=_("Response status code"), null=True)


class PaymentRetryLog(BaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='retry_logs')
    attempt_number = models.PositiveSmallIntegerField(default=1, verbose_name=_("Attempt number"))
    response = models.TextField(verbose_name=_("Payment Gateway Response"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'PaymentRetryLog'
        verbose_name = _('Payment Retry Log')
        verbose_name_plural = _('Payment Retry Logs')


class TransactionHistory(BaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(_('Status'), max_length=32, choices=Transaction.StatusType.choices)
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Changed at"))
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Changed by"))

    class Meta:
        db_table = 'TransactionHistory'
        verbose_name = _('Transaction History')
        verbose_name_plural = _('Transaction Histories')
        ordering = ('-changed_at',)


