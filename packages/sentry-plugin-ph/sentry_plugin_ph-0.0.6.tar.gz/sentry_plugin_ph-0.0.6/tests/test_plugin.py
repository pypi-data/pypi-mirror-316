import json
from unittest import TestCase, mock
from sentry_plugin_dingtalk.plugin import DingtalkPlugin

class MockProject:
    def __init__(self):
        self.slug = "test-project"

class MockEvent:
    def __init__(self):
        self.project = MockProject()
        self.project_id = 123
        self.event_id = "abc123"
        self.title = "Test Error"
        self.message = "Test error message"
        self.platform = "python"
        self.datetime = mock.Mock()
        self.datetime.strftime.return_value = "2024-03-14 12:00:00"
        self.release = "v1.0.0"
        self._tags = {"url": "http://example.com", "environment": "production"}

    def get_tag(self, tag):
        return self._tags.get(tag)

class MockGroup:
    def __init__(self):
        self.project = MockProject()

    def get_absolute_url(self, event_id=None):
        return f"http://sentry.example.com/issues/{event_id}"

    def is_ignored(self):
        return False

class TestDingtalkPlugin(TestCase):
    def setUp(self):
        self.plugin = DingtalkPlugin()
        self.event = MockEvent()
        self.group = MockGroup()

        # 模拟配置
        self.plugin.get_option = mock.Mock()
        self.plugin.get_option.side_effect = self._mock_get_option

    def _mock_get_option(self, key, project):
        if key == "options":
            return json.dumps([{
                "title": "测试标题 {projectName}",
                "markdown": "## 错误通知\n- 项目：{projectName}\n- 环境：{environment}\n- URL：{url}",
                "url": "https://demo-pre.puhuiboss.com",
                "recipientCodes": "TEST123",
                "condition": {
                    "tag": "{environment}",
                    "op": "==",
                    "value": "production"
                }
            }])
        elif key == "markdowns":
            return ""
        return None

    def test_is_configured(self):
        """测试配置检查"""
        self.assertTrue(self.plugin.is_configured(self.group.project))

    def test_get_tag_data(self):
        """测试标签数据获取"""
        tag_data = self.plugin.get_tag_data(self.group, self.event)
        self.assertEqual(tag_data["projectName"], "test-project")
        self.assertEqual(tag_data["projectId"], "123")
        self.assertEqual(tag_data["environment"], "production")

    def test_render_tag(self):
        """测试模板渲染"""
        tag_data = self.plugin.get_tag_data(self.group, self.event)
        template = "项目：{projectName}, 环境：{environment}"
        rendered = self.plugin.render_tag(self.event, tag_data, template)
        self.assertEqual(rendered, "项目：test-project, 环境：production")

    def test_check_condition(self):
        """测试条件判断"""
        # 测试相等条件
        self.assertTrue(self.plugin.check_condition("test", "==", "test"))
        self.assertFalse(self.plugin.check_condition("test", "==", "other"))
        
        # 测试包含条件
        self.assertTrue(self.plugin.check_condition("test string", "in", "string"))
        self.assertFalse(self.plugin.check_condition("test string", "in", "other"))

    @mock.patch('urllib.request.urlopen')
    def test_send_notification(self, mock_urlopen):
        """测试发送通知"""
        # 模拟所有 HTTP 响应
        responses = [
            {"data": "test_sign"},  # 第一个签名
            {"data": {"token": "test_token"}},  # token
            {"data": "push_sign"},  # 推送签名
            {"code": 0, "message": "success"}  # 最终推送响应
        ]
        
        mock_response = mock.Mock()
        mock_response.read.side_effect = [
            json.dumps(resp).encode('utf-8') for resp in responses
        ]
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # 调用通知方法
        self.plugin.notify_users(self.group, self.event)

        # 验证 HTTP 请求
        self.assertTrue(mock_urlopen.called)
        calls = mock_urlopen.call_args_list
        
        # 验证请求次数
        self.assertEqual(len(calls), 4)

        # 验证最后一个请求（发送消息）
        last_call = calls[-1]
        request = last_call.args[0]
        
        # 验证请求URL和数据
        self.assertTrue(request.full_url.endswith('/api/open/api/push'))
        request_data = json.loads(request.data.decode('utf-8'))
        self.assertEqual(request_data['data']['msgSource'], '前端团队')
        self.assertTrue('测试标题' in request_data['data']['msgTitle'])

    def test_parse_config(self):
        """测试配置解析"""
        config_list = self.plugin.parse_config(self.group)
        self.assertTrue(isinstance(config_list, list))
        self.assertEqual(len(config_list), 1)
        self.assertEqual(config_list[0]['recipientCodes'], 'TEST123')

    def test_send_msg_directly(self):
        """直接测试 send_msg 方法"""
        plugin = DingtalkPlugin()
        
        # 模拟 _make_request 方法
        def mock_make_request(url, data):
            if url.endswith('/api/open/getSign'):
                return {"data": "test_sign"}
            elif url.endswith('/api/open/api/auth'):
                return {"data": {"token": "test_token"}}
            elif url.endswith('/api/open/api/push'):
                return {"code": 0, "message": "success"}
            return {}
            
        plugin._make_request = mock_make_request
        
        # 准备测试数据
        test_title = "测试标题"
        test_text = """
        ## 错误通知
        - 项目：测试项目
        - 环境：生产环境
        - 错误：测试错误
        """
        test_item = {
            "url": "https://demo-pre.puhuiboss.com",
            "recipientCodes": "TEST123"
        }
        
        # 直接调用 send_msg 方法
        try:
            plugin.send_msg(test_title, test_text, test_item)
            self.assertTrue(True)  # 如果没有抛出异常，测试通过
        except Exception as e:
            self.fail(f"send_msg 调用失败: {str(e)}")

if __name__ == '__main__':
    import unittest
    unittest.main() 