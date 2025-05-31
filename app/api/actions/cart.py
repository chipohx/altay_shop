from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Cart, CartItem, Products
from app.api.models import Cart_sc, CartItem_sc, Product_sc

async def _get_or_create_cart(session_id: str, db: AsyncSession) -> Cart:
    # Try to find existing cart
    result = await db.execute(select(Cart).where(Cart.session_id == session_id))
    cart = result.scalar_one_or_none()
    
    if not cart:
        # Create new cart if not found
        cart = Cart(
            session_id=session_id,
            created_at=datetime.utcnow().isoformat()
        )
        db.add(cart)
        await db.commit()
        await db.refresh(cart)
    
    return cart

async def _get_cart(session_id: str, db: AsyncSession) -> Cart_sc:
    cart = await _get_or_create_cart(session_id, db)
    
    # Get cart items with product details
    result = await db.execute(
        select(CartItem, Products)
        .join(Products)
        .where(CartItem.cart_id == cart.id)
    )
    items = result.all()
    
    cart_items = []
    for item, product in items:
        cart_items.append(CartItem_sc(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product=Product_sc(
                id=product.id,
                category_id=product.category_id,
                title=product.title,
                description=product.description,
                price=product.price,
                main_photo=product.main_photo,
                additional_photos=product.additional_photos
            )
        ))
    
    return Cart_sc(
        id=cart.id,
        session_id=cart.session_id,
        created_at=cart.created_at,
        items=cart_items
    )

async def _add_to_cart(session_id: str, product_id: int, quantity: int, db: AsyncSession) -> Cart_sc:
    cart = await _get_or_create_cart(session_id, db)
    
    # Check if product exists
    result = await db.execute(select(Products).where(Products.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise ValueError("Product not found")
    
    # Check if item already in cart
    result = await db.execute(
        select(CartItem)
        .where(CartItem.cart_id == cart.id)
        .where(CartItem.product_id == product_id)
    )
    cart_item = result.scalar_one_or_none()
    
    if cart_item:
        # Update quantity if item exists
        cart_item.quantity += quantity
    else:
        # Create new cart item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)
    
    await db.commit()
    return await _get_cart(session_id, db)

async def _update_cart_item(session_id: str, item_id: int, quantity: int, db: AsyncSession) -> Cart_sc:
    cart = await _get_or_create_cart(session_id, db)
    
    # Find cart item
    result = await db.execute(
        select(CartItem)
        .where(CartItem.id == item_id)
        .where(CartItem.cart_id == cart.id)
    )
    cart_item = result.scalar_one_or_none()
    
    if not cart_item:
        raise ValueError("Cart item not found")
    
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        await db.delete(cart_item)
    else:
        # Update quantity
        cart_item.quantity = quantity
    
    await db.commit()
    return await _get_cart(session_id, db)

async def _remove_from_cart(session_id: str, item_id: int, db: AsyncSession) -> Cart_sc:
    cart = await _get_or_create_cart(session_id, db)
    
    # Find and remove cart item
    result = await db.execute(
        select(CartItem)
        .where(CartItem.id == item_id)
        .where(CartItem.cart_id == cart.id)
    )
    cart_item = result.scalar_one_or_none()
    
    if cart_item:
        await db.delete(cart_item)
        await db.commit()
    
    return await _get_cart(session_id, db)

async def _clear_cart(session_id: str, db: AsyncSession) -> Cart_sc:
    cart = await _get_or_create_cart(session_id, db)
    
    # Remove all items from cart
    await db.execute(
        select(CartItem)
        .where(CartItem.cart_id == cart.id)
        .delete()
    )
    await db.commit()
    
    return await _get_cart(session_id, db) 