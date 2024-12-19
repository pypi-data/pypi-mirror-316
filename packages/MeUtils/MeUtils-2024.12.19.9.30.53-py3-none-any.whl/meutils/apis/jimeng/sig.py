#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : sig
# @Time         : 2024/12/18 15:36
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
import hashlib
import hmac
import datetime


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


if __name__ == '__main__':
    pass
    from meutils.pipe import *
    from meutils.apis.jimeng.utils import get_upload_token

    # data = arun(get_upload_token())

    # access_key_id = data['data']['auth']['access_key_id']
    # secret_access_key = data['data']['auth']['secret_access_key']
    # session_token = data['data']['auth']['session_token']

    import hashlib
    import hmac
    import datetime


    def sign(key, msg):
        """计算 HMAC-SHA256"""
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


    def getSignatureKey(key, dateStamp, regionName, serviceName):
        """生成签名密钥"""
        kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = sign(kDate, regionName)
        kService = sign(kRegion, serviceName)
        kSigning = sign(kService, 'aws4_request')
        return kSigning


    def calculate_signature(string_to_sign, secret_key, region, service, date):
        """计算 AWS4-HMAC-SHA256 签名"""
        # 生成签名密钥
        signing_key = getSignatureKey(
            secret_key,
            date.strftime('%Y%m%d'),
            region,
            service
        )

        # 计算最终签名
        signature = hmac.new(
            signing_key,
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature

        # 示例参数


    secret_key = 'AKTPN2VkZWY2MWNhNjVlNGZhZThiZmVmNzEwODA3YjM1YTY'
    region = 'cn-north-1'
    service = 'imagex'
    date = datetime.datetime.utcnow()
    print(date)
    hash_of_canonical_request = {
        "SessionKey": "eyJhY2NvdW50VHlwZSI6IkltYWdlWCIsImFwcElkIjoiIiwiYml6VHlwZSI6IiIsImZpbGVUeXBlIjoiaW1hZ2UiLCJsZWdhbCI6IiIsInN0b3JlSW5mb3MiOiJbe1wiU3RvcmVVcmlcIjpcInRvcy1jbi1pLWE5cm5zMnJsOTgvYmQzZGNlZWIzN2Y3NDA5NjlkMTBiZjBiZjhhMzk0NmUuanBlZ1wiLFwiQXV0aFwiOlwiU3BhY2VLZXkvYTlybnMycmw5OC8xLzp2ZXJzaW9uOnYyOmV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpsZUhBaU9qRTNNelExTXpBd016Z3NJbk5wWjI1aGRIVnlaVWx1Wm04aU9uc2lZV05qWlhOelMyVjVJam9pWm1GclpWOWhZMk5sYzNOZmEyVjVJaXdpWW5WamEyVjBJam9pZEc5ekxXTnVMV2t0WVRseWJuTXljbXc1T0NJc0ltVjRjR2x5WlNJNk1UY3pORFV6TURBek9Dd2labWxzWlVsdVptOXpJanBiZXlKdmFXUkxaWGtpT2lKaVpETmtZMlZsWWpNM1pqYzBNRGsyT1dReE1HSm1NR0ptT0dFek9UUTJaUzVxY0dWbklpd2labWxzWlZSNWNHVWlPaUl4SW4xZExDSmxlSFJ5WVNJNmV5SmliRzlqYTE5dGIyUmxJam9pSWl3aVkyOXVkR1Z1ZEY5MGVYQmxYMkpzYjJOcklqb2llMXdpYldsdFpWOXdZM1JjSWpvd0xGd2liVzlrWlZ3aU9qQXNYQ0p0YVcxbFgyeHBjM1JjSWpwdWRXeHNMRndpWTI5dVpteHBZM1JmWW14dlkydGNJanBtWVd4elpYMGlMQ0psYm1OeWVYQjBYMkZzWjI4aU9pSWlMQ0psYm1OeWVYQjBYMnRsZVNJNklpSXNJbVY0ZEY5amIyNTBaVzUwWDNSNWNHVWlPaUpwYldGblpTOXFjR1ZuSWl3aWFYTmZhVzFoWjJWNElqcDBjblZsTENKemNHRmpaU0k2SW1FNWNtNXpNbkpzT1RnaWZYMTkueVFadDJoYWFVMDBuMTFZREJXZDBCbTNIYWdtVlNUN0UzNXMwSkNnOGpzMFwiLFwiVXBsb2FkSURcIjpcIjE3ZThiODUxNzczNDRlYjFiYmM1MDAzMWU3NzQ3NGUyXCIsXCJVcGxvYWRIZWFkZXJcIjpudWxsLFwiU3RvcmFnZUhlYWRlclwiOm51bGx9XSIsInVwbG9hZEhvc3QiOiJ0b3MtZC14LWxmLnNuc3Nkay5jb20iLCJ1cmkiOiJ0b3MtY24taS1hOXJuczJybDk4L2JkM2RjZWViMzdmNzQwOTY5ZDEwYmYwYmY4YTM5NDZlLmpwZWciLCJ1c2VySWQiOiIifQ=="
    }
    hash_of_canonical_request = json.dumps(hash_of_canonical_request)
    string_to_sign = f'AWS4-HMAC-SHA256\n20241218T075358Z\n20241218/cn-north-1/imagex/aws4_request\n{hash_of_canonical_request}'

    # 计算签名
    signature = calculate_signature(string_to_sign, secret_key, region, service, date)
    print(f'签名结果: {signature}')
