from django import template
from django.template.loader import render_to_string
from myapp.models import MenuItem
from myapp.utils import build_tree, mark_active_and_open

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name, template_name="tree_menu/menu.html"):
    request = context.get("request")
    if request is None:
        return ""

    current_path = request.path

    items = list(
        MenuItem.objects.filter(menu__name=menu_name)
        .select_related("parent")
        .only("id", "parent_id", "title", "url", "named_url", "order")  # оптимизация
    )

    if not items:
        return ""

    tree = build_tree(items)
    mark_active_and_open(tree, current_path)

    return render_to_string(
        template_name,
        {"tree": tree, "request": request},
        request=request
    )
