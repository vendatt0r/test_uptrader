
def build_tree(items):
    item_by_id = {item.id: item for item in items}
    for it in items:
        it.children_list = []
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

    found_in_subtree = False

    for item in tree:
        item.active = (item._resolved_url == current_path)
        item.open = False

        child_found = False
        if getattr(item, "children_list", None):
            child_found = mark_active_and_open(item.children_list, current_path)
            if child_found:
                item.open = True
                found_in_subtree = True

        if item.active:
            found_in_subtree = True
            for ch in getattr(item, "children_list", ()):
                ch.open = True

    return found_in_subtree
