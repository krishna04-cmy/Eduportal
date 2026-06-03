from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FeePlan, Order, Cart
from students.models import Student
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import FeePlanSerializer

@login_required(login_url='/login/')
def fee_list(request):
    fee_plans = FeePlan.objects.all()
    cart_items = Cart.objects.filter(user=request.user)
    cart_count = cart_items.count()

    return render(request, 'fees/fee_list.html', {
        'fee_plans': fee_plans,
        'cart_count': cart_count,
    })

@login_required(login_url='/login/')
def cart_add(request, pk):
    fee_plan = get_object_or_404(FeePlan, pk=pk)

    if Cart.objects.filter(user=request.user, fee_plan=fee_plan).exists():
        messages.error(request, 'Already in cart!')
        return redirect('/fees/')

    Cart.objects.create(user=request.user, fee_plan=fee_plan)
    messages.success(request, 'Added to cart!')
    return redirect('/fees/')

@login_required(login_url='/login/')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.fee_plan.amount for item in cart_items)

    return render(request, 'fees/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required(login_url='/login/')
def cart_remove(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
    cart_item.delete()
    messages.success(request, 'Removed from cart!')
    return redirect('/fees/cart/')

@login_required(login_url='/login/')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, 'Cart is empty!')
        return redirect('/fees/')

    total = sum(item.fee_plan.amount for item in cart_items)

    try:
        student = Student.objects.get(name=request.user.username)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found!')
        return redirect('/fees/')

    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                student=student,
                fee_plan=item.fee_plan,
                amount=item.fee_plan.amount,
                status='paid',
                paid_at=timezone.now(),
            )
        cart_items.delete()
        messages.success(request, 'Payment successful!')
        return redirect('/fees/orders/')

    return render(request, 'fees/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'student': student,
    })

@login_required(login_url='/login/')
def order_list(request):
    try:
        student = Student.objects.get(name=request.user.username)
        orders = Order.objects.filter(student=student).order_by('-created_at')
    except Student.DoesNotExist:
        orders = []

    return render(request, 'fees/order_list.html', {
        'orders': orders,
    })


# ADMIN SIDE FEES PLAN ADD-----------------------------------------------------

@login_required(login_url='/login/')
def fee_plan_add(request):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can add fee plans!')
        return redirect('/fees/')
    
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        amount = request.POST['amount']
        duration = request.POST['duration']
        
        FeePlan.objects.create(
            name=name,
            description=description,
            amount=amount,
            duration=duration,
        )
        messages.success(request, 'Fee Plan added!')
        return redirect('/fees/')
    
    return render(request, 'fees/fee_plan_add.html')


@login_required(login_url='/login/')
def fee_plan_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can edit fee plans!')
        return redirect('/fees/')
    
    fee_plan = get_object_or_404(FeePlan, pk=pk)
    
    if request.method == 'POST':
        fee_plan.name = request.POST['name']
        fee_plan.description = request.POST['description']
        fee_plan.amount = request.POST['amount']
        fee_plan.duration = request.POST['duration']
        fee_plan.save()
        messages.success(request, 'Fee Plan updated!')
        return redirect('/fees/')
    
    return render(request, 'fees/fee_plan_edit.html', {'fee_plan': fee_plan})


@login_required(login_url='/login/')
def fee_plan_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can delete fee plans!')
        return redirect('/fees/')
    
    fee_plan = get_object_or_404(FeePlan, pk=pk)
    fee_plan.delete()
    messages.success(request, 'Fee Plan deleted!')
    return redirect('/fees/')

@login_required(login_url='/login/')
def all_orders(request):
    if not request.user.is_staff:
        messages.error(request, 'Only Admin can view all orders!')
        return redirect('/fees/')
    
    orders = Order.objects.all().order_by('-created_at')
    
    return render(request, 'fees/all_orders.html', {
        'orders': orders,
    })


# DRF ViewSet
class FeePlanViewSet(ModelViewSet):
    queryset = FeePlan.objects.all()
    serializer_class = FeePlanSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]