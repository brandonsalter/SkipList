import random
import math

class SkipList:

    class Node:
        def __init__(self, key, value, level):
            self.key = key
            self.value = value
            self.next = [None] * (level + 1) # only need singly linked towers

    def __init__(self):
        self.max_level = 8
        self.header = self.Node(float('-inf'), None, self.max_level)
        self.level = 0
        self.size = 0

    def coin_flips_result(self): # to avoid repeated flips
        level = 0
        while random.randint(0,1) == 1 and level < self.max_level:
            level += 1
        return level

    def update_max_level(self): # dynamically take maximum between log(size) or c=10
        self.max_level = max(10, int(math.log2(self.size)))

    def search(self, key, component=False):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.next[i] and current.next[i].key < key:
                current = current.next[i]
            update[i] = current

        if component:
            return update, current

        current = current.next[0]

        if current and current.key == key:
            return current
        else:
            return None

    def insert(self, key, value):
        update = self.search(key, component=True)[0]

        current = update[0].next[0]
        if current and current.key == key:
            current.value = value
            return

        new_level = self.coin_flips_result()

        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        new_node = self.Node(key, value, new_level)

        for i in range(new_level + 1):
            new_node.next[i] = update[i].next[i]
            update[i].next[i] = new_node

        self.size += 1
        self.update_max_level()

    def delete(self, key):
        update, current = self.search(key, component=True) 
        
        current = current.next[0]

        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].next[i] != current:
                    break
                update[i].next[i] = current.next[i]

            while self.level > 0 and self.header.next[self.level] is None:
                self.level -= 1

    def display(self):
        for i in range(self.level + 1):
            node = self.header.next[i]
            print('Level {}: '.format(i), end=' (-inf, None) -')
            while node:
                print('> ({}, {}) -'.format(node.key, node.value), end='')
                node = node.next[i]
            print('')

    def display_keys(self):
        for i in range(self.level + 1):
            node = self.header.next[i]
            print('Level {}: '.format(i), end=' (-inf) -')
            while node:
                print('> {} -'.format(node.key), end='')
                node = node.next[i]
            print('')

if __name__ == "__main__":
    skip_list = SkipList()
    skip_list.display()
    print('')

    skip_list.insert(14, 'alpha')
    skip_list.insert(23, 'beta')
    skip_list.insert(34, 'gamma')
    skip_list.insert(42, 'delta')
    skip_list.insert(50, 'epsilon')
    skip_list.insert(59, 'zeta')
    skip_list.insert(66, 'eta')
    skip_list.insert(72, 'theta')
    skip_list.insert(79, 'iota')

    skip_list.display_keys()

    key_to_search = 34
    result = skip_list.search(key_to_search)
    if result:
        print(f'\nKey ({key_to_search}) Value: {result.key}')
    else:
        print(f'\nKey {key_to_search} not found')

    key_to_delete = 50
    skip_list.delete(key_to_delete)
    print(f'\nKey Deleted: {key_to_delete}\n')
    skip_list.display_keys()
