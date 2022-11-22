# 接口自动化-new
## 1.前言
项目接口较多，测试场景多，版本更新影响范围广，为了能及时对改动影响的所有模块遍历测试场景，故开发此新版接口自动化。为了易于维护，选择了python+unittest+excel模式，当前版本只需在excel测试文件中进行模块、用例的增删改，实现了脚本和用例完全脱离。
> 环境：Python、Unittest、BeautifulReport、Excel

- BeautifulReport模块做了自定义修改，生成的html报告中用例描述由原先的函数描述改为测试执行函数中的title变量，请直接将文件夹BeautifulReport粘贴至X:\Python36\Lib\site-packages文件夹下

## 2.文件结构介绍

> **common**
> > 
> > **base_assert.py**:断言，目前仅支持assertEqual和assertIn，后续根据需要维护添加
> > 
> > **read_ini.py**:读取config.ini中的固定配置项如域名、token
> > 
> > **log.py**:日志，支持debug、info、warning、error、critical日志
> > 
> > **read_excel.py**:读取excel测试用例并初始化，包括用例中的关键字替换
> > 
> > **base_run.py**:单用例执行方法，setup函数、teardown函数、testcase函数
> > 
> > **request_func.py**:封装request方法，目前支持POST、GET，后续可根据需要维护添加
> > 
> > **trans_json.py**:封装处理字典json转换

> **config**
> 
> > config.ini:域名配置、token配置
> >
> > file_path.py:所有需要传入的文件地址

> **log**
> 
> > log.log:所有日志信息
> >
> > error.log:报错日志信息

> **report**
> > 
> > xxxx.html:报告html

> run.py:执行用例集

> test_case_data.xlsx:测试用例

## 3.测试用例参数
test_case_data.xlsx

用例参数 | 枚举 | 解释说明
---|--- |---
case_id | testcase001 | 测试用例编号，同时也是测试类名
case_module | test_createApp | 测试用例接口模块，同时也是测试执行函数名称，必须以test开头
case_name | (开发者)新建应用：正常调用2 | 测试用例描述
username | usernamexxx、/、空 | 用户名，需要切换账号时填入，如果使用上次登录的账号则使用"/"，如果不需要登录直接为空
password | passwordxxx、/、空 | 密码，同用户名一致
method | POST、GET | 接口类型，暂时仅支持post、get
url_path | /user2/xxx/xxx | 接口url地址
api_type | web、oauth | 接口网关类型，web接口则使用web网关的域名，如果是oauth则使用oauth域名
headers | {}、空 | 接口请求头，如果需要指定则填上，如果不需要则传入{}空括号，如果是公共接口则为空
request_body | {"xx":"xx_<time_stamp>"}、空 | 有入参则输入，没有为空，目前支持<time_stamp>标志转换为当前时间戳(保留13位)，对于新建的业务场景可以添加时间戳标志使用例可以重复执行
status_code | 200 | 预期状态码
resp_expect | "xx":"xx" | 预期返回结果，只要包含返回结果的关键字部分即可
use_data | test001 | 目前无实际作用，仅做标识
casetype | 正向、反向 | 目前无实际作用，仅做标识

注意：测试用例读取逻辑为一次性所有读取后批量处理需要替换的参数，如果多条用例都使用了<time_stamp>标识，会把所有标识替换成相同时间戳，所以编写测试用例时注意避免重复问题，例如创建多个应用可以使用"app1<time_stamp>"、"app2<time_stamp>"、"app3<time_stamp>"
## 4.关键代码
read_ini.py

```
def read_inifile():
    # 读取配置
    try:
        config = configparser.ConfigParser()
        config.read(file_path.config_file)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise
    return config

class GetIni:
    def __init__(self, inikey, inivalue, newvalue=None):
        # 初始化配置
        self.inikey = inikey
        self.inivalue = inivalue
        self.newvalue = newvalue
        self.config = read_inifile()

    def get_ini(self):
        # 返回配置文件的某项参数值
        try:
            convalues = self.config.get(self.inikey, self.inivalue)
        except Exception as e:
            MyLog.error('\033[31m {} \033[0m'.format(e))
            raise
        return convalues

    def write_ini(self):
        # 修改配置文件的某项参数值
        try:
            self.config.set(self.inikey, self.inivalue, self.newvalue)
            self.config.write(open(file_path.config_file, 'w'))
        except Exception as e:
            MyLog.error('\033[31m {} \033[0m'.format(e))
            raise
```
read_excel.py

```
def read_xlrd(excel_file):
    '''读取excel所有数据'''
    try:
        data=xlrd.open_workbook(excel_file)
        # 获取所有sheet名
        sheets=data.sheet_names()
        datafile=[]
        now=int(round(time.time() * 1000))
        for sheet in sheets:
            #遍历所有sheet的数据
            table=data.sheet_by_name(sheet)
            for rowNum in range(table.nrows):
                #去掉表头,替换时间戳标志
                if rowNum>0:
                    rowdata=table.row_values(rowNum)
                    rowData=[str(i).replace('<time_stamp>',str(now)) for i in rowdata]
                    datafile.append(rowData)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise
    return datafile

```
request_func.py

```
def set_headers(headers, token_type, access_token):
    # 设置header
    try:
        if headers != '' and 'Authorization' not in headers:
            # headers转换成dict，添加token，url拼接
            headers = trans_json.json_loads(headers)
            headers['Authorization'] = token_type+' '+access_token
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise
    return headers


def set_urls(api_type, url):
    # 拼接完整url
    try:
        login_url = GetIni('login_url', 'login_url').get_ini()
        http_url = GetIni('http_url', 'http_url').get_ini()
        if api_type == 'oauth':
            #果是oauth接口，拼接oauth域名
            url = login_url+url
        else:
            #拼接web域名
            url = http_url+url
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise
    return url


def print_log(method, url, params):
    # 打印请求方法、url、入参至报告和log
    print('url:[{}] {}'.format(method, url))
    print('request: {}'.format(params))
    MyLog.info('url:[{}] {}'.format(method, url))
    MyLog.info('request: {}'.format(params))


def request_post(url, headers, params, api_type):
    # post方法
    try:
        token_type = GetIni('http_token', 'token_type').get_ini()
        access_token = GetIni('http_token', 'access_token').get_ini()
        url = set_urls(api_type, url)
        print_log('POST', url, params)
        headers = set_headers(headers, token_type, access_token)
        response = requests.post(url=url, headers=headers, data=params)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise
    return response
```
base_run.py

```
def setup(self):
    # 每个用例执行前调用,判断是否需要登录新账号
    try:
        if self.data.username and self.data.username != '/':
            # 用例需要切换账号登录时，获取用户名密码登录，返回token写入config.ini
            param = {
                'username': self.data.username,
                'password': self.data.password,
                'grant_type': 'password',
                'scope': 'read'
            }
            # 获取配置中的登录token
            login_token = GetIni('login_token', 'Authorization').get_ini()
            # 获取登录url
            login = GetIni('login_url', 'login').get_ini()
            # 登录headers
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Authorization': login_token}
            # 登录requests
            response = request_func.request_post(
                login, headers, param, 'oauth')
            # 返参json解析
            response_data = trans_json.json_loads(response.text)
            # 新用户token写入配置
            GetIni('http_token', 'access_token',
                   response_data['access_token']).write_ini()
        else:
            pass
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise

def teardown(self):
    pass

def test_case(self):
    # 主体测试函数
    try:
        MyLog.info('------[正在执行：{}]------'.format(self.data.case_id))
        if self.data.method == 'POST':
            # post请求
            res = request_func.request_post(
                self.data.url_path, self.data.headers, self.data.request_body, self.data.api_type)
        elif self.data.method == 'GET':
            # get请求
            res = request_func.request_get(
                self.data.url_path, self.data.headers, self.data.api_type, self.data.request_body)
        # 打印信息至报告
        print_report(res.status_code, res.text, int(
            float(self.data.status_code)), self.data.resp_expect)
    except Exception as e:
        MyLog.error('\033[31m {} \033[0m'.format(e))
        raise
    assertion = Assertions()
    assertion.assert_code(self.data.case_id, res.status_code,
                          int(float(self.data.status_code)))
    assertion.assert_in_text(
        self.data.case_id, res.text, self.data.resp_expect)
    MyLog.info('执行成功')


def print_report(status_code, text, assert_code, resp_expect):
    # 打印code,response,expectcode,expectres
    print('status code: {}'.format(status_code))
    print('response: {}'.format(text))
    print('assert code: {}'.format(assert_code))
    print('assert response: {}'.format(resp_expect))
```
run.py创建测试用例集，程序入口文件

```
if __name__ == "__main__":
    # 读取测试用例
    datafile = read_excel.read_xlrd(file_path.test_data)
    case_numbers = len(datafile)

    # 获取当前时间
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    # 定义报告存放路径
    filename = file_path.report_file+now+'result.html'
    # 创建unittest套件
    testsuit = unittest.TestSuite()

    with open(filename, 'wb') as fp:
        # 遍历所有用例
        MyLog.info('************开始测试************')
        for case_num in range(case_numbers):
            data = InitData(datafile, case_num)
            data.get_data()
            # 创建测试类，data.case_module类名，data用例数据，title用例描述，setUp设置为setup函数，每条用例之前前调用，tearDown用例执行后调用，data.case_id测试用例执行函数
            newTestCase = type(data.case_module, (unittest.TestCase,), {
                               'data': data, 'title': data.case_name, 'tearDown': base_run.teardown, 'setUp': base_run.setup, data.case_id: base_run.test_case},)
            # 测试类加入unittest套件
            testsuit.addTest(unittest.TestLoader(
            ).loadTestsFromTestCase(newTestCase))
        #定义测试报告
        run = BeautifulReport(testsuit)
        run.report(filename=filename, description='UTyun用户中心autoapi测试报告')
        MyLog.info('************完成测试************')
```
## 5.生成测试报告
reportxxx.html

![image](http://note.youdao.com/yws/res/6021/WEBRESOURCEef337cda967c89c920a3cb7c3e17f60b)
## 6.日志文件
log.log

```
2020-12-21 02:41:59,344 - INFO - ------[正在执行：testcase004]------
2020-12-21 02:41:59,348 - INFO - url:[POST] https://xxxx/xxxxx/xxx/app
2020-12-21 02:41:59,349 - INFO - request: {"xxxxx":"xxxxx","description":"hhh","name": "xxxx"}
2020-12-21 02:41:59,466 - INFO - assert code--Success , status_code：[200] == expected_code: [200]
2020-12-21 02:41:59,467 - INFO - assert response--Success ,expected_msg: [{"utData":null,"utCode":0}] in body: [{"utData":null,"utCode":0}]
2020-12-21 02:41:59,468 - INFO - 执行成功
```
## 7.后续优化
- 改进接口之间的数据关联
- 断言处理的不够灵活
- 报告没有很好的模块划分
- 添加邮件发送功能
- 集成Jenkins定时任务
