import hashlib
import threading
import time

from django.http import HttpResponse
from django.utils.decorators import method_decorator
# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
from django.views.generic import View
from wechatpy import parse_message
from wechatpy.events import SubscribeEvent, SubscribeScanEvent
from wechatpy.messages import TextMessage
from wechatpy.replies import TextReply

from chatgpt_lsp.common.utils.cache import redis_cache
from chatgpt_lsp.common.utils.openai_api import OpenAI, set_answer
# from . import receive, reply
from chatgpt_lsp.settings import WECHAT


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class WechatView(View):
    def get(self, request):
        signature = str(request.GET.get("signature"))
        timestamp = str(request.GET.get("timestamp"))
        nonce = str(request.GET.get("nonce"))
        echostr = request.GET.get("echostr")

        token = WECHAT["TOKEN"]

        sortlist = [token, timestamp, nonce]
        sortlist.sort()
        sha1 = hashlib.sha1()
        sha1.update("".join(sortlist).encode('utf-8'))
        hashcode = sha1.hexdigest()
        print("handle/GET func: hashcode, signature: ", hashcode, signature)
        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("")
    
    def post(self, request):
        web_data = request.body
        openid = request.GET.get("openid")
        print("Handle Post webdata is ", web_data)
        recMsg = parse_message(web_data)
        if isinstance(recMsg, (SubscribeScanEvent, SubscribeEvent)):
            # 关注或扫二维码
            result = TextReply(content="欢迎使用宝仔的私人AI助理，请直接输入问题，有问题请私信我", message=recMsg).render()
            return HttpResponse(result)
        if isinstance(recMsg, TextMessage):
            ## 发送方帐号id
            # toUser = recMsg.FromUserName
            ## 开发者微信号id
            # fromUser = recMsg.ToUserName
            content = recMsg.content
            if content != "继续":
                s = threading.Thread(target=set_answer, args=(openid, content))
                s.start()
                time.sleep(2)
                answer = redis_cache.pop(openid)
                if answer:
                    answer = answer.decode('utf-8')
                else:
                    answer = "我正在思考中，请稍后回复【继续】获取回答"
            else:
                answer = redis_cache.pop(openid)
                if answer:
                    answer = answer.decode('utf-8')
                else:
                    answer = "请稍后，还没准备好参考答案"
            result = TextReply(content=answer, message=recMsg).render()
            # replyMsg = reply.TextMsg(toUser, fromUser, answer)
            # print(replyMsg.send())
            return HttpResponse(result)
        else:
            print("暂且不处理")
            return HttpResponse("success")

def chatgpt(request):
    return HttpResponse("gossss")
    # r = OpenAI()
    # answer = r.answer("用python实现一个斐波那契数列")
    # question = "用python实现一个斐波那契数列"
    # openid = "coco"
    # s = threading.Thread(target=set_answer, args=(openid, question))
    # s.start()
    # time.sleep(2)
    # answer = redis_cache.pop(openid)
    # print(answer)
    # return HttpResponse(answer)
