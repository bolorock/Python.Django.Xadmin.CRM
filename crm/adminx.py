# coding=utf-8
import xadmin
from xadmin import views
from crm.models import *
from xadmin.layout import *
from xadmin.plugins.inline import Inline
from django.conf import settings
from django import forms

class ContactInline(object):
    model = Contact
    extra = 1
    style = 'accordion'

class SaleDetailInline(object):
    model = SaleDetail
    extra = 1
    style = 'accordion'
    
class CategoryAdmin(object):
    list_display=('name','description')
    search_fields=['name']
    
class UnitAdmin(object):
    list_display=('name',)
    search_fields=['name']
    
class ManufacturerAdmin(object):
    list_display=('name','tel','website','remarks')
    search_fields=['name','website']
    
class ProductAdmin(object):        
    list_display=('name','model','manufacturer','price','costprice','category','status','create_time')
    search_fields=['name','sn']
#     wizard_form_list = [
#         ('基本信息', ('name','category','status','unit')),
#         ('出厂信息', ('manufacturer','sn', 'model','serviceDate','parameter')),
#         ('价格信息', ('price','costprice','discountRatel')),
#         ('附加信息',('description','faq','remarks'))
#     ]
    raw_id_fields = ('manufacturer',)
    form_layout = Container(
        Fieldset('基本信息', Row('name','status'),Row('category','unit')),
        Fieldset('出厂信息', Row('manufacturer','serviceDate'),'model', 'parameter'),
        Fieldset('价格信息', Row('price','discountRatel'),Row('costprice','otherFee'),Row('computingTax','taxes')),
        Fieldset('附加信息', 'description','faq','remarks'),
        css_class='form-horizontal'
        )
    
    def media(self):
        media= forms.Media()  #+ self.vendor('saledetail.js')
        media.add_js([self.static('xadmin/vendor/product/product.js')])
        return self.get_media() + media
    
    
    
class CustomerAdmin(object):
    list_display=('name','host_lever','short_name','code','relation_rating','customer_from','area','tel')
    search_fields=['name']
    form_layout = (
        Container(
            TabHolder(
                Tab('基本信息',
                    Fieldset('热度设置',
                             'name',
                             Row('is_host','host_lever'),
                             Row('host_category','host_memo'),
                             description="客户的热度设置"
                             ),
                    Fieldset('基本设置',
                             Row('short_name','code'),
                             Row('value_rating','credit_rating'),
                             Row('customer_type','relation_rating'),
                             'customer_from',
                             'customer_info'
                             ),
                    css_id="tab_baseinfo"
                    ),
                Tab('联系方式',
                    Fieldset('联系信息',
                             Row('city','area'),
                             Row('zipcode','address'),
                             'tel','website',
                             'remarks'
                            ),
                    Inline(Contact),
                    css_id="tab_contact",
                    ),
            ),
            css_class='form-horizontal'
        )
    )
    inlines = [ContactInline]
    reversion_enable = True
    
class ContactAdmin(object):
    list_display=('customer','name','appellation','sex','contact_type','preside','department','headship','tel','mobile','email','qq')
    search_fields=['name']
  
class SaleAdmin(object):
    list_display=('code','identify_date','sale_type','sale_status','customer','invoice_no','amount','gross_margin','pay_mode','delivery_date','deliver_address')
    search_fields=['code']
    form_layout = (
        Container(
            TabHolder(
                Tab('销售信息',
                    Fieldset('基本信息',
                        Row('code','customer'),
                        Row('sale_type','sale_status'),
                        Row('contactor','tel'),
                        'identify_date'
                    ),
                    Fieldset('收款信息',
                        'pay_mode',
                        Row('amount', 'gross_margin'),
                        Row('Receive','Arrears'),
                        'ReceiveDate',
                        collapsed=True,
                        description="(【总金额】，【毛利】会根据销售明细自动算出)",
                    ),
                    Fieldset('交货信息',
                        Row('deliver_type','deliver_address'),
                        'delivery_date',
                         collapsed=True,          
                    ),
                    Fieldset('其它信息',
                        'note',
                         collapsed=True,
                    ),
                    css_id="tab_baseinfo"
                ),
                Tab('产品明细',
                    Inline(SaleDetail),
                    css_id="tab_productinfo"
                )
            ),
            css_class='form-horizontal'
        )          
    )
    inlines = [SaleDetailInline]
    reversion_enable = True
    
    def media(self):
        media= forms.Media()  #+ self.vendor('saledetail.js')
        media.add_js([self.static('xadmin/vendor/saledetail/saledetail.js')])
        return self.get_media() + media
    
class SaleDetailAdmin(object):
    list_display=('sale','product','num','price','costprice','discountRate1','otherFee')
    search_fields=['sale']
    readonly_fields = ('price','costprice',)
#     form_layout = Container(
#         Fieldset('产品信息','product', Row('num','price'),Row('costprice','otherFee'),'discountRate1'),
#         css_class='form-horizontal'
#         )

#计税方式
class ComputingTaxAdmin(object):
    list_display=('name','expression')
    
#发票
class InvoiceAdmin(object):
    list_display=('invoice_no','receipt_date','Invoice_date','company','sum_money','note')
    
#仓库
class StorehouseAdmin(object):
    list_display=('name',)
    
#库存
class InventoryAdmin(object):
    list_display=('storehouse','product','num','sn','produce_date','sterilized_date','validity_date','in_date')


#退货
class ReturnAdmin(object):
    list_display=('sale','product','sn','num','return_date','note')
    
class CostAdmin(object):
    list_display=('title','cost_type','amount','cost_time','note')
    
    
xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Unit,UnitAdmin)
xadmin.site.register(Manufacturer,ManufacturerAdmin)
xadmin.site.register(Product,ProductAdmin)
xadmin.site.register(Customer,CustomerAdmin)
xadmin.site.register(Contact,ContactAdmin)
xadmin.site.register(Sale,SaleAdmin)
xadmin.site.register(ComputingTax,ComputingTaxAdmin)
#xadmin.site.register(SaleDetail,SaleDetailAdmin)
xadmin.site.register(Invoice,InvoiceAdmin)
xadmin.site.register(Storehouse,StorehouseAdmin)
xadmin.site.register(Inventory,InventoryAdmin)
xadmin.site.register(Return,ReturnAdmin)
xadmin.site.register(Cost,CostAdmin)
