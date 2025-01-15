from django.urls import path
from apps.payment.views import *

app_name = "payment"

urlpatterns = [
    # path("health-check/", HealthCheckView.as_view(), name="health-check"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("register-card/", RegisterCard.as_view(), name="register-card"),
    path("transaction-history/", TransactionHistoryView.as_view(), name="transaction-history"),]


