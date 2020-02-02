import  os

class Trie:
    def __init__(self):
        self._items = []
        self._children = None

    def get(self, parts, fallback=None):
        if len(parts) == 0:
            return self
        if fallback is None:
            fallback = Trie()
        if self._children is None:
            self._children = dict()
        if type(parts) == str:
            return self._children.get(parts, fallback)
        first, *others = parts
        if first not in self._children:
            self._children[first] = fallback
        return self._children[first].get(others)

    def append(self, item):
        self._items.append(item)

    def keys(self):
        if self._children is None:
            return []
        return self._children.keys()

    def items(self):
        if self._children is None:
            return []
        return self._children.items()

    def traverse(
            self,
            path,
            file_name,
            item_map,
            directory_map,
            level=0,
            separate_items=False,
            get_item_name=None
    ):
        mapper = item_map
        if separate_items:
            assert get_item_name is not None
            mapper = get_item_name
        os.makedirs(path)
        if file_name is not None and directory_map is not None:
            index = directory_map(
                level,
                [mapper(item) for item in self._items],
                self.keys(),
                os.path.basename(path),
            )
            with open(os.path.join(path, file_name), 'w') as file:
                file.write(index)
        if separate_items:
            for item in self._items:
                with open(os.path.join(path, get_item_name(item)), 'w') as file:
                    file.write(item_map(item))
        for name, trie in self.items():
            trie.traverse(
                path=os.path.join(path, name),
                file_name=file_name,
                item_map=item_map,
                directory_map=directory_map,
                level=level + 1,
                separate_items=separate_items,
                get_item_name=get_item_name
            )


def add_trie_path(trie, parts):
    if len(parts) == 0:
        return trie
    first, *other = parts
    trie._children[first] = add_trie_path(trie.get(first), other)
    return trie


def add_trie_item(trie, path, item):
    trie.get(path).append(item)
    return trie

