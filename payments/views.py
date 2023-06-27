from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import json
from django.conf import settings

def initiate_payment(request):
    # Code to handle the initiation of payment
    # Make a POST request to Daraja API to initiate the payment
    url = 'https://api.daraja.co.ke/payments/initiate'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.DARAJA_API_KEY}'
    }
    payload = {
        'amount': '1000',
        'description': 'Payment for your order',
        'reference': 'order_123',
        'callback_url': settings.DARAJA_CALLBACK_URL
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    payment_data = response.json()

    # Retrieve payment URL from the API response and redirect the user
    payment_url = payment_data['payment_url']
    return redirect(payment_url)

def payment_callback(request):
    # Code to handle the payment callback
    # Retrieve the payment status and update your database accordingly
    payment_status = request.GET.get('status')
    if payment_status == 'success':
        # Update your database and handle successful payment
        return HttpResponse('Payment successful')
    else:
        # Handle failed payment
        return HttpResponse('Payment failed')

