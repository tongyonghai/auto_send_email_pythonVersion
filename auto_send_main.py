import contract_estimate_mail
import daochu_material_tables
import decode_request_recorde
import ecn_code_register
import ecn_no_deliver_and_controlled_drawing_bill
import json
import os
import sys


if __name__== "__main__":
    with open(r"email_data.json",mode='r',encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        s1=  contract_estimate_mail.contract_estimate()
        s1.mainfun(load_dict['合同评审'])
        s2= daochu_material_tables.daochu_material()
        s2.mainfun(load_dict['导出物料总表'])
        s3=decode_request_recorde.decode_request_recorde()
        s3.mainfun(load_dict['解密审批记录'])
        s4= ecn_code_register.ecn_code_register()
        s4.mainfun(load_dict['ECN编号登记表-最新'])
        s5=ecn_no_deliver_and_controlled_drawing_bill.ecn_no_deliver_and_controlled_drawing_bill()
        s5.mainfun(load_dict['已受控图纸清单及未出货机器信息'])
