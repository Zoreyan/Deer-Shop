from celery import shared_task
from django.utils import timezone
from .models import Shop
from datetime import timedelta
from apps.dashboard.models import Notification
from apps.user.models import User
from django.core.mail import send_mail
from django.conf import settings
import logging
from .models import Product
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)

@shared_task
def check_shop_payments():
    now = timezone.now()
    shops = Shop.objects.filter(is_active=True)
    for shop in shops:
        # Проверка срока оплаты
        time_until_due = shop.payment_due_date - now
        users = User.objects.filter(shop=shop)

        # Если срок оплаты прошёл
        if shop.payment_due_date <= now:
            if shop.auto_pay:
                if shop.balance >= shop.tariff.price:
                    shop.balance -= shop.tariff.price
                    shop.is_active = True
                    shop.payment_due_date = now + timedelta(days=30)
                    shop.payment_due_date = shop.payment_due_date.replace(minute=59, second=0, microsecond=0)
                    shop.save()
                    if shop.system_notifications:
                        notification = Notification.objects.create(
                            category="Тариф",
                            shop=shop,
                            title=f"Ваш тариф успешно обновлен!",
                        )
                        notification.is_not_read.set(users)
                    if shop.email_notifications:
                        for user in users:
                            if user.get_email_notification:
                                try:
                                    send_mail(
                                        subject="Тариф обновлён",
                                        message=f"Уважаемый {user.username}, ваш тариф успешно обновлён. Спасибо за оплату!",
                                        from_email=settings.DEFAULT_FROM_EMAIL,
                                        recipient_list=[user.email],
                                    )
                                except Exception as e:
                                    logger.error(f"Ошибка отправки почты: {e}")
                else:
                    shop.is_active = False
                    shop.save()
                    if shop.system_notifications:
                        notification = Notification.objects.create(
                            category="Тариф",
                            shop=shop,
                            title=f"Срок оплаты истёк, но ваш баланс недостаточен для оплаты.",
                        )
                        notification.is_not_read.set(users)
                    if shop.email_notifications:
                        for user in users:
                            if user.get_email_notification:
                                try:
                                    send_mail(
                                        subject="Срок оплаты истёк",
                                        message=f"Уважаемый {user.username}, срок оплаты истёк, но ваш баланс недостаточен для оплаты. Пожалуйста, пополните баланс для продолжения использования магазина.",
                                        from_email=settings.DEFAULT_FROM_EMAIL,
                                        recipient_list=[user.email],
                                    )
                                except Exception as e:
                                    logger.error(f"Ошибка отправки почты: {e}")
            else:
                shop.is_active = False
                shop.save()
                if shop.system_notifications:
                    notification = Notification.objects.create(
                        category="Тариф",
                        shop=shop,
                        title=f"Срок оплаты истёк, тариф не оплачен.",
                    )
                    notification.is_not_read.set(users)
                if shop.email_notifications:
                    for user in users:
                        if user.get_email_notification:
                            try:
                                send_mail(
                                    subject="Срок оплаты истёк",
                                    message=f"Уважаемый {user.username}, срок оплаты истёк, тариф не оплачен.",
                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                    recipient_list=[user.email],
                                )
                            except Exception as e:
                                logger.error(f"Ошибка отправки почты: {e}")


        # Если до срока оплаты осталось менее 1 часа
        elif time_until_due <= timedelta(hours=1):
            if shop.system_notifications and shop.balance < shop.tariff.price:
                notification = Notification.objects.create(
                    category="Тариф",
                    shop=shop,
                    title=f"До окончания тарифа осталось менее 1 часа, если оплата не будет произведена, ваш магазин будет заблокирован",
                )
                notification.is_not_read.set(users)
            if shop.email_notifications:
                for user in users:
                    if user.get_email_notification:
                        try:
                            send_mail(
                                subject="Магазин",
                                message="У вашего магазина не хватает средств для оплаты. При недостаточном балансе ваш магазин будет заблокирован.",
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=["recipient@example.com"],
                            )
                        except Exception as e:
                            logger.error(f"Ошибка отправки почты: {e}")


@shared_task
def check_product_stock(products, shop_id):
    """
    Задача для проверки продуктов на наличие минимального количества.
    Если количество меньше минимального, создаём одно уведомление с таблицей товаров.
    """
    if not products:  # Проверяем, что список продуктов не пуст
        return "No products provided."

    # Список продуктов с низким запасом
    low_stock_products = []

    try:
        # Получаем магазин
        shop = Shop.objects.get(id=shop_id)
    except Shop.DoesNotExist:
        return f"Shop with id {shop_id} does not exist."

    # Получаем пользователей, связанных с магазином
    users = User.objects.filter(shop=shop)

    # Обрабатываем каждый продукт
    for product_data in products:
        product_id = product_data.get('id')
        if not product_id:
            continue  # Пропускаем, если id продукта отсутствует

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue  # Пропускаем, если продукт не найден

        if product.quantity < product.min_quantity:
            low_stock_products.append({
                'name': product.name,
                'quantity': product.quantity,
                'min_quantity': product.min_quantity
            })

    # Если есть продукты с низким запасом, создаём уведомление
    if low_stock_products:
        if shop.system_notifications:
            notification_title = f"Низкий запас на {len(low_stock_products)} товар(ов)"
            notification_details = render_to_string(
                'user/notification_details_table.html',
                {'products': low_stock_products}
            )
            notification = Notification.objects.create(
                shop=shop,
                category="Товар",
                title=notification_title,
                details=notification_details
            )
            notification.is_not_read.set(users)

        # Отправка email-уведомлений, если включены
        if shop.email_notifications:
            for user in users:
                if user.get_email_notification:
                    try:
                        send_mail(
                            subject="Магазин - Низкий запас товаров",
                            message="Некоторые товары имеют низкий запас. Проверьте уведомления.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[user.email],
                        )
                    except Exception as e:
                        logger.error(f"Ошибка отправки почты пользователю {user.email}: {e}")

    return f"Checked products. Low stock found for {len(low_stock_products)} products."