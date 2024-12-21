#  Weshort - Shortener URL API Client Library for Python
#  Copyright (C) 2024-present AyiinXd <https://github.com/AyiinXd>
#
#  This file is part of Weshort.
#
#  Weshort is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Weshort is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Weshort.  If not, see <http://www.gnu.org/licenses/>.

class CreatedPayment:
    def __init__(self, **kwargs):
        self.ownerName: str = kwargs.get("ownerName", "")
        self.transactionId: str = kwargs.get("transactionId", "")
        self.orderId: str = kwargs.get("orderId", "")
        self.qrisToken: str = kwargs.get("qrisToken", "")
        self.expired: str = kwargs.get("expired", "")

    def parser(self):
        return {
            "_": "CreatePayment",
            "ownerName": self.ownerName,
            "orderId": self.orderId,
            "transactionId": self.transactionId,
            "qrisToken": self.qrisToken,
            "expired": self.expired
        }


class Payment:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", 0)
        self.orderId: str = kwargs.get("orderId", "")
        self.ownerName: str = kwargs.get("ownerName", "")
        self.amount: int = kwargs.get("amount", 0)
        self.keyword: str = kwargs.get("keyword", "")
        self.status: str = kwargs.get("status", "")
        self.createdAt: str = kwargs.get("createdAt", "")
        self.updatedAt: str = kwargs.get("updatedAt", "")

    def parser(self):
        return {
            "_": "Payment",
            "id": self.id,
            "orderId": self.orderId,
            "ownerName": self.ownerName,
            "amount": self.amount,
            "keyword": self.keyword,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }


class CheckedTransaction:
    def __init__(self, **kwargs):
        self.statusCode: str = kwargs.get("statusCode", "")
        self.transactionId: str = kwargs.get("transactionId", "")
        self.amount: str = kwargs.get("amount", "")
        self.currency: str = kwargs.get("currency", "")
        self.orderId: str = kwargs.get("orderId", "")
        self.paymentType: str = kwargs.get("paymentType", "")
        self.transactionStatus: str = kwargs.get("transactionStatus", "")
        self.fraudStatus: str = kwargs.get("fraudStatus", "")
        self.transactionTime: str = kwargs.get("transactionTime", "")
        self.expiredTime: str = kwargs.get("expiredTime", "")

    def parser(self):
        return {
            "_": "CheckedTransaction",
            "statusCode": self.statusCode,
            "transactionId": self.transactionId,
            "amount": self.amount,
            "currency": self.currency,
            "orderId": self.orderId,
            "paymentType": self.paymentType,
            "transactionStatus": self.transactionStatus,
            "fraudStatus": self.fraudStatus,
            "transactionTime": self.transactionTime,
            "expiredTime": self.expiredTime
        }


class PaymentData:
    def __init__(self, **kwargs):
        self.statusCode: str = kwargs.get("statusCode", "")
        self.transactionId: str = kwargs.get("transactionId", "")
        self.amount: str = kwargs.get("amount", "")
        self.currency: str = kwargs.get("currency", "")
        self.orderId: str = kwargs.get("orderId", "")
        self.paymentType: str = kwargs.get("paymentType", "")
        self.transactionStatus: str = kwargs.get("transactionStatus", "")
        self.fraudStatus: str = kwargs.get("fraudStatus", "")
        self.transactionTime: str = kwargs.get("transactionTime", "")
        self.expiredTime: str = kwargs.get("expiredTime", "")

    def parser(self):
        return {
            "_": "PaymentData",
            "statusCode": self.statusCode,
            "transactionId": self.transactionId,
            "amount": self.amount,
            "currency": self.currency,
            "orderId": self.orderId,
            "paymentType": self.paymentType,
            "transactionStatus": self.transactionStatus,
            "fraudStatus": self.fraudStatus,
            "transactionTime": self.transactionTime,
            "expiredTime": self.expiredTime
        }


class TransactionData:
    def __init__(self, **kwargs):
        self.keyword: str = kwargs.get("keyword", "")
        self.url: str = kwargs.get("url", "")
        self.shortUrl: str = kwargs.get("shortUrl", "")

    def parser(self):
        return {
            "_": "TransactionData",
            "keyword": self.keyword,
            "url": self.url,
            "shortUrl": self.shortUrl
        }


class TransactionSuccess:
    def __init__(self, **kwargs):
        self.payment: PaymentData = PaymentData(**kwargs.get("payment", {}))
        self.data: TransactionData = TransactionData(**kwargs.get("data", {}))

    def parser(self):
        return {
            "_": "TransactionSuccess",
            "payment": self.payment.parser(),
            "data": self.data.parser()
        }
