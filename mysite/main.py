# coding=utf-8
'''
Created on 2013-8-14

@author: hgq
'''

from xadmin import views
import xadmin
from crm.models import *

class GolbeSetting2(object):
    site_title ="**管理系统";
#     globe_search_models = [Customer, Product]
    globe_models_icon = {
        #crm
        Category: 'adjust', 
        Unit: 'glass',
        Manufacturer:'home',
        Product:'gift',
        Customer:'user',
        Contact:'inbox',
        Sale:'briefcase',
       # SaleDetail:'tasks'
        ComputingTax:'book',
        Invoice:'file',
        Inventory:'tasks',
        Return:'random',
        Cost:'briefcase',
    }

def registe_menus():
    xadmin.site.register(views.CommAdminView, GolbeSetting2)