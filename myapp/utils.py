"""
Утилиты для сборки дерева меню и пометок active/open.
Вход — список объектов MenuItem (обычный список, уже извлечённый из БД).
"""

def build_tree(items):
    """Построить древовидную структуру: у каждого item добавится attribute children_list (список)."""
    item_by_id = {item.id: item for item in items}
    for it in items:
        it.children_list = []
        # заранее посчитаем url и сохраним, чтобы не вызывать reverse много раз
        try:
            it._resolved_url = it.get_url()
        except Exception:
            it._resolved_url = None

    roots = []
    for item in items:
        if item.parent_id and item.parent_id in item_by_id:
            parent = item_by_id[item.parent_id]
            parent.children_list.append(item)
        else:
            roots.append(item)
    return roots


def mark_active_and_open(tree, current_path):
    """
    Помечает элементы:
      - item.active = True, если item._resolved_url == current_path
      - item.open = True для всех предков активного элемента
      - а также открывает первые уровни под активным элементом (т.е. children активного получают .open = True)
    Возвращает True если в поддереве найден активный элемент.
    """
    found_in_subtree = False

    for item in tree:
        item.active = (item._resolved_url == current_path)
        # по-умолчанию закрыт
        item.open = False

        # рекурсивно обработаем детей
        child_found = False
        if getattr(item, "children_list", None):
            child_found = mark_active_and_open(item.children_list, current_path)
            if child_found:
                # если в дочерней ветке найден активный — открыть текущий (все выше активного раскрыты)
                item.open = True
                found_in_subtree = True

        if item.active:
            found_in_subtree = True
            # раскрываем первый уровень под активным пунктом
            for ch in getattr(item, "children_list", ()):
                ch.open = True

    return found_in_subtree
