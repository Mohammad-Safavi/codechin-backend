
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
import requests
import json
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import *
from .serializers import *


MERCHANT = '00000000-0000-0000-0000-000000000000'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/api/v1/account/verify/'


def send_request(request):
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(
            req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success':'حذف با موفقیت انجام شد.'})

    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request, *args, **kwargs):
        serializer = CreateCartSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if serializer.save():
                return Response({'success':'محصول موردنظر با موفقیت به سبد خرید افزوده شد.'})


class CountCartView(APIView):
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        action = request.data['action']
        cart_id = request.data['cart_id']
        cart = Cart.objects.filter(pk=cart_id)
        if cart.exists():
            if action == "add" :
                cart.update(count=cart.first().count+1)
                return Response({'success':'تعداد محصول در سبد خرید شما افزایش یافت'})
            elif action == "dec" :
                if cart.first().count > 1 :
                    cart.update(count=cart.first().count-1)
                    return Response({'success':'تعداد محصول در سبد خرید شما کاهش یافت.'})
                else :
                    return Response({'error':'تعداد محصول شما از ۱ عدد نمی تواند کمتر شود.'}, status=status.HTTP_204_NO_CONTENT)
            else :
                return Response({'error':'مقدار action نا مفهوم است.'}, status=status.HTTP_204_NO_CONTENT)
        else :
            return Response({'error':'سبد خرید موردنظر معتبر نمی باشد.'}, status=status.HTTP_204_NO_CONTENT)


