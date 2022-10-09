'''
Author: xiaomin
Date: 2021-01-15 10:19:52
'''
import re

a = '{"utData":{"size":20,"number":0,"totalElements":1,"totalPages":1,"content":[{"userUid":"4968626353668038659","username":"autotest_devechi","accountSystemKey":"defat","nickname":null,"activated":true,"userAppAuthorityVO":[{"appKey":"autotest31610677018779","appName":"autotest3_1610677018779","appStatus":1,"authorities":[{"authorityKey":"autotest31610677018779_authority","name":"autotest31610677018779_edit","description":"authority1_edit","parent":null,"appKey":"autotest31610677018779"}],"authorityGroups":[{"authorityGroupKey":"autotest31610677018779_juese1","authorityGroupName":"juese1","authorityGroupParent":null,"description":"juese1","appKey":"autotest31610677018779","authorityEntities":[],"children":null}]}]}]},"utCode":0}'

pattern = re.compile('"totalElements":1,"totalPages":1,"content":(.*?),"username":"autotest_devechi"')

result = pattern.findall(a)
print(result)