// Original C++17 experiments. These test the host library, not historic SGI internals.
#include <algorithm>
#include <cassert>
#include <functional>
#include <iostream>
#include <iterator>
#include <list>
#include <map>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <unordered_map>
#include <vector>
#include <deque>

struct Counted {
    static int alive;
    static int copies;
    static int fail_at;
    int value;
    explicit Counted(int v) : value(v) { ++alive; }
    Counted(const Counted& other) : value(other.value) {
        if (++copies == fail_at) throw std::runtime_error("planned copy failure");
        ++alive;
    }
    ~Counted() { --alive; }
};
int Counted::alive = 0;
int Counted::copies = 0;
int Counted::fail_at = -1;

int category(std::input_iterator_tag) { return 1; }
int category(std::forward_iterator_tag) { return 2; }
int category(std::bidirectional_iterator_tag) { return 3; }
int category(std::random_access_iterator_tag) { return 4; }

int main() {
    std::vector<std::string> passed;
    {
        Counted sources[] = {Counted(1), Counted(2), Counted(3)};
        assert(Counted::alive == 3);
        std::allocator<Counted> storage;
        Counted* raw = storage.allocate(3);
        assert(Counted::alive == 3); // Allocation does not construct Counted objects.
        Counted::copies = 0;
        Counted::fail_at = 2;
        bool threw = false;
        try {
            std::uninitialized_copy(std::begin(sources), std::end(sources), raw);
        } catch (const std::runtime_error&) {
            threw = true;
        }
        assert(threw && Counted::alive == 3); // Successfully copied prefix was destroyed.
        Counted::copies = 0;
        Counted::fail_at = -1;
        auto end = std::uninitialized_copy(std::begin(sources), std::end(sources), raw);
        assert(end == raw + 3 && Counted::alive == 6);
        std::destroy(raw, end);
        assert(Counted::alive == 3);
        storage.deallocate(raw, 3);
    }
    assert(Counted::alive == 0);
    passed.push_back("lifetime-and-uninitialized-copy-rollback");
    {
        using P = std::iterator_traits<const int*>;
        static_assert(std::is_same<P::value_type, int>::value, "value_type excludes const");
        static_assert(std::is_same<P::reference, const int&>::value, "reference preserves const");
        assert(category(std::iterator_traits<std::vector<int>::iterator>::iterator_category{}) == 4);
        assert(category(std::iterator_traits<std::list<int>::iterator>::iterator_category{}) == 3);
        std::list<int> values{1, 2, 3, 4, 5};
        auto at = values.begin();
        std::advance(at, 3);
        assert(*at == 4 && std::distance(values.begin(), at) == 3);
    }
    passed.push_back("traits-and-category-dispatch");
    {
        std::vector<int> values{1};
        const auto old_capacity = values.capacity();
        auto old_iterator = values.begin();
        (void)old_iterator; // Never use after capacity increases.
        while (values.size() <= old_capacity) values.push_back(2);
        assert(values.capacity() > old_capacity);
        assert(values.front() == 1);
        // Reallocation invalidates old iterators; do not inspect one to 'test' invalidation.
    }
    passed.push_back("vector-reallocation-without-dangling-access");
    {
        std::list<int> source{1, 2, 3}, destination{9};
        auto moving = std::next(source.begin());
        int* identity = std::addressof(*moving);
        destination.splice(destination.end(), source, moving);
        assert((std::vector<int>(source.begin(), source.end()) == std::vector<int>{1, 3}));
        assert((std::vector<int>(destination.begin(), destination.end()) == std::vector<int>{9, 2}));
        assert(*moving == 2 && std::addressof(*moving) == identity);
    }
    passed.push_back("list-splice-node-identity");
    {
        std::deque<int> values;
        for (int i = 0; i < 1000; ++i) values.push_back(i);
        values.push_front(-1);
        assert(values[501] == 500 && *(values.begin() + 1000) == 999);
        assert(std::distance(values.begin(), values.end()) == 1001);
    }
    passed.push_back("deque-random-access");
    {
        std::vector<int> values{2, 8, 1, 8, 5};
        std::make_heap(values.begin(), values.end());
        const auto size = values.size();
        std::pop_heap(values.begin(), values.end());
        assert(values.size() == size && values.back() == 8);
        assert(std::is_heap(values.begin(), values.end() - 1));
        values.pop_back();
        assert(values.size() == size - 1 && std::is_heap(values.begin(), values.end()));
    }
    passed.push_back("pop-heap-does-not-erase");
    {
        std::map<int, std::string> values{{2, "two"}, {1, "one"}};
        static_assert(std::is_const<typename std::remove_reference<decltype(values.begin()->first)>::type>::value,
                      "map key is const");
        values.begin()->second = "ONE";
        assert(values.begin()->first == 1 && values.at(1) == "ONE");
        std::unordered_map<int, int> hash{{1, 10}, {6, 60}, {11, 110}};
        const auto count = hash.size();
        hash.rehash(37);
        std::size_t seen = 0;
        for (std::size_t b = 0; b < hash.bucket_count(); ++b) {
            for (auto it = hash.begin(b); it != hash.end(b); ++it) {
                assert(hash.bucket(it->first) == b);
                ++seen;
            }
        }
        assert(seen == count && hash.at(6) == 60); // No fixed bucket count or traversal order.
    }
    passed.push_back("map-key-policy-and-hash-buckets");
    {
        std::vector<int> left{1, 2, 3, 4, 5};
        auto end = std::copy(left.begin() + 2, left.end(), left.begin());
        assert(end == left.begin() + 3 && (left == std::vector<int>{3, 4, 5, 4, 5}));
        std::vector<int> right{1, 2, 3, 4, 5};
        auto start = std::copy_backward(right.begin(), right.begin() + 3, right.end());
        assert(start == right.begin() + 2 && (right == std::vector<int>{1, 2, 1, 2, 3}));
    }
    passed.push_back("legal-copy-directions");
    {
        std::vector<int> values{0, 1, 0, 2, 0, 3};
        const auto size = values.size();
        auto new_end = std::remove(values.begin(), values.end(), 0);
        assert(values.size() == size && std::distance(values.begin(), new_end) == 3);
        assert((std::vector<int>(values.begin(), new_end) == std::vector<int>{1, 2, 3}));
        values.erase(new_end, values.end());
        assert(values.size() == 3);
        std::vector<int> groups{1, 1, 2, 1, 1};
        new_end = std::unique(groups.begin(), groups.end());
        assert(groups.size() == 5);
        assert((std::vector<int>(groups.begin(), new_end) == std::vector<int>{1, 2, 1}));
    }
    passed.push_back("logical-end-is-not-erasure");
    {
        std::list<int> values{1, 2, 2, 2, 5};
        auto low = std::lower_bound(values.begin(), values.end(), 2);
        auto high = std::upper_bound(values.begin(), values.end(), 2);
        assert(std::distance(values.begin(), low) == 1);
        assert(std::distance(low, high) == 3);
        assert(std::lower_bound(values.begin(), values.end(), 9) == values.end());
    }
    passed.push_back("list-binary-bounds-and-distance");
    {
        std::vector<int> values{4, 2, 2, 8, 1, 2, 7};
        auto ordered = values;
        std::sort(ordered.begin(), ordered.end());
        auto nth = values.begin() + 3;
        std::nth_element(values.begin(), nth, values.end());
        assert(*nth == ordered[3]);
        for (auto i = values.begin(); i != nth; ++i)
            for (auto j = nth; j != values.end(); ++j) assert(!(*j < *i));
        auto same_multiset = values;
        std::sort(same_multiset.begin(), same_multiset.end());
        assert(same_multiset == ordered);
    }
    passed.push_back("nth-element-with-duplicate-values");
    {
        std::vector<int> values{1, 2, 3};
        std::for_each(values.begin(), values.end(), [](int& value) { value += 10; });
        assert((values == std::vector<int>{11, 12, 13}));
        auto reverse = values.rbegin();
        assert(reverse.base() == values.end() && *reverse == 13);
        ++reverse;
        assert(reverse.base() == values.end() - 1 && *reverse == 12);
        std::vector<int> destination;
        std::copy(values.rbegin(), values.rend(), std::back_inserter(destination));
        assert((destination == std::vector<int>{13, 12, 11}));
    }
    passed.push_back("for-each-reference-and-iterator-adapters");
    {
        std::vector<int> values{1, 4, 9, 16};
        std::vector<int> differences(values.size());
        std::adjacent_difference(values.begin(), values.end(), differences.begin());
        assert((differences == std::vector<int>{1, 3, 5, 7}));
        assert(std::accumulate(values.begin(), values.end(), 0) == 30);
        assert(std::accumulate(values.begin(), values.end(), 100, std::minus<int>{}) == 70);
        std::vector<int> restored(values.size());
        std::partial_sum(differences.begin(), differences.end(), restored.begin());
        assert(restored == values);
    }
    passed.push_back("ordered-numeric-fold-and-differences");
    {
        std::vector<int> a{1,1,2}, b{1,3}, out;
        std::set_union(a.begin(),a.end(),b.begin(),b.end(),std::back_inserter(out));
        assert((out==std::vector<int>{1,1,2,3}));
        out.clear();
        std::set_symmetric_difference(a.begin(),a.end(),b.begin(),b.end(),std::back_inserter(out));
        assert((out==std::vector<int>{1,2,3}));
    }
    passed.push_back("ordered-multiset-multiplicities");
    {
        std::vector<int> v{1,2,3,4,5};
        auto returned=std::rotate(v.begin(),v.begin()+2,v.end());
        assert((v==std::vector<int>{3,4,5,1,2}) && returned==v.begin()+3);
        v={1,3,2};assert(std::next_permutation(v.begin(),v.end()));
        assert((v==std::vector<int>{2,1,3}));
        v={3,2,1};assert(!std::next_permutation(v.begin(),v.end()));
        assert((v==std::vector<int>{1,2,3}));
        assert(!std::prev_permutation(v.begin(),v.end()));
        assert((v==std::vector<int>{3,2,1}));
    }
    passed.push_back("rotate-and-permutation-boundaries");
    {
        auto first=[](int x){return 3-x;};
        auto second=[](int x){return x-3;};
        auto composed=[](int x){return 3*(x+2);};
        assert(first(10)==-7 && second(10)==7 && composed(4)==18);
        std::vector<int> v{1,2,3};
        std::for_each(v.begin(),v.end(),[](int x){return x+100;});
        assert((v==std::vector<int>{1,2,3})); // Ordinary return values are ignored.
    }
    passed.push_back("callable-direction-and-ignored-return");
    std::cout << "{\"status\":\"ok\",\"standard\":\"C++17\",\"scope\":\"host library experiments, not historical SGI verification\",\"passed\":[";
    for (std::size_t i = 0; i < passed.size(); ++i) {
        if (i) std::cout << ',';
        std::cout << '"' << passed[i] << '"';
    }
    std::cout << "]}\n";
}
