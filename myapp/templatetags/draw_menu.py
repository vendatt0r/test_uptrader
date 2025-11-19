from django import template
from django.template.loader import render_to_string
from myapp.models import MenuItem
from myapp.utils import build_tree, mark_active_and_open

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name, template_name="tree_menu/menu.html"):
    """
    Тег для отрисовки меню по имени.
    Важно: для удовлетворения требования 'ровно 1 запрос к БД' мы делаем ОДИН запрос:
      MenuItem.objects.filter(menu__name=menu_name).select_related('parent','menu')
    Если возвращается пустой список — считаем, что меню пусто/не существует и возвращаем пустую строку.
    (Если важно отличать 'существует, но пусто' от 'не существует' — потребуется второй запрос к Menu,
     но тогда количество запросов станет >1).
    """
    request = context.get("request")
    if request is None:
        # без request невозможно определить active по URL
        return ""

    current_path = request.path

    # --- ровно 1 запрос к БД для получения всех пунктов меню (и данных меню через select_related)
    items = list(
        MenuItem.objects.filter(menu__name=menu_name)
        .select_related("parent")
        .only("id", "parent_id", "title", "url", "named_url", "order")  # оптимизация
    )
    # --------------------------------------------------------------

    if not items:
        # нет пунктов — ничего не выводим (см. объяснение в docstring)
        return ""

    tree = build_tree(items)
    mark_active_and_open(tree, current_path)

    # контекст можно дополнить классами и т.д.
    return render_to_string(
        template_name,
        {"tree": tree, "request": request},
        request=request
    )
