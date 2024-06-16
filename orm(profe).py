from datetime import date,datetime
from decimal import Decimal,ROUND_HALF_UP
import random
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
import os
import django
from django.db.models import F,Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min, Count
from django.db.models.functions import Substr
from argparse import Namespace
# Establece la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proy_crud.settings')
# Inicializa Django
django.setup()

from django.contrib.auth.models import User
from core.models import Brand, Supplier, Product, Category, Customer, PaymentMethod, Invoice, InvoiceDetail


def probar_orm():
    #py manage.py sqlmigrate core 0001 # presenta el codigo sql a migrar
    #py manage.py showmigrations # mustra las migraciones realizadas
    def create_user(create=False):
      if create:
        User.objects.create_user(username='dverap', password='davp1234', email='dan@example.com')
      users=User.objects.all()
      print("Listado de Usuarios")
      print(users.query)
      print(users)
    
    def script_brands(create=False):
      if create:
        user= User.objects.get(username='dverap')
        brand1 = Brand.objects.create(description="Nike", user=user)
        brand2 = Brand.objects.create(description="Arroz Flor", user=user,state=False)
        brand3 = Brand.objects.create(description="Atun Real", user=user)
        brand4 = Brand.objects.create(description="Azucar Valdez", user=user)
        brand5 = Brand.objects.create(description="Samsung", user=user)
      print("Listado de las marcas")
      brands= Brand.objects.all()
      print(brands)
      brands= Brand.active_brands.all()
      print(brands.query)
      for brand in brands: print(brand,brand.state) 
    
    def scripts_category(create=False):
      if create:
        user= User.objects.get(id=1)
        cat = Category(description='electrodomesticos',user=user)
        cat.save()
        Category(description='Atun',user=user).save()
      print("Listado de Categorias")
      print(Category.objects.all())
     
    def scripts_payment_Method(create=False):
      if create:
        user= User.objects.get(pk=1)
        PaymentMethod.objects.bulk_create([ 
          PaymentMethod(description="Contado",user=user), 
          PaymentMethod(description="Credito",user=user), 
          PaymentMethod(description="Tarjeta",user=user) 
        ]) 
      print("Listado de los Metodos de Pagos")
      print(PaymentMethod.objects.all())
      
    def scripts_customer(create=False):
      if create:
        user= User.objects.get(pk=1)
        Customer.objects.bulk_create([ 
          Customer(dni='0914192182',first_name='Daniel',last_name='Vera',address='Milagro',gender='M',date_of_birth=datetime.date(1970, 5, 21),user=user), 
          Customer(dni='0914192184',first_name='Miguel',last_name='Berrones',address='9 de Octubre',gender='M',date_of_birth=datetime.date(2017, 10, 10),user=user), 
          Customer(dni='0914192185',first_name='Yady',last_name='Bohorquez',address='Pedro Carbo',gender='F',date_of_birth=datetime.date(1975, 7, 10),user=user) 
        ]) 
      
      print("Listado de los Clientes")
      customers= Customer.objects.values('id','dni','first_name','last_name')
      customers2= Customer.objects.values_list('id','dni','first_name','last_name')
      print(customers)
      print(customers2)
      print(list(customers))
      print(list(customers2))
      
    def scripts_invoices():
      # Product.active_products.update(stock=F('stock') + 1000)    
      # Obtener el usuario de ejemplo
      user = User.objects.first()  # Supongamos que es el primer usuario creado
      # Obtener clientes y productos predefinidos
      customer = Customer.objects.last()  # Obtiene un objeto como e ultimo cliente
      # products = Product.objects.all()[0]# Se Obtiene un queryset con el 1,[0:3] 3 primeros, [-1] el ultimo producto dado el rango 931
      products = Product.objects.filter(description__in=('Jamon plumrose','Pepi cola','Leche'))# Se Obtiene 3 productos que coincida con la condicion 
      payment_method = PaymentMethod.objects.get(description='Contado') # se obtiene un objeto con el pago de contado
      # Crear la factura
      sale = Invoice.objects.create(
          customer=customer,
          payment_method=payment_method,
          issue_date=timezone.now(),
          subtotal=Decimal('0.00'),
          iva=Decimal('0.00'),
          discount=Decimal('0.00'),
          total=Decimal('0.00'),
          payment=Decimal('0.00'),
          change=Decimal('0.00'),
          status='F',
          user=user
      )
      # Crear detalles de factura para los productos comprados con una precision d eredondeo de 2 decimales
      redondeo,quantity,tsub,tiva=Decimal('0.01'),1,0,0
      for product in products:
          quantity = random.randint(1, 100)
          sub = quantity*product.price
          sub = sub.quantize(redondeo,rounding=ROUND_HALF_UP)
          iva = sub*product.iva/100
          iva = round(iva, 2)
          if quantity > product.stock:
            quantity = product.stock
          InvoiceDetail.objects.create(
              invoice=sale,
              product=product,
              cost=product.cost, 
              quantity=quantity,
              price=product.price,
              subtotal=sub,
              iva=iva  
          )
          # product.stock = product.stock - quantity
          # product.save()
          product.reduce_stock(quantity)
          #Product.objects.filter(id=product.id).update(stock=F('stock') - quantity)
          #Product.update_stock(product.id,quantity)
          tiva+=iva
          tsub+=sub
         
      sale.discount=0
      sale.iva=tiva
      sale.subtotal=tsub
      sale.total=tsub+tiva
      sale.save()
      

    def script_queryset():
       Product.objects.filter(id=13).update(state=False)
       product_all = Product.objects.all()
       product_values = Product.objects.values('id','description','price','stock','state')
       product_list = Product.objects.values_list('id','description','price','stock','state')
       product_filter = Product.objects.filter(state=True)
       product_manager = Product.active_products.all() 
       product_exclude = product_manager.exclude(price = 200)
       product_exclude = Product.active_products.all().exclude(price = 200)
       product_distinct = Product.objects.values('preci').distinct()
       print("Listado de objetos de Productos: all")
       print(product_all)
       print("Listado de objetos de Productos: values")
       print(product_values)
       print("Listado de objetos de Productos values_list")
       print(product_list)
       print("Listado de objetos de Productos list")
       prods_list = list(product_list)
       prods_id = [prod[2] for prod in prods_list]
       print(prods_list)
       print(prods_id,max(prods_id),sum(prods_id),random.choice(prods_id))
       print("Listado de objetos de Productos: filter")
       print(product_filter)
       print("Listado de objetos de Productos: manager")
       print(product_manager)
       print("Listado de objetos de Productos: exclude")
       print(product_exclude)
    # create_user()
    def script_get():
       print("Objeto Producto")
       try:
         product1 = Product.active_products.get(pk=3)
         print(product1)
       except ObjectDoesNotExist:
         print("El producto con el ID 1 no existe.")  
       try:  
         product2 = get_object_or_404(Product, pk=4)
         print(product2.id,product2.description)
       except Http404 as e:
         print("¡El producto con el ID 1 no existe!")
     
    def script_functions():
      # filtros operadores relacionales
      productos_mayor = Product.active_products.filter(stock__gt=1000) # stock > 100
      productos_mayor_igual = Product.active_products.filter(stock__gte=1000) # stock >= 100
      productos_menor = Product.active_products.filter(stock__lt=1000) # stock < 50
      productos_menor_igual = Product.active_products.filter(stock__lte=1000) # stock <= 50
      productos_igual = Product.active_products.filter(stock=1000) # stock = 50
      productos_mayor_menor = Product.active_products.filter(stock__gte=1000, stock__lte=1200).values('description','stock')# stock >=1000 y <=1200
      productos_rango = Product.objects.filter(stock__range=(1000, 1200))
      productos_in = Product.objects.filter(stock__in=(931, 1298))
      # print(Product.active_products.values('description','stock','expiration_date'))
      # print("Listados de productos >=1000 y <=1200")
      # print(productos_mayor_menor)
      # print(productos_rango.values_list('description','stock'))
      # print(list(productos_in.values('description','stock')))
      # filtros funciones string o cadenas
      productos_filtro1 = Product.objects.filter(description = 'Jamon plumrose')
      productos_filtro1 = Product.objects.filter(description__exact='Jamon plumrose')
      productos_filtro2 = Product.objects.filter(description__iexact='jamon plumrose')
      productos_filtro1 = Product.objects.filter(description__contains='jamon')
      productos_filtro2 = Product.objects.filter(description__icontains='jamon')
      productos_filtro1 = Product.objects.filter(description__startswith='jamon')
      productos_filtro2 = Product.objects.filter(description__istartswith='jamon')
      productos_filtro1 = Product.objects.filter(description__endswith='plumrose')
      productos_filtro2 = Product.objects.filter(description__iendswith='plumrose')
      productos_filtro1 = Product.objects.filter(description__in=['Jamon plumrose','carnes'])
      #encontrar "jamon" seguido de cualquier número de espacios y luego una palabra que comienza en minuscula
      productos_filtro1 = Product.objects.filter(description__regex=r'jamon\s+[a-z]\w*')
      productos_filtro2 = Product.objects.filter(description__iregex=r'jamon\s+[a-z]\w*')
      # print("Listados de productos -  strings")
      # print(productos_filtro1)
      # print(productos_filtro2)
      #filtros de fechas
      # print("Listados de productos - funciones fechas")
      # products_fecha = Product.objects.filter(expiration_date__lt=date(2024, 5, 13))# <2024-05-13
      # products_fecha = Product.objects.filter(expiration_date__year__in=(2024,2025))# 
      # products_fecha = Product.objects.filter(expiration_date__month=2)#
      # products_fecha = Product.objects.filter(expiration_date__day=13)# 
      # print(products_fecha.values('description','expiration_date'))
      # filtros logicos objeto Q
      print(Product.active_products.values('description','stock'))
      products_or = Product.objects.filter(Q(price__gt=2000) | Q(stock__lt=1000)) # > or <
      products_and = Product.objects.filter( Q(stock__gt=1000) & Q(stock__lte=1200)) # > and <=
      products_not = Product.objects.filter(~Q(stock__gt=1000)) # not > 1000
      products_union = Product.objects.filter((Q(stock__gt=1000) & Q(stock__lt=1200)) | Q(description__icontains='jamon'))
      print(products_union.values('description','stock'))
      
    def script_agregate():
      results_agregate = Product.objects.filter(stock__gte=1000).aggregate(total_precio=Sum('price'),
                                                   promedio_precio=Avg('price'),
                                                   precio_maximo=Max('price'),
                                                   precio_minimo=Min('price'),
                                                   total_productos=Count('id')
                                                  )
      # print(results_agregate,results_agregate['total_precio'])
      result = Product.objects.filter(state=True).values('line', 'brand__description').annotate(total_stock=Sum('stock')).order_by('line', 'brand__description').filter(total_stock__gte=2226)
      print(Product.objects.values('description','line','brand__description','price','stock'))
      print(result)
      print(result.query)
      products_total = Product.objects.annotate(name=Substr('description', 1, 5),total_value=F('price') * F('stock')).values('name','price','stock','total_value').order_by('description')
      print(products_total)
  
    def script_routes():
       invoices = Invoice.objects.all()
       #  invoices = Invoice.objects.values('id','issue_date','customer__first_name','total')
       invoices = Invoice.objects.select_related('customer','payment_method').values('id','issue_date','customer__first_name', 'payment_method__description','total')
       #print(invoices)
      #  for inv in invoices:
      #    f = Namespace(**inv)
      #    print(f"id:{f.id} fecha:{f.issue_date.strftime('%Y %B %d')} cliente:{f.customer__first_name} total:{inv['total']}")
        # print(f"id:{inv.id} fecha:{inv.issue_date.strftime('%Y %B %d')} cliente:{inv.customer.first_name} total:{inv.total}")
       # relacion inversa 
      #  customer = Customer.objects.get(id=1)
      #  invoices = customer.customer_invoices.all()
       #print(invoices) 
       customer_invoices = Customer.objects.prefetch_related('customer_invoices').all()
       print(customer_invoices)
       for cliente in customer_invoices: 
         print(cliente.get_full_name)
         for factura in cliente.customer_invoices.all():
                print(f"Factura ID: { factura.id }, Fecha de emisión: {factura.issue_date }, Total: { factura.total }")
         else:
           print("sin facturas")
    
    def update_delete():
      print(Product.objects.filter(price__lt=3))
      print(Product.objects.filter(price__lt=3).update(price=F('price') * 1.10))
      print(Brand.objects.filter(description='Galleta Maria').delete())
    # update_delete()
    # create_user()
    # script_brands()
    # scripts_category()
    # scripts_payment_Method()
    # scripts_customer()
    scripts_invoices()
    #script_queryset()
    #script_get()
    #script_functions()
    #script_agregate()
    # script_routes()
    

if __name__ == '__main__':
    probar_orm()

