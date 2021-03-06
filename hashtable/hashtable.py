class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        self.capacity = capacity
        self.data = [None] * capacity
        self.entries = 0

    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here
        return len(self.data)

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # Your code here
        return self.entries / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here
        fnv_prime = 1099511628211
        offset_basis =  14695981039346656037
        hash_value = offset_basis
        key_utf8 = key.encode()
        for byte in key_utf8:
            hash_value = hash_value ^ byte
            hash_value = hash_value * fnv_prime
        return hash_value
        

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here
        hash_value = 5381
        for char in key:
            hash_value = (hash_value * 33) + ord(char)
        return hash_value

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)
        new_entry = HashTableEntry(key, value)
        current = self.data[index]
        if self.data[index] is None:
            self.data[index] = HashTableEntry(key, value)
            self.entries += 1
            if self.get_load_factor() > 0.7:
                self.resize(self.capacity * 2)
        elif current.key is key:
            current.value = value
        else:
            self.data[index] = new_entry
            new_entry.next = current
            self.entries += 1
            if self.get_load_factor() > 0.7:
                self.resize(self.capacity * 2)
     

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)
        current = self.data[index]
        previous = current
        if current.key is key:
            current.value = None
            current = None
            self.entries -= 1
            if self.get_load_factor() < 0.2 and self.capacity // 2 >= 8:
                self.resize(self.capacity // 2)
        elif current is None:
            print("Key was not found.")
        else:
            while current is not None:
                previous = current
                current = current.next
                if current.key is key:
                    current.value = None
                    previous.next = None
                    self.entries -= 1
                    if self.get_load_factor() < 0.2 and self.capacity // 2 >= 8:
                        self.resize(self.capacity // 2)
                    return 
            print("Key was not found.")

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        index = self.hash_index(key)
        
        if self.data[index] is None:
            return None
        if self.data[index].key is key:
            return self.data[index].value
        else:
            current = self.data[index]
            while current.next is not None:
                current = current.next
                if current.key is key:
                    return current.value
            return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        new_ht = HashTable(new_capacity)
        for entry in self.data:
            if entry:
                new_ht.put(entry.key, entry.value)
                if entry.next:
                    current = entry
                    while current.next:
                        current = current.next
                        new_ht.put(current.key, current.value)
        self.data = new_ht.data
        self.capacity = new_ht.capacity

if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")
    z = ht.get("line_12")
    print(f"Get Line 12: {z}")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

ht2 = HashTable(8)

print(f"Capacity: {ht2.capacity}")
ht2.put("key-0", "val-0")
ht2.put("key-1", "val-1")
ht2.put("key-2", "val-2")
ht2.put("key-3", "val-3")
ht2.put("key-4", "val-4")
ht2.put("key-5", "val-5")
ht2.put("key-6", "val-6")
ht2.put("key-7", "val-7")

print(f"Capacity: {ht2.capacity}")
ht2.put("key-8", "val-8")
ht2.put("key-9", "val-9")
ht2.put("key-10", "val-10")
ht2.put("key-11", "val-11")
ht2.put("key-12", "val-12")
ht2.put("key-13", "val-13")
ht2.put("key-14", "val-14")
ht2.put("key-15", "val-15")
x = ht2.get("key-15")
print(f"Get for key-15: {x}")
print(f"Capacity: {ht2.capacity}")

ht2.delete("key-15")
ht2.delete("key-14")
ht2.delete("key-13")
ht2.delete("key-12")
ht2.delete("key-11")
ht2.delete("key-10")
ht2.delete("key-9")
ht2.delete("key-8")
x = ht2.capacity // 2
print(f"Cap // 2: {x}")
ht2.resize(x)
print(f"Capacity after resize: {ht2.capacity}")
y = ht2.get_load_factor()
print(f"Load Factor: {y}")
print(f"Entries: {ht2.entries}")
print(f"Capacity: {ht2.capacity}")
ht2.delete("key-7")
ht2.delete("key-6")
ht2.delete("key-5")
y = ht2.get_load_factor()
print(f"Load Factor: {y}")
print(f"Entries: {ht2.entries}")
print(f"Capacity: {ht2.capacity}")
ht2.delete("key-4")
ht2.delete("key-3")
ht2.delete("key-2")
y = ht2.get_load_factor()
print(f"Load Factor: {y}")
print(f"Entries: {ht2.entries}")
print(f"Capacity: {ht2.capacity}")

# def slowfun_too_slow(x, y):
#     v = math.pow(x, y)
#     v = math.factorial(v)
#     v //= (x + y)
#     v %= 982451653

#     return v
import math
v = math.pow(3, 5)
print(v)
v = math.factorial(int(v))
print(v)
v //= (3 + 5)
print(v)
v %= 982451653
print(v)