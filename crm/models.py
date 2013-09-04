# coding=utf-8
from django.db import models
from django.db.models.query import QuerySet
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.utils import simplejson
from crm.util import generate_code

#产品状态
PRODUCT_STATUS = (
    (0, u"正常"),
    (1, u"停售"),
)

#客户热度
HOST_LEVEL=(
    (1,u"低热"),
    (2,u"中热"),
    (3,u"高热"),
            
)

#价值评估
RATING=(
    (1,u"低热"),
    (2,u"中热"),
    (3,u"高热"),     
)

#客户种类
CUSTOMER_TYPE=(
    (1,u"潜在客户"),
    (2,u"普通客户"),
    (3,u"VIP客户"), 
    (4,u"代理商"), 
    (5,u"合作伙伴"), 
    (6,u"失效客户"),           
)

#关系等级
RELATION_RATING=(
    (1,u"密切"),
    (2,u"较好"),
    (3,u"一般"), 
    (4,u"较差 "),                         
)

#客户来源
CUSTOMER_FROM=(
    (1,u"老客户"),
    (2,u"独立开发"),
    (3,u"代理商"),
    (3,u"公开招标"), 
    (3,u"其它"),            
)

#客户阶段
CUSTOMER_STATUS=(
    (1,u"售前跟踪"),
    (2,u"合同执行"),
    (3,u"合同期满"),              
)

#性别
SEX=(
    (0,u"男"),
    (1,u"女"),
)

#联系人分类
CONTACT_TYPE=(
    (1,u"特别重要"),
    (2,u"重要"),
    (3,u"普通"),
    (4,u"不重要"),
    (5,u"失效"),
)

#销售单类别
SALE_TYPE=(
    (1,u"产品销售"),
    (2,u"服务"),
    (3,u"业务合作"),
    (4,u"代理分销"),
    (5,u"其它"),
)

#销售状态
SALE_STATUS=(
    (1,u"新订单"),
    (2,u"已交货"),
    (3,u"已收款"),
    (4,u"已结束"),
    (5,u"已取消"),
)

#付款方式
PAY_MODE=(
    (1,u"支票"),
    (2,u"现金"),
    (3,u"银行汇款"),
    (4,u"网上银行"),
    (5,u"其它"),
)

#交货方式
DELIVER_TYPE=(
    (1,u"自己送货"),
    (2,u"邮寄"),
    (3,u"自取"),
    (4,u"其它"),
)

COST_TYPE=(
    (1,u"送礼"),
    (2,U"活动经费"),
    (3,U"其它"),
)



#分类
class Category(models.Model):
    name=models.CharField(max_length=100,verbose_name='名称')
    description=models.TextField(blank=True, null=True,verbose_name='描述')
    #ParentCategoryId
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural =verbose_name
        
#单位   
class Unit(models.Model):
    name=models.CharField(max_length=10,verbose_name='名称')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '单位'
        verbose_name_plural =verbose_name
    
#厂家
class Manufacturer(models.Model):
    name=models.CharField(max_length=128,verbose_name='名称')
    tel=models.CharField(max_length=30,blank=True, null=True,verbose_name='电话')
    website = models.URLField(blank=True, null=True,verbose_name='网址')
    remarks=models.TextField(blank=True, null=True,verbose_name='备注')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '供应商'
        verbose_name_plural =verbose_name

#计税公式      
class ComputingTax(models.Model):
    name=models.CharField(max_length=60,verbose_name='名称')
    expression=models.CharField(max_length=200,help_text="价格：A，成本：B；例子：(A-B)*0.01",verbose_name="公式")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '计税公式'
        verbose_name_plural =verbose_name
    
#产品
class Product(models.Model):
    name=models.CharField(max_length=128,verbose_name='名称')
    category=models.ForeignKey(Category,verbose_name='分类')
    
    status= models.SmallIntegerField(choices=PRODUCT_STATUS,verbose_name='状态',default=0)
    model =models.CharField(max_length=128,verbose_name='型号')
    manufacturer=models.ForeignKey(Manufacturer,verbose_name='供应商') #Many-to-one
    serviceDate=models.CharField(max_length=20,blank=True, null=True,verbose_name='保修期')
    unit = models.ForeignKey(Unit,verbose_name='单位')
    
    price=models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='价格')
    costprice=models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='成本价格')
    taxes=models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='税金')
    computingTax=models.ForeignKey(ComputingTax,verbose_name='计税公式')
    otherFee=models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='其它成本')
    discountRatel=models.DecimalField(max_digits=3,decimal_places=2,default=1.0,blank=True, null=True,verbose_name='折扣率')
    
    description=models.TextField(blank=True, null=True,verbose_name='产品说明')
    parameter=models.TextField(blank=True, null=True,verbose_name='规格') #技术参数 (规格）
    faq=models.TextField(blank=True, null=True,verbose_name='常见问题')
    remarks=models.TextField(blank=True, null=True,verbose_name='备注')
    create_time = models.DateTimeField(auto_now=True,verbose_name='创建时间')
    
    def to_json(self):
        if isinstance(self, QuerySet):
            return simplejson.dumps(self, cls=DjangoJSONEncoder,ensure_ascii=False) #ensure_ascii=False处理中文编码
        if isinstance(self, models.Model):
            set_obj = [self]
            set_str = simplejson.dumps(simplejson.loads(serialize('json', set_obj)),ensure_ascii=False)
            str_obj = set_str[1:len(set_str)-1]
        return str_obj

    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '产品'
        verbose_name_plural =verbose_name

#客户    
class Customer(models.Model):
    name=models.CharField(max_length=128,verbose_name='名称')
    is_host=models.BooleanField(verbose_name='是否热点客户')
    host_lever=models.SmallIntegerField(choices=HOST_LEVEL,verbose_name='热度')
    host_category=models.ManyToManyField(Category,blank=True, null=True,verbose_name='热点分类')
    host_memo=models.CharField(max_length=128,blank=True, null=True,verbose_name='热点说明')

    #基本信息
    short_name=models.CharField(max_length=64,blank=True, null=True,verbose_name='简称')
    code=models.CharField(max_length=64,verbose_name='编号')
    value_rating=models.SmallIntegerField(choices=RATING,blank=True, null=True,verbose_name='价值评估')
    credit_rating=models.SmallIntegerField(choices=RATING,blank=True, null=True,verbose_name='信用评估')
    customer_type=models.SmallIntegerField(choices=CUSTOMER_TYPE,blank=True, null=True,verbose_name='客户种类')
    relation_rating=models.SmallIntegerField(choices=CUSTOMER_STATUS,blank=True, null=True,verbose_name='客户阶段')
    customer_from=models.SmallIntegerField(choices=CUSTOMER_FROM,blank=True, null=True,verbose_name='客户来源')
    customer_info=models.TextField(blank=True, null=True,verbose_name='客户简介')
    
    #联系方式
    zipcode=models.CharField(max_length=16,blank=True, null=True,verbose_name='邮编')
    city=models.CharField(max_length=50,default="广州",blank=True, null=True,verbose_name='城市')
    area=models.CharField(max_length=50,default="天河",blank=True, null=True,verbose_name='区域')
    address=models.CharField(max_length=128,blank=True, null=True,verbose_name='地址')
    tel=models.CharField(max_length=30,blank=True, null=True,verbose_name='电话')
    website = models.URLField(blank=True, null=True,verbose_name='网址')
     
    remarks=models.TextField(blank=True, null=True,verbose_name='备注')
    create_time = models.DateTimeField(auto_now=True,verbose_name='创建时间')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '客户 '
        verbose_name_plural =verbose_name
    
#联系人
class Contact(models.Model):
    customer = models.ForeignKey(Customer,verbose_name='对应客户')
    #联系人
    name=models.CharField(max_length=20,blank=True, null=True,verbose_name='姓名')
    sex=models.SmallIntegerField(choices=SEX,verbose_name='性别')
    contact_type=models.SmallIntegerField(choices=CONTACT_TYPE,blank=True, null=True,verbose_name='联系人分类')
    preside=models.CharField(max_length=32,blank=True, null=True,verbose_name='负责业务')
    appellation=models.CharField(max_length=32,blank=True, null=True,verbose_name='称谓') #称谓,如：李总、王老师
    department=models.CharField(max_length=32,blank=True, null=True,verbose_name='部门')
    headship=models.CharField(max_length=32,blank=True, null=True,verbose_name='职务')
    
    tel=models.CharField(max_length=30,blank=True, null=True,verbose_name='电话')
    mobile=models.CharField(max_length=22,blank=True, null=True,verbose_name='手机')
    fax=models.CharField(max_length=22,blank=True, null=True,verbose_name='传真')
    email = models.EmailField(blank=True, null=True,verbose_name='邮箱')
    qq=models.CharField(max_length=20,blank=True, null=True,verbose_name='QQ')
    
    remarks=models.TextField(blank=True, null=True,verbose_name='备注')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '联系人 '
        verbose_name_plural =verbose_name
    
#销售
class Sale(models.Model):
    code=models.CharField(max_length=30,verbose_name='编号',default=generate_code('SALE'))
    invoice_no=models.CharField(max_length=30,blank=True, null=True,verbose_name='发票号码')
    identify_date=models.DateTimeField(verbose_name='签定日期') #销售单签定日期
    sale_type=models.SmallIntegerField(choices=SALE_TYPE,verbose_name='类型') #销售单类型
    sale_status=models.SmallIntegerField(choices=SALE_STATUS,verbose_name='状态') #销售状态
    
    customer = models.ForeignKey(Customer,verbose_name='客户')
    contactor=models.CharField(max_length=20,blank=True, null=True,verbose_name='联系人')
    tel=models.CharField(max_length=30,blank=True, null=True,verbose_name='电话')
    
    amount=models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='总金额') 
    gross_margin=models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='毛利') 
    pay_mode=models.SmallIntegerField(choices=PAY_MODE,blank=True, null=True,verbose_name='付款方式') 
    Receive=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True,verbose_name='已收款')
    Arrears=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True,verbose_name='欠款金额')
    ReceiveDate=models.DateTimeField(blank=True, null=True,verbose_name='收款时间')
    
    deliver_type=models.SmallIntegerField(choices=DELIVER_TYPE,blank=True, null=True,verbose_name='交货方式')
    deliver_address=models.CharField(max_length=100,blank=True, null=True,verbose_name='交货地址')
    delivery_date=models.DateTimeField(blank=True, null=True,verbose_name='交货时间')
    
    note = models.TextField(blank=True, null=True,verbose_name='备注') 
    creator_id=models.IntegerField(blank=True, null=True,verbose_name='录入人ID')
    creator_name=models.CharField(max_length=30,blank=True, null=True,verbose_name='录入人姓名')
    create_time = models.DateTimeField(auto_now=True,verbose_name='录入时间')
    
    def __unicode__(self):
        return self.code
    
    class Meta:
        verbose_name = '销售 '
        verbose_name_plural =verbose_name
    

#销售明细
class SaleDetail(models.Model):
    sale=models.ForeignKey(Sale,verbose_name='对应销售单')
    product=models.ForeignKey(Product,verbose_name='产品')
    
    sn=models.CharField(max_length=64,verbose_name='批号')
    produce_date=models.DateField(blank=True, null=True,verbose_name='生产日期')
    sterilized_date=models.DateField(blank=True, null=True,verbose_name='灭菌日期')
    validity_date=models.DateField(blank=True, null=True,verbose_name='有效期')
    
    num=models.IntegerField(verbose_name='数量')
    price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name='单价')
    costprice=models.DecimalField(max_digits=8,decimal_places=2,verbose_name='成本价格')
    taxes=models.DecimalField(max_digits=8,decimal_places=2,verbose_name='税金')
    discountRate1=models.DecimalField(max_digits=3,decimal_places=2,blank=True, null=True,verbose_name='折扣率',default=1.0)
    otherFee=models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='其它费用') 
    profit =models.DecimalField(max_digits=8,decimal_places=2,blank=True, null=True,verbose_name='利润')#根据  “数量X单价”--“成本单价X数量”--其它费用  算出毛利
    
    def __unicode__(self):
        return self.product.name
    
    class Meta:
        verbose_name = '销售明细 '
        verbose_name_plural =verbose_name
    
#发票
class Invoice(models.Model): 
    invoice_no=models.CharField(max_length=30,verbose_name='发票号码')
    receipt_date=models.DateField(blank=True, null=True,verbose_name='收到日期')
    Invoice_date=models.DateField(blank=True, null=True,verbose_name='开票日期')
    company=models.CharField(max_length=60,blank=True, null=True,verbose_name='开票单位')
    sum_money=models.DecimalField(max_digits=8,decimal_places=2,verbose_name='开票金额')
    
    note = models.TextField(blank=True, null=True,verbose_name='备注') 
    creator_id=models.IntegerField(blank=True, null=True,verbose_name='录入人ID')
    creator_name=models.CharField(max_length=30,blank=True, null=True,verbose_name='录入人姓名')
    create_time = models.DateTimeField(auto_now=True,verbose_name='录入时间')
    
    def __unicode__(self):
        return self.invoice_no
    
    class Meta:
        verbose_name = '发票'
        verbose_name_plural =verbose_name
    
#仓库
class Storehouse(models.Model):
    name=models.CharField(max_length=10,verbose_name='名称')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = '仓库'
        verbose_name_plural =verbose_name

#库存
class Inventory(models.Model):
    storehouse=models.ForeignKey(Storehouse,verbose_name='仓库')
    product=models.ForeignKey(Product,verbose_name='产品')
    sn=models.CharField(max_length=64,verbose_name='批号')
    produce_date=models.DateField(blank=True, null=True,verbose_name='生产日期')
    sterilized_date=models.DateField(blank=True, null=True,verbose_name='灭菌日期')
    validity_date=models.DateField(blank=True, null=True,verbose_name='有效期')
    num=models.IntegerField(verbose_name='数量')
    in_date=models.DateField(blank=True, null=True,verbose_name='入库日期')
    
    def __unicode__(self):
        return '%s_(%s)' % (self.product, self.sn)
    
    class Meta:
        verbose_name = '库存'
        verbose_name_plural =verbose_name
    
#退货
class Return(models.Model):
    sale=models.ForeignKey(Sale,verbose_name='对应销售单')
    product=models.ForeignKey(Product,verbose_name='产品')
    sn=models.CharField(max_length=64,blank=True, null=True,verbose_name='批号')
    num=models.IntegerField(verbose_name='数量')
    return_date=models.DateField(blank=True, null=True,verbose_name='退货日期')
    note = models.TextField(blank=True, null=True,verbose_name='备注') 
    
    def __unicode__(self):
        return '%s_(%s)' % (self.product, self.sn)
    
    class Meta:
        verbose_name = '退货'
        verbose_name_plural =verbose_name
    
#费用支出
class Cost(models.Model):
    title=models.CharField(max_length=64,verbose_name='主题')
    cost_type=models.SmallIntegerField(choices=COST_TYPE,blank=True, null=True,verbose_name='费用类型')
    amount =models.DecimalField(max_digits=8,decimal_places=2,verbose_name='总金额')
    cost_time = models.DateTimeField(verbose_name='时间')
    note = models.TextField(blank=True, null=True,verbose_name='备注') 
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = '费用支出'
        verbose_name_plural =verbose_name
    
    