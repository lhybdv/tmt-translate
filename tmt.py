#!/bin/evn python
# coding=utf-8

import json
import re
import os
import sys

from workflow import Workflow

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models


class ICON(object):
    DEFAULT = 'icon.png'
    SOUND = 'sound.png'
    G_TRANSLATE = 'gtranslate.png'


def create_tmt_client():
    cred = credential.Credential(os.getenv("SecretId"), os.getenv("SecretKey"))

    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.ap-beijing.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

    return client


def translate_text(client, text, target) -> str:
    req = models.TextTranslateRequest()
    params = {
        "SourceText": text,
        "Source": "auto",
        "Target": target,
        "ProjectId": 0
    }
    req.from_json_string(json.dumps(params))
    resp = client.TextTranslate(req)

    return resp.TargetText

def is_chinese(text):
    return len(re.findall(r'[\u4e00-\u9fff]+', text)) == 0


def main():
    text = sys.argv[1]
    wf = Workflow()
    try:
        client = create_tmt_client()

        target = 'zh' if is_chinese(text) else 'en'
        result = translate_text(client, text, target)
    except Exception as err:
        result = err
        target = 'unknown'

    if type(result) != str:
        return

    wf.add_item(
        title=result,
        subtitle=u"复制到剪切板",
        valid=True,
        arg=result,
        icon=ICON.DEFAULT
    )

    title = result if target == 'en' else text
    wf.add_item(
        title=title,
        subtitle=u"回车听发音",
        valid=True,
        arg="~"+title,
        icon=ICON.SOUND,
    )

    wf.send_feedback()

if __name__ == u"__main__":
    main()
