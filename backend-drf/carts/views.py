from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.response import Response
from products.models import Product
from rest_framework import status



class CartListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        # if created: # created is Boolean True/False
            # print('cart created')
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id') # product_id: 2
        quantity = request.data.get('quantity')

        if not product_id:
            return Response({"error": "product_id is required"})
        
        product = get_object_or_404(Product, id=product_id, is_active=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # item.quantity = item.quantity + quantity
            item.quantity += int(quantity)
            item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ManageCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        if 'change' not in request.data: # change should contain either +1 or -1
            return Response({"error": "change value is required"})
        
        change = int(request.data.get('change'))
        
        item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        product = item.product

        if change > 0:
            if item.quantity + change > product.stock:
                return Response({"error": "Not enough stock"})
            
        new_qty = item.quantity + change

        if new_qty <= 0:
            item.delete()
            return Response({"success": "Item removed"})
        
        item.quantity = new_qty
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, item_id):
        item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





            
        



