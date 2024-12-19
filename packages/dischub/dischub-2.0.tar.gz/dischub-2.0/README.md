# Dischub Python SDK

## Overview

The Dischub Python SDK allows developers to easily integrate with the Dischub API for online payment processing. This SDK provides a simple interface for creating payments via the Dischub API.

## Installation

You can install the Dischub SDK using pip:

```bash
"pip install dischub

"from dischub import Dischub

"
def payment():
    data = {
        "sender": "chihoyistanford@gmail.com",
        "recipient": "chihoyistanford0@gmail.com",
        "amount": 100,
        "currency": "USD",
    }
    payment_instance = Dischub()
    response = payment_instance.create_payment(data)
    print(response)
"
