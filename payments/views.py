from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView


def initiate_payment(request):
    # Code to handle the initiation of payment
    # Make a POST request to Daraja API to initiate the payment
    url = "https://api.daraja.co.ke/payments/initiate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.DARAJA_API_KEY}",
    }
    payload = {
        "amount": "1000",
        "description": "Payment for your order",
        "reference": "order_123",
        "callback_url": settings.DARAJA_CALLBACK_URL,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    payment_data = response.json()

    # Retrieve payment URL from the API response and redirect the user
    payment_url = payment_data["payment_url"]
    return redirect(payment_url)


def payment_callback(request):
    # Code to handle the payment callback
    # Retrieve the payment status and update your database accordingly
    payment_status = request.GET.get("status")
    if payment_status == "success":
        # Update your database and handle successful payment
        return HttpResponse("Payment successful")
    else:
        # Handle failed payment
        return HttpResponse("Payment failed")


def paystackInitiatePayment(request):
    if request.method == "POST":
        user = request.user
        email = user.email
        # Retrieve form data or request data
        amount = request.POST.get("amount")

        # Paystack initiation endpoint
        url = "https://api.paystack.co/transaction/initialize"

        # Headers
        headers = {
            "Authorization": "Bearer sk_live_ae8eed68829a37618a7dc3af22e6be9ba1fc713f",
            "Content-Type": "application/json",
        }

        # Payload
        data = {"email": email, "amount": amount}

        try:
            # Make the request to Paystack
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            print(response_data)

            if response.status_code == 200 and response_data.get("status") == True:
                payment_url = response_data["data"]["authorization_url"]
                return redirect(payment_url)
            else:
                return JsonResponse({"error": "Failed to initiate payment"}, status=400)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
