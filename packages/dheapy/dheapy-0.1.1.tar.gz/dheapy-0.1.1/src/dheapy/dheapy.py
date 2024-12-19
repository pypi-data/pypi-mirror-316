from exceptions import Empty
from typing import Any, List, Optional, Union, Tuple


class DHeap:
    """A priority queue implemented with a d-ary heap."""

    class _Item:
        __slots__ = "_key", "_value", "_var"

        def __init__(
            self, key: Union[int, float], value: Any, var: str = "max"
        ) -> None:
            self._var = var
            self._value = value

            if self._var == "min":
                self._key = -key
            else:
                self._key = key

        def __lt__(self, other: Any) -> bool:
            return self._key < other._key

    class _Locator(_Item):
        __slots__ = "_index"

        def __init__(self, k: Union[int, float], v: Any, var: str, j: int) -> None:
            super().__init__(k, v, var)
            self._index = j

    def __init__(self, branching_factor: int = 2, variant: str = "max") -> None:
        """Create a new empty Priority Queue."""
        if branching_factor < 2:
            raise ValueError("Branching factor must be greater than 1.")

        self._data: List[Any] = []
        self._D = branching_factor
        self._variant = variant

    # Time complexity: O(1)
    def __len__(self) -> int:
        """Returns the number of items in the priority queue."""
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self) == 0
        # return self._data == []

    def _upheap(self, index: int) -> None:
        assert 0 <= index < len(self._data)

        parent_index = self._parent_index(index)

        if index > 0 and self._data[index] > self._data[parent_index]:
            self._swap(index, parent_index)
            self._upheap(parent_index)

    def _downheap(self, index: int) -> None:
        """Moves an item down toward the leaves of the heap."""

        if len(self._data) == 1:
            return self._data[0]

        assert 0 <= index < len(self._data)

        current_data = self._data[index]
        current_key = current_data._key
        current_index = index
        first_leaf_index = self._first_leaf_index()

        while current_index < first_leaf_index:
            child_index = self._highest_priority_child_index(current_index)
            assert child_index is not None

            if self._data[child_index]._key > current_key:
                self._data[current_index] = self._data[child_index]
                self._data[current_index]._index = current_index
                current_index = child_index
            else:
                break

        self._data[current_index] = current_data
        self._data[current_index]._index = current_index

    def _first_leaf_index(self) -> int:
        return (len(self._data) - 2) // self._D + 1

    def _first_child_index(self, index) -> int:
        """Computes the index of the first child of a heap node."""
        return (index * self._D) + 1

    def _parent_index(self, index) -> int:
        """Computes the index of the parent of a heap node."""
        return (index - 1) // self._D

    def _highest_priority_child_index(self, index) -> Optional[int]:
        first_index = self._first_child_index(index)
        size = len(self)
        last_index = min(first_index + self._D, size)

        if first_index >= size:
            return None

        highest_priority = -float("inf")
        index = first_index

        for i in range(first_index, last_index):
            if self._data[i]._key > highest_priority:
                highest_priority = self._data[i]._key
                index = i

        return index

    # Time complexity: O(1)
    def _viewtop(self) -> Any:
        """Return but do not remove (k, v) tuple with minimum key."""
        if self.is_empty():
            raise Empty("Priority queue is empty")

        item = self._data[0]
        return (item._key, item._value)

    def _swap_items(self, i: int, j: int) -> None:
        """Swap the items at indices i and j of array."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _swap(self, i: int, j: int) -> None:
        """Swap items and then reset locator indices."""
        self._swap_items(i, j)  # perform the swaps of items
        self._data[i]._index = i  # reset locator index (post-swap)
        self._data[j]._index = j  # reset locator index (post-swap)

    # Time complexity: O(log n) - amortized
    def _pop(self) -> Any:
        """Remove and return (k, v) tuple with minimum key."""
        if self.is_empty():
            raise Empty("Priority queue is empty")

        self._swap(0, len(self._data) - 1)  # put minimum item at the end
        item = self._data.pop()  # and remove it from the list
        self._downheap(0)  # then fix new root
        return (item._key, item._value)

    def _bubble(self, index: int) -> None:
        parent_index = self._parent_index(index)
        if index > 0 and self._data[index] > self._data[parent_index]:
            self._upheap(index)
        else:
            self._downheap(index)

    def _removeheap(self, loc: Any) -> Any:
        """Remove and return the (k,v) pair identified by Locator loc."""
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError("Invalid locator.")

        if j == len(self) - 1:
            self._data.pop()
        else:
            self._swap(j, len(self) - 1)
            self._data.pop()
            self._bubble(j)

        if self._variant == "min":
            return (loc._key * (-1), loc._value)
        else:
            return (loc._key, loc._value)

    def _updateheap(self, loc: Any, newkey: Union[int, float], newval: Any) -> None:
        """Update the key and value for the entry identified by Locator loc."""
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError("Invalid locator")

        loc._key = newkey
        loc._value = newval
        self._bubble(j)

    # Time complexity: O(1)
    def _location(self, key: Union[int, float], value: Any) -> Any:
        if self._variant == "min":
            key *= -1
        else:
            key = key

        ht = {
            item: True
            for item in self._data
            if item._key == key and item._value == value
        }
        return list(ht.keys())[0]

    # -------------------- Modules for Public Operations --------------------#
    # Time complexity: O(log n) -> amortized with dynamic array
    def insert(self, key: Union[int, float], value: Any) -> Any:
        """Add a key-value pair."""

        if not isinstance(key, (int, float)):
            raise TypeError("Priority must be a number either of integer or float type")

        token = self._Locator(
            key, value, self._variant, len(self._data)
        )  # initialize locator index
        self._data.append(token)
        self._upheap(len(self._data) - 1)
        return token

    # Time complexity: O(1)
    def peek(self) -> Any:
        if self.is_empty():
            raise Empty("Priority queue is empty.")

        if self._variant == "min":
            return self._viewtop()[0] * (-1), self._viewtop()[1]
        else:
            return self._viewtop()[0], self._viewtop()[1]

    # Time complexity: O(log n) -> amortized with dynamic array
    def delete(self) -> Any:
        if self.is_empty():
            raise Empty("Priority queue is empty")

        if len(self._data) == 1:
            last_item = self._data.pop()
            if self._variant == "min":
                return last_item._key * (-1), last_item._value
            return last_item._key, last_item._value

        if self._variant == "min":
            item = self._pop()
            return item[0] * (-1), item[1]
        else:
            return self._pop()

    # Time complexity: O(1)
    def show(self, indx: int) -> Any:
        if self.is_empty():
            raise Empty("Priority queue is empty")

        if not isinstance(indx, int):
            raise TypeError("Index must be of integer type")

        if 0 <= indx < len(self._data):
            if self._variant == "min":
                return self._data[indx]._key * (-1), self._data[indx]._value
            else:
                return self._data[indx]._key, self._data[indx]._value
        else:
            raise IndexError("Index is invalid")

    # Time complexity: O(log n)
    def removeitem(self, key: Union[int, float], value: Any) -> Tuple:
        if self.contains(key, value) == False:
            msg = f"Item ({key}, {value}) not found"
            raise ValueError(msg)

        loc = self._location(key, value)
        return self._removeheap(loc)

    # Time complexity: O(log n)
    def update(self, olditem: Tuple, newitem: Tuple) -> None:
        oldkey = olditem[0]
        oldval = olditem[1]

        if self.contains(oldkey, oldval) == False:
            msg = f"Item ({oldkey}, {oldval}) not found"
            raise ValueError(msg)

        loc = self._location(oldkey, oldval)

        newkey = newitem[0]
        newval = newitem[1]

        if self._variant == "min":
            newkey *= -1
        else:
            newkey = newkey

        self._updateheap(loc, newkey, newval)

    # Time complexity: O(1)
    def contains(self, key: Union[int, float], value: Any) -> bool:
        if self._variant == "min":
            key *= -1
        else:
            key = key

        ht = {
            item: True
            for item in self._data
            if item._key == key and item._value == value
        }

        return True if ht else False


def heapsorted(toSort: List, branching_factor: int = 2, variant: str = "max") -> List:
    if not isinstance(toSort, (list, tuple)):
        raise TypeError("Object to sort must be iterable")

    h = DHeap(branching_factor, variant)

    for i in toSort:
        h.insert(i[0], i[1])

    newArray = []

    while not h.is_empty():
        newArray.append(h.peek())
        h.delete()

    return newArray
