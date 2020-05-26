import sys

# Cache is a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library (e.g., collections.OrderedDict).
#       Implement the data structure yourself.
class Cache:
    # Initializes the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        self.map = [None] * n * 100
        self.head = None
        self.tail = None
        self.capacity = n
        self.current_len = 0

    def hash(self, key):
        num = 0
        for k in key:
            num += ord(k)
        return num % (self.capacity * 100)

    # Access a page and update the cache so that it stores the most
    # recently accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        idx = self.hash(url)
        print(idx, url)
        # Cacheに保存されてる要素にアクセスされた時
        if (self.map[idx] != None):
            # 最初の要素だったら
            if url == self.head['key']:
                return
            # 次の要素が格納されているか
            if self.map[idx]['next']:
                self.map[idx]['next']['prev'] = self.map[idx]['prev']
            # 前の要素が格納されているか
            if self.map[idx]['prev']:
                self.map[idx]['prev']['next'] = self.map[idx]['next']
            # 最後の要素だったら
            if url == self.tail['key']:
                self.tail = self.tail['prev']
            self.current_len -= 1
            
        self.current_len += 1

        # 今回アクセスされたページ
        page = {'key': url, 'value': contents, 'next': self.head, 'prev': None}
        # mapが空の時
        if (not self.tail):
            self.tail = page
        else :
            self.head['prev'] = page
        self.head = page

        self.map[idx] = page
        
        # 上限を超えた時
        if self.current_len > self.capacity:
            self.map.pop(self.hash(self.tail['key']))
            # 上限が1の時超えてしまうので
            if self.tail['prev'] :
                self.tail['prev']['next'] = None
            self.tail = self.tail['prev']
            self.current_len -= 1
            
        
    # Return the URLs stored in the cache. The URLs are ordered
    # in the order in which the URLs are mostly recently accessed.
    def get_pages(self):
        page = self.head
        pages = []
        while page:
            pages.append(page['key'])
            page = page['next']
        return pages


# Does your code pass all test cases? :)
def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)
    # Initially, no page is cached.
    equal(cache.get_pages(), [])
    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    equal(cache.get_pages(), ["a.com"])
    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["b.com", "a.com"])
    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["c.com", "b.com", "a.com"])
    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    equal(cache.get_pages(), ["a.com", "d.com", "c.com", "b.com"])
    cache.access_page("c.com", "CCC")
    print(cache.get_pages())
    equal(cache.get_pages(), ["c.com", "a.com", "d.com", "b.com"])
    cache.access_page("a.com", "AAA")
    equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
    cache.access_page("a.com", "AAA")
    equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    print(cache.get_pages())
    equal(cache.get_pages(), ["e.com", "a.com", "c.com", "d.com"])
    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    equal(cache.get_pages(), ["f.com", "e.com", "a.com", "c.com"])
    print("OK!")

# A helper function to check if the contents of the two lists is the same.
def equal(list1, list2):
    assert(list1 == list2)
    for i in range(len(list1)):
        assert(list1[i] == list2[i])

if __name__ == "__main__":
    cache_test()
    