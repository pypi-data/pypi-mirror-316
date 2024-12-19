import json
import requests


class UserMsg:
    def __init__(self, text, mode, conversationMainId):
        self.text = text
        self.mode = mode
        self.conversationMainId = conversationMainId


class DingTalkWebhook:
    def __init__(self, text, phones, webhook_id=None, webhook_url=None):
        self.text = text
        self.phones = phones
        self.webhook_id = webhook_id
        self.webhook_url = webhook_url


class ParamTest:
    def __init__(self, dict):
        self.dict = dict

    def get(self, key):
        return self.dict[key]


class ZhiwoAssistant:

    def __init__(self, param, local=True):
        self.param = param
        if param.get('authorization') is None or len(param.get('authorization')) == 0:
            raise ValueError('authorization参数不能为空')
        profile = param.get('authorization').split('#')[0]
        self.authorization = param.get('authorization').split('#')[1]
        self.refBusinessKey = param.get('refBusinessKey')
        self.conversationMainId = param.get('conversationMainId')
        self.mode = param.get('mode')
        if local:
            self.base_url = "http://localhost:8080"
        elif profile == 'test':
            self.base_url = "https://core-apigateway-test.renliwo.com/dep-service"
        elif profile == 'uat':
            self.base_url = "https://uat-core.renliwo.com/dep-service"
        elif profile == 'prod':
            self.base_url = ''
        else:
            raise ValueError('为止使用环境')

    def send_ding_talk_webhook(self, text, phones, webhook_id=None, webhook_url=None):
        ding_talk_webhook = DingTalkWebhook(text, phones, webhook_id, webhook_url)
        self.send_msg(ding_talk_webhook=ding_talk_webhook)

    def send_user_msg(self, text: str):
        # user_msg = UserMsg(text, self.mode, self.conversationMainId)
        self.send_msg(user_msg_text=text)

    def send_msg(self, user_msg_text: str = None, ding_talk_webhook: DingTalkWebhook = None):
        headers = {
            'Authorization': self.authorization,
            'refBusinessKey': self.refBusinessKey,
            'Content-Type': 'application/json'
        }

        multi_msg = {}
        if user_msg_text is not None:
            user_msg = UserMsg(user_msg_text, self.mode, self.conversationMainId)
            multi_msg['user_msg'] = user_msg.__dict__
        if ding_talk_webhook is not None:
            multi_msg['ding_talk_webhook'] = ding_talk_webhook.__dict__

        if not multi_msg:
            return False

        url = self.base_url + '/appsdk/sendMsg'
        data_json = json.dumps(multi_msg)
        response = requests.request('POST', url, headers=headers, data=data_json)
        if response.status_code != 200:
            print(f'发送消息 {data_json} 响应码不是200')
            return False
        else:
            response_json = response.json()
            response_code = response_json.get('code')
            if response_code != '200':
                print(f'发送消息 {data_json} 状态码不是200 response:{json.dumps(response_json)}')
                return False
            else:
                return True

    def get_sql_data_by_job_number(self, jobNumber, param=None):
        headers = {
            'Authorization': self.authorization,
            'refBusinessKey': self.refBusinessKey,
            'Content-Type': 'application/json'
        }

        payload = {
            'jobNumber': jobNumber,
            'paramJson': json.dumps(param)
        }

        url = self.base_url + '/appsdk/getSqlDataByJobNumber'
        data_json = json.dumps(payload)
        response = requests.request('POST', url, headers=headers, data=data_json)
        if response.status_code != 200:
            print(f'查询sql {data_json} 响应码不是200')
            return None
        else:
            response_json = response.json()
            response_code = response_json.get('code')
            if response_code != '200':
                print(f'查询sql {data_json} 状态码不是200 response:{json.dumps(response_json)}')
                return None
            else:
                result = response_json.get("result")
                if result is None:
                    print(f'查询sql {data_json} result为空 response:{json.dumps(response_json)}')
                    return None
                else:
                    return result

    def __str__(self):
        return f'ZhiwoAssistant(refBusinessKey={self.refBusinessKey}, authorization={self.authorization}, base_url={self.base_url})'


if __name__ == '__main__':
    # mode:0-正常消息 1-debug 2-调度测试
    param = ParamTest({
        'mode': 0,
        'authorization': 'authorization',
        'refBusinessKey': 'refBusinessKey',
        'conversationMainId': 'conversationMainId',
    })
    assistant = ZhiwoAssistant(
        param, local=False
    )
    sql_data = assistant.get_sql_data_by_job_number('jobNumber', '5007 5008')
    print(json.dumps(sql_data))

    assistant.send_user_msg("测试websocket消息")
    assistant.send_ding_talk_webhook("webhook", ['phone'], webhook_id="webhook_id")
    assistant.send_msg(user_msg_text='websocket plus',
                       ding_talk_webhook=DingTalkWebhook('webhook plus', ['phone'], webhook_url='https://webhook'))
