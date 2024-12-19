from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, auto
from itertools import repeat
from math import isfinite, isinf, isnan
from operator import sub
from typing import TYPE_CHECKING, Any, ClassVar, Literal

from hypothesis import given
from hypothesis.strategies import (
    DataObject,
    binary,
    data,
    datetimes,
    dictionaries,
    floats,
    frozensets,
    integers,
    lists,
    none,
    permutations,
    sampled_from,
    sets,
    text,
)
from pytest import mark, param, raises
from typing_extensions import override

from tests.test_operator import make_objects
from utilities.hypothesis import sets_fixed_length, text_ascii, zoned_datetimes
from utilities.iterables import (
    CheckBijectionError,
    CheckDuplicatesError,
    CheckIterablesEqualError,
    CheckLengthError,
    CheckLengthsEqualError,
    CheckMappingsEqualError,
    CheckSetsEqualError,
    CheckSubMappingError,
    CheckSubSetError,
    CheckSuperMappingError,
    CheckSuperSetError,
    Collection,
    EnsureIterableError,
    EnsureIterableNotStrError,
    MaybeIterable,
    OneEmptyError,
    OneNonUniqueError,
    OneStrError,
    ResolveIncludeAndExcludeError,
    SortIterableError,
    always_iterable,
    apply_to_tuple,
    apply_to_varargs,
    check_bijection,
    check_duplicates,
    check_iterables_equal,
    check_length,
    check_lengths_equal,
    check_mappings_equal,
    check_sets_equal,
    check_submapping,
    check_subset,
    check_supermapping,
    check_superset,
    chunked,
    ensure_hashables,
    ensure_iterable,
    ensure_iterable_not_str,
    expanding_window,
    filter_include_and_exclude,
    groupby_lists,
    hashable_to_iterable,
    is_iterable,
    is_iterable_not_enum,
    is_iterable_not_str,
    one,
    one_str,
    pairwise_tail,
    product_dicts,
    resolve_include_and_exclude,
    sort_iterable,
    take,
    transpose,
)
from utilities.sentinel import sentinel

if TYPE_CHECKING:
    import datetime as dt
    from collections.abc import Iterable, Iterator, Sequence


class TestAlwaysIterable:
    @given(x=binary())
    def test_bytes(self, *, x: bytes) -> None:
        assert list(always_iterable(x)) == [x]

    @given(x=integers())
    def test_integer(self, *, x: int) -> None:
        assert list(always_iterable(x)) == [x]

    @given(x=lists(binary()))
    def test_list_of_bytes(self, *, x: list[bytes]) -> None:
        assert list(always_iterable(x)) == x

    @given(x=text())
    def test_string(self, *, x: str) -> None:
        assert list(always_iterable(x)) == [x]

    @given(x=lists(text()))
    def test_list_of_strings(self, *, x: list[str]) -> None:
        assert list(always_iterable(x)) == x

    @given(x=dictionaries(text(), integers()))
    def test_dict(self, *, x: dict[str, int]) -> None:
        assert list(always_iterable(x)) == list(x)

    @given(x=lists(integers()))
    def test_lists(self, *, x: list[int]) -> None:
        assert list(always_iterable(x)) == x

    def test_generator(self) -> None:
        def yield_ints() -> Iterator[int]:
            yield 0
            yield 1

        assert list(always_iterable(yield_ints())) == [0, 1]


class TestApplyToTuple:
    @given(x=integers(), y=integers())
    def test_main(self, *, x: int, y: int) -> None:
        result = apply_to_tuple(sub, (x, y))
        expected = x - y
        assert result == expected


class TestApplyToVarArgs:
    @given(x=integers(), y=integers())
    def test_main(self, *, x: int, y: int) -> None:
        result = apply_to_varargs(sub, x, y)
        expected = x - y
        assert result == expected


class TestCheckBijection:
    @given(data=data(), n=integers(0, 10))
    def test_main(self, *, data: DataObject, n: int) -> None:
        keys = data.draw(sets_fixed_length(integers(0, 100), n))
        values = data.draw(sets_fixed_length(integers(0, 100), n))
        mapping = dict(zip(keys, values, strict=True))
        check_bijection(mapping)

    def test_error(self) -> None:
        with raises(
            CheckBijectionError,
            match="Mapping .* must be a bijection; got duplicates {None: 2}",
        ):
            check_bijection({True: None, False: None})


class TestCheckDuplicates:
    @given(x=sets(integers()))
    def test_main(self, *, x: set[int]) -> None:
        check_duplicates(x)

    def test_error(self) -> None:
        with raises(
            CheckDuplicatesError,
            match="Iterable .* must not contain duplicates; got {None: 2}",
        ):
            check_duplicates([None, None])


class TestCheckIterablesEqual:
    def test_pass(self) -> None:
        check_iterables_equal([], [])

    def test_error_differing_items_and_left_longer(self) -> None:
        with raises(
            CheckIterablesEqualError,
            match="Iterables .* and .* must be equal; differing items were .* and left was longer",
        ):
            check_iterables_equal([1, 2, 3], [9])

    def test_error_differing_items_and_right_longer(self) -> None:
        with raises(
            CheckIterablesEqualError,
            match="Iterables .* and .* must be equal; differing items were .* and right was longer",
        ):
            check_iterables_equal([9], [1, 2, 3])

    def test_error_differing_items_and_same_length(self) -> None:
        with raises(
            CheckIterablesEqualError,
            match="Iterables .* and .* must be equal; differing items were .*",
        ):
            check_iterables_equal([1, 2, 3], [1, 2, 9])

    def test_error_no_differing_items_just_left_longer(self) -> None:
        with raises(
            CheckIterablesEqualError,
            match="Iterables .* and .* must be equal; left was longer",
        ):
            check_iterables_equal([1, 2, 3], [1])

    def test_error_no_differing_items_just_right_longer(self) -> None:
        with raises(
            CheckIterablesEqualError,
            match="Iterables .* and .* must be equal; right was longer",
        ):
            check_iterables_equal([1], [1, 2, 3])


class TestCheckLength:
    def test_equal_pass(self) -> None:
        check_length([], equal=0)

    def test_equal_fail(self) -> None:
        with raises(CheckLengthError, match=r"Object .* must have length .*; got .*"):
            check_length([], equal=1)

    @mark.parametrize("equal_or_approx", [param(10), param((11, 0.1))])
    def test_equal_or_approx_pass(
        self, *, equal_or_approx: int | tuple[int, float]
    ) -> None:
        check_length(range(10), equal_or_approx=equal_or_approx)

    @mark.parametrize(
        ("equal_or_approx", "match"),
        [
            param(10, "Object .* must have length .*; got .*"),
            param(
                (11, 0.1),
                r"Object .* must have approximate length .* \(error .*\); got .*",
            ),
        ],
    )
    def test_equal_or_approx_fail(
        self, *, equal_or_approx: int | tuple[int, float], match: str
    ) -> None:
        with raises(CheckLengthError, match=match):
            check_length([], equal_or_approx=equal_or_approx)

    def test_min_pass(self) -> None:
        check_length([], min=0)

    def test_min_error(self) -> None:
        with raises(
            CheckLengthError, match="Object .* must have minimum length .*; got .*"
        ):
            check_length([], min=1)

    def test_max_pass(self) -> None:
        check_length([], max=0)

    def test_max_error(self) -> None:
        with raises(
            CheckLengthError, match="Object .* must have maximum length .*; got .*"
        ):
            check_length([1], max=0)


class TestCheckLengthsEqual:
    def test_pass(self) -> None:
        check_lengths_equal([], [])

    def test_error(self) -> None:
        with raises(
            CheckLengthsEqualError,
            match="Sized objects .* and .* must have the same length; got .* and .*",
        ):
            check_lengths_equal([], [1, 2, 3])


class TestCheckMappingsEqual:
    def test_pass(self) -> None:
        check_mappings_equal({}, {})

    def test_error_extra_and_missing_and_differing_values(self) -> None:
        with raises(
            CheckMappingsEqualError,
            match="Mappings .* and .* must be equal; left had extra keys .*, right had extra keys .* and differing values were .*",
        ):
            check_mappings_equal({"a": 1, "b": 2, "c": 3}, {"b": 2, "c": 9, "d": 4})

    def test_error_extra_and_missing(self) -> None:
        with raises(
            CheckMappingsEqualError,
            match="Mappings .* and .* must be equal; left had extra keys .* and right had extra keys .*",
        ):
            check_mappings_equal({"a": 1, "b": 2, "c": 3}, {"b": 2, "c": 3, "d": 4})

    def test_error_extra_and_differing_values(self) -> None:
        with raises(
            CheckMappingsEqualError,
            match="Mappings .* and .* must be equal; left had extra keys .* and differing values were .*",
        ):
            check_mappings_equal({"a": 1, "b": 2, "c": 3}, {"a": 9})

    def test_error_missing_and_differing_values(self) -> None:
        with raises(
            CheckMappingsEqualError,
            match="Mappings .* and .* must be equal; right had extra keys .* and differing values were .*",
        ):
            check_mappings_equal({"a": 1}, {"a": 9, "b": 2, "c": 3})

    def test_error_extra_only(self) -> None:
        with raises(
            CheckMappingsEqualError,
            match="Mappings .* and .* must be equal; left had extra keys .*",
        ):
            check_mappings_equal({"a": 1, "b": 2, "c": 3}, {"a": 1})

    def test_error_missing_only(self) -> None:
        with raises(
            CheckMappingsEqualError,
            match="Mappings .* and .* must be equal; right had extra keys .*",
        ):
            check_mappings_equal({"a": 1}, {"a": 1, "b": 2, "c": 3})

    def test_error_differing_values_only(self) -> None:
        with raises(
            CheckMappingsEqualError,
            match="Mappings .* and .* must be equal; differing values were .*",
        ):
            check_mappings_equal({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 9})


class TestCheckSetsEqual:
    @mark.parametrize(
        ("left", "right"), [param(set(), set()), param(iter([]), iter([]))]
    )
    def test_pass(self, *, left: Iterable[Any], right: Iterable[Any]) -> None:
        check_sets_equal(left, right)

    def test_error_extra_and_missing(self) -> None:
        with raises(
            CheckSetsEqualError,
            match="Sets .* and .* must be equal; left had extra items .* and right had extra items .*",
        ):
            check_sets_equal({1, 2, 3}, {2, 3, 4})

    def test_error_extra(self) -> None:
        with raises(
            CheckSetsEqualError,
            match="Sets .* and .* must be equal; left had extra items .*",
        ):
            check_sets_equal({1, 2, 3}, set())

    def test_error_missing(self) -> None:
        with raises(
            CheckSetsEqualError,
            match="Sets .* and .* must be equal; right had extra items .*",
        ):
            check_sets_equal(set(), {1, 2, 3})


class TestCheckSubMapping:
    def test_pass(self) -> None:
        check_submapping({}, {})

    def test_error_extra_and_differing_values(self) -> None:
        with raises(
            CheckSubMappingError,
            match="Mapping .* must be a submapping of .*; left had extra keys .* and differing values were .*",
        ):
            check_submapping({"a": 1, "b": 2, "c": 3}, {"a": 9})

    def test_error_extra_only(self) -> None:
        with raises(
            CheckSubMappingError,
            match="Mapping .* must be a submapping of .*; left had extra keys .*",
        ):
            check_submapping({"a": 1, "b": 2, "c": 3}, {"a": 1})

    def test_error_differing_values_only(self) -> None:
        with raises(
            CheckSubMappingError,
            match="Mapping .* must be a submapping of .*; differing values were .*",
        ):
            check_submapping({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 9})


class TestCheckSubSet:
    @mark.parametrize(
        ("left", "right"), [param(set(), set()), param(iter([]), iter([]))]
    )
    def test_pass(self, *, left: Iterable[Any], right: Iterable[Any]) -> None:
        check_subset(left, right)

    def test_error(self) -> None:
        with raises(
            CheckSubSetError,
            match="Set .* must be a subset of .*; left had extra items .*",
        ):
            check_subset({1, 2, 3}, {1})


class TestCheckSuperMapping:
    def test_pass(self) -> None:
        check_supermapping({}, {})

    def test_error_missing_and_differing_values(self) -> None:
        with raises(
            CheckSuperMappingError,
            match="Mapping .* must be a supermapping of .*; right had extra keys .* and differing values were .*",
        ):
            check_supermapping({"a": 1}, {"a": 9, "b": 2, "c": 3})

    def test_error_extra_only(self) -> None:
        with raises(
            CheckSuperMappingError,
            match="Mapping .* must be a supermapping of .*; right had extra keys .*",
        ):
            check_supermapping({"a": 1}, {"a": 1, "b": 2, "c": 3})

    def test_error_differing_values_only(self) -> None:
        with raises(
            CheckSuperMappingError,
            match="Mapping .* must be a supermapping of .*; differing values were .*",
        ):
            check_supermapping({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 9})


class TestCheckSuperSet:
    @mark.parametrize(
        ("left", "right"), [param(set(), set()), param(iter([]), iter([]))]
    )
    def test_pass(self, *, left: Iterable[Any], right: Iterable[Any]) -> None:
        check_superset(left, right)

    def test_error(self) -> None:
        with raises(
            CheckSuperSetError,
            match=r"Set .* must be a superset of .*; right had extra items .*\.",
        ):
            check_superset({1}, {1, 2, 3})


class TestChunked:
    @mark.parametrize(
        ("iterable", "expected"),
        [
            param("ABCDEF", [["A", "B", "C"], ["D", "E", "F"]]),
            param("ABCDE", [["A", "B", "C"], ["D", "E"]]),
        ],
    )
    def test_main(
        self, *, iterable: Iterable[str], expected: Sequence[Sequence[str]]
    ) -> None:
        result = list(chunked(iterable, 3))
        assert result == expected

    def test_odd(self) -> None:
        result = list(chunked("ABCDE", 3))
        expected = [["A", "B", "C"], ["D", "E"]]
        assert result == expected


@dataclass(unsafe_hash=True, slots=True)
class _Item:
    n: int


class TestCollection:
    def test_and_singleton(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection & _Item(1)
        assert isinstance(result, Collection)
        expected = Collection(_Item(1))
        assert result == expected

    def test_and_collection(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection & Collection(_Item(1))
        assert isinstance(result, Collection)
        expected = Collection(_Item(1))
        assert result == expected

    def test_and_iterable(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection & [_Item(1)]
        assert isinstance(result, Collection)
        expected = Collection(_Item(1))
        assert result == expected

    def test_filter(self) -> None:
        collection = Collection(map(_Item, range(4)))
        result = collection.filter(lambda item: item.n % 2 == 0)
        assert isinstance(result, Collection)
        expected = Collection(_Item(0), _Item(2))
        assert result == expected

    def test_hash(self) -> None:
        collection = Collection(map(_Item, range(3)))
        _ = hash(collection)

    def test_init(self) -> None:
        class SubCollection(Collection[_Item]):
            @override
            def __init__(self, *item_or_items: MaybeIterable[_Item]) -> None:
                super().__init__(*item_or_items)
                if any(item.n >= 1 for item in self):
                    msg = "n >= 1 is not permitted"
                    raise ValueError(msg)

        with raises(ValueError, match="n >= 1 is not permitted"):
            _ = SubCollection(map(_Item, range(3)))

    def test_map_return_same_type(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection.map(lambda item: replace(item, n=item.n + 1))
        assert isinstance(result, Collection)
        expected = Collection(map(_Item, range(1, 4)))
        assert result == expected

    def test_map_return_different_type(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection.map(lambda item: item.n)
        assert isinstance(result, Collection)
        expected = Collection(range(3))
        assert result == expected

    def test_new_one_singleton(self) -> None:
        collection = Collection(_Item(1))
        assert isinstance(collection, Collection)
        assert len(collection) == 1
        assert one(collection) == _Item(1)

    def test_new_one_iterable(self) -> None:
        collection = Collection(map(_Item, range(3)))
        assert isinstance(collection, Collection)
        assert len(collection) == 3

    def test_new_many_singletons(self) -> None:
        collection = Collection(_Item(1), _Item(2), _Item(3))
        assert isinstance(collection, Collection)
        assert len(collection) == 3

    def test_new_many_iterables(self) -> None:
        collection = Collection(map(_Item, range(3)), map(_Item, range(3)))
        assert isinstance(collection, Collection)
        assert len(collection) == 3

    def test_new_check_items(self) -> None:
        class SubCollection(Collection[_Item]):
            @classmethod
            @override
            def check_items(cls, items: Iterable[_Item]) -> None:
                if any(item.n >= 1 for item in items):
                    msg = "n >= 1 is not permitted"
                    raise ValueError(msg)

        with raises(ValueError, match="n >= 1 is not permitted"):
            _ = SubCollection(map(_Item, range(3)))

    def test_or_singleton(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection | _Item(3)
        assert isinstance(result, Collection)
        expected = Collection(map(_Item, range(4)))
        assert result == expected

    def test_or_collection(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection | Collection(map(_Item, range(1, 4)))
        assert isinstance(result, Collection)
        expected = Collection(map(_Item, range(4)))
        assert result == expected

    def test_or_iterable(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection | map(_Item, range(1, 4))
        assert isinstance(result, Collection)
        expected = Collection(map(_Item, range(4)))
        assert result == expected

    def test_partition(self) -> None:
        collection = Collection(map(_Item, range(4)))
        result_false, result_true = collection.partition(lambda item: item.n % 2 == 0)
        assert isinstance(result_false, Collection)
        expected_false = Collection(_Item(1), _Item(3))
        assert result_false == expected_false
        assert isinstance(result_true, Collection)
        expected_true = Collection(_Item(0), _Item(2))
        assert result_true == expected_true

    def test_repr(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = repr(collection)
        expected = "Collection({_Item(n=0), _Item(n=1), _Item(n=2)})"
        assert result == expected

    def test_str(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = str(collection)
        expected = "Collection({_Item(n=0), _Item(n=1), _Item(n=2)})"
        assert result == expected

    def test_sub_single_item(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection - _Item(1)
        assert isinstance(result, Collection)
        expected = Collection(_Item(0), _Item(2))
        assert result == expected

    def test_sub_collection(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection - Collection(_Item(1))
        assert isinstance(result, Collection)
        expected = Collection(_Item(0), _Item(2))
        assert result == expected

    def test_sub_iterable(self) -> None:
        collection = Collection(map(_Item, range(3)))
        result = collection - [_Item(1)]
        assert isinstance(result, Collection)
        expected = Collection(_Item(0), _Item(2))
        assert result == expected


class TestEnsureHashables:
    def test_main(self) -> None:
        assert ensure_hashables(1, 2, a=3, b=4) == ([1, 2], {"a": 3, "b": 4})


class TestEnsureIterable:
    @mark.parametrize("obj", [param([]), param(()), param("")])
    def test_main(self, *, obj: Any) -> None:
        _ = ensure_iterable(obj)

    def test_error(self) -> None:
        with raises(EnsureIterableError, match="Object .* must be iterable"):
            _ = ensure_iterable(None)


class TestEnsureIterableNotStr:
    @mark.parametrize("obj", [param([]), param(())])
    def test_main(self, *, obj: Any) -> None:
        _ = ensure_iterable_not_str(obj)

    @mark.parametrize("obj", [param(None), param("")])
    def test_error(self, *, obj: Any) -> None:
        with raises(
            EnsureIterableNotStrError,
            match="Object .* must be iterable, but not a string",
        ):
            _ = ensure_iterable_not_str(obj)


class TestExpandingWindow:
    @mark.parametrize(
        ("iterable", "expected"),
        [
            param(
                [1, 2, 3, 4, 5], [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
            ),
            param([], []),
        ],
    )
    def test_main(self, *, iterable: Iterable[int], expected: list[list[int]]) -> None:
        result = list(expanding_window(iterable))
        assert result == expected


class TestHashableToIterable:
    def test_none(self) -> None:
        result = hashable_to_iterable(None)
        expected = None
        assert result is expected

    @given(x=lists(integers()))
    def test_integers(self, *, x: int) -> None:
        result = hashable_to_iterable(x)
        expected = (x,)
        assert result == expected


class TestFilterIncludeAndExclude:
    def test_none(self) -> None:
        rng = list(range(5))
        result = list(filter_include_and_exclude(rng))
        assert result == rng

    def test_include_singleton(self) -> None:
        result = list(filter_include_and_exclude(range(5), include=0))
        expected = [0]
        assert result == expected

    def test_include_iterable(self) -> None:
        result = list(filter_include_and_exclude(range(5), include=[0, 1, 2]))
        expected = [0, 1, 2]
        assert result == expected

    def test_exclude_singleton(self) -> None:
        result = list(filter_include_and_exclude(range(5), exclude=0))
        expected = [1, 2, 3, 4]
        assert result == expected

    def test_exclude_iterable(self) -> None:
        result = list(filter_include_and_exclude(range(5), exclude=[0, 1, 2]))
        expected = [3, 4]
        assert result == expected

    def test_both(self) -> None:
        result = list(
            filter_include_and_exclude(range(5), include=[0, 1], exclude=[3, 4])
        )
        expected = [0, 1]
        assert result == expected

    def test_include_key(self) -> None:
        @dataclass(kw_only=True, slots=True)
        class Example:
            n: int

        result = list(
            filter_include_and_exclude(
                [Example(n=n) for n in range(5)], include=[0, 1, 2], key=lambda x: x.n
            )
        )
        expected = [Example(n=n) for n in [0, 1, 2]]
        assert result == expected

    def test_exclude_key(self) -> None:
        @dataclass(kw_only=True, slots=True)
        class Example:
            n: int

        result = list(
            filter_include_and_exclude(
                [Example(n=n) for n in range(5)], exclude=[0, 1, 2], key=lambda x: x.n
            )
        )
        expected = [Example(n=n) for n in [3, 4]]
        assert result == expected


class TestGroupbyLists:
    iterable: ClassVar[str] = "AAAABBBCCDAABB"

    def test_main(self) -> None:
        result = list(groupby_lists(self.iterable))
        expected = [
            ("A", list(repeat("A", times=4))),
            ("B", list(repeat("B", times=3))),
            ("C", list(repeat("C", times=2))),
            ("D", list(repeat("D", times=1))),
            ("A", list(repeat("A", times=2))),
            ("B", list(repeat("B", times=2))),
        ]
        assert result == expected

    def test_key(self) -> None:
        result = list(groupby_lists(self.iterable, key=ord))
        expected = [
            (65, list(repeat("A", times=4))),
            (66, list(repeat("B", times=3))),
            (67, list(repeat("C", times=2))),
            (68, list(repeat("D", times=1))),
            (65, list(repeat("A", times=2))),
            (66, list(repeat("B", times=2))),
        ]
        assert result == expected


class TestIsIterable:
    @mark.parametrize(
        ("obj", "expected"),
        [param(None, False), param([], True), param((), True), param("", True)],
    )
    def test_main(self, *, obj: Any, expected: bool) -> None:
        assert is_iterable(obj) is expected


class TestIsIterableNotEnum:
    def test_single(self) -> None:
        class Truth(Enum):
            true = auto()
            false = auto()

        assert not is_iterable_not_enum(Truth)

    def test_union(self) -> None:
        class Truth1(Enum):
            true = auto()
            false = auto()

        class Truth2(Enum):
            true = auto()
            false = auto()

        assert is_iterable_not_enum((Truth1, Truth2))

    @mark.parametrize(
        ("obj", "expected"),
        [param(None, False), param([], True), param((), True), param("", True)],
    )
    def test_others(self, *, obj: Any, expected: bool) -> None:
        assert is_iterable_not_enum(obj) is expected


class TestIsIterableNotStr:
    @mark.parametrize(
        ("obj", "expected"),
        [param(None, False), param([], True), param((), True), param("", False)],
    )
    def test_main(self, *, obj: Any, expected: bool) -> None:
        assert is_iterable_not_str(obj) is expected


class TestOne:
    def test_main(self) -> None:
        assert one([None]) is None

    def test_error_empty(self) -> None:
        with raises(OneEmptyError, match="Iterable .* must not be empty"):
            _ = one([])

    def test_error_non_unique(self) -> None:
        with raises(
            OneNonUniqueError,
            match="Iterable .* must contain exactly one item; got .*, .* and perhaps more",
        ):
            _ = one([1, 2])


class TestOneStr:
    @given(text=sampled_from(["a", "b", "c"]))
    def test_case_sensitive(self, *, text: str) -> None:
        assert one_str(["a", "b", "c"], text) == text

    @given(text=sampled_from(["a", "b", "c"]), case=sampled_from(["lower", "upper"]))
    def test_case_insensitive(
        self, *, text: str, case: Literal["lower", "upper"]
    ) -> None:
        match case:
            case "lower":
                text_use = text.lower()
            case "upper":
                text_use = text.upper()
        assert one_str(["a", "b", "c"], text_use, case_sensitive=False) == text

    def test_error_duplicates(self) -> None:
        with raises(
            OneStrError, match=r"Iterable .* must not contain duplicates; got {'a': 2}"
        ):
            _ = one_str(["a", "a"], "a")

    def test_error_case_sensitive_empty_error(self) -> None:
        with raises(OneStrError, match=r"Iterable .* does not contain 'd'"):
            _ = one_str(["a", "b", "c"], "d")

    def test_error_bijection_error(self) -> None:
        with raises(
            OneStrError,
            match=r"Iterable .* must not contain duplicates \(case insensitive\); got .*",
        ):
            _ = one_str(["a", "A"], "a", case_sensitive=False)

    def test_error_case_insensitive_empty_error(self) -> None:
        with raises(
            OneStrError, match=r"Iterable .* does not contain 'd' \(case insensitive\)"
        ):
            _ = one_str(["a", "b", "c"], "d", case_sensitive=False)


class TestPairwiseTail:
    def test_main(self) -> None:
        iterable = range(5)
        result = list(pairwise_tail(iterable))
        expected = [(0, 1), (1, 2), (2, 3), (3, 4), (4, sentinel)]
        assert result == expected


class TestProductDicts:
    def test_main(self) -> None:
        mapping = {"x": [1, 2], "y": [7, 8, 9]}
        result = list(product_dicts(mapping))
        expected = [
            {"x": 1, "y": 7},
            {"x": 1, "y": 8},
            {"x": 1, "y": 9},
            {"x": 2, "y": 7},
            {"x": 2, "y": 8},
            {"x": 2, "y": 9},
        ]
        assert result == expected


class TestResolveIncludeAndExclude:
    def test_none(self) -> None:
        include, exclude = resolve_include_and_exclude()
        assert include is None
        assert exclude is None

    def test_include_singleton(self) -> None:
        include, exclude = resolve_include_and_exclude(include=1)
        assert include == {1}
        assert exclude is None

    def test_include_iterable(self) -> None:
        include, exclude = resolve_include_and_exclude(include=[1, 2, 3])
        assert include == {1, 2, 3}
        assert exclude is None

    def test_exclude_singleton(self) -> None:
        include, exclude = resolve_include_and_exclude(exclude=1)
        assert include is None
        assert exclude == {1}

    def test_exclude_iterable(self) -> None:
        include, exclude = resolve_include_and_exclude(exclude=[1, 2, 3])
        assert include is None
        assert exclude == {1, 2, 3}

    def test_both(self) -> None:
        include, exclude = resolve_include_and_exclude(
            include=[1, 2, 3], exclude=[4, 5, 6]
        )
        assert include == {1, 2, 3}
        assert exclude == {4, 5, 6}

    def test_error(self) -> None:
        with raises(
            ResolveIncludeAndExcludeError,
            match="Iterables .* and .* must not overlap; got .*",
        ):
            _ = resolve_include_and_exclude(include=[1, 2, 3], exclude=[3, 4, 5])


class TestSortIterables:
    @given(
        x=make_objects(floats_allow_nan=False), y=make_objects(floats_allow_nan=False)
    )
    def test_main(self, *, x: Any, y: Any) -> None:
        result1 = sort_iterable([x, y])
        result2 = sort_iterable([y, x])
        assert result1 == result2

    @given(x=datetimes() | zoned_datetimes(), y=datetimes() | zoned_datetimes())
    def test_datetimes(self, *, x: dt.datetime, y: dt.datetime) -> None:
        result1 = sort_iterable([x, y])
        result2 = sort_iterable([y, x])
        assert result1 == result2

    @given(x=floats(), y=floats())
    def test_floats(self, *, x: float, y: float) -> None:
        result1 = sort_iterable([x, y])
        result2 = sort_iterable([y, x])
        for i, j in zip(result1, result2, strict=True):
            assert isfinite(i) is isfinite(j)
            assert isinf(i) is isinf(j)
            assert isnan(i) is isnan(j)

    @given(x=text_ascii(), y=text_ascii())
    def test_strings(self, *, x: str, y: str) -> None:
        result1 = sort_iterable([x, y])
        result2 = sort_iterable([y, x])
        assert result1 == result2

    @given(x=frozensets(frozensets(integers())), y=frozensets(frozensets(integers())))
    def test_nested_frozensets(
        self, *, x: frozenset[frozenset[int]], y: frozenset[frozenset[int]]
    ) -> None:
        result1 = sort_iterable([x, y])
        result2 = sort_iterable([y, x])
        assert result1 == result2

    @given(data=data(), x=lists(none()))
    def test_nones(self, *, data: DataObject, x: list[None]) -> None:
        result1 = sort_iterable(x)
        result2 = sort_iterable(data.draw(permutations(result1)))
        assert result1 == result2

    def test_error(self) -> None:
        with raises(SortIterableError, match="Unable to sort .* and .*"):
            _ = sort_iterable([sentinel, sentinel])


class TestTake:
    def test_simple(self) -> None:
        result = take(5, range(10))
        expected = list(range(5))
        assert result == expected

    def test_null(self) -> None:
        result = take(0, range(10))
        expected = []
        assert result == expected

    def test_negative(self) -> None:
        with raises(
            ValueError,
            match=r"Indices for islice\(\) must be None or an integer: 0 <= x <= sys.maxsize\.",
        ):
            _ = take(-3, range(10))

    def test_too_much(self) -> None:
        result = take(10, range(5))
        expected = list(range(5))
        assert result == expected


class TestTranspose:
    @given(n=integers(1, 10))
    def test_singles(self, *, n: int) -> None:
        iterable = ((i,) for i in range(n))
        result = transpose(iterable)
        assert isinstance(result, tuple)
        (first,) = result
        assert isinstance(first, tuple)
        assert len(first) == n
        for i in first:
            assert isinstance(i, int)

    @given(n=integers(1, 10))
    def test_pairs(self, *, n: int) -> None:
        iterable = ((i, i) for i in range(n))
        result = transpose(iterable)
        assert isinstance(result, tuple)
        first, second = result
        for part in [first, second]:
            assert len(part) == n
            for i in part:
                assert isinstance(i, int)

    @given(n=integers(1, 10))
    def test_triples(self, *, n: int) -> None:
        iterable = ((i, i, i) for i in range(n))
        result = transpose(iterable)
        assert isinstance(result, tuple)
        first, second, third = result
        for part in [first, second, third]:
            assert len(part) == n
            for i in part:
                assert isinstance(i, int)

    @given(n=integers(1, 10))
    def test_quadruples(self, *, n: int) -> None:
        iterable = ((i, i, i, i) for i in range(n))
        result = transpose(iterable)
        assert isinstance(result, tuple)
        first, second, third, fourth = result
        for part in [first, second, third, fourth]:
            assert len(part) == n
            for i in part:
                assert isinstance(i, int)

    @given(n=integers(1, 10))
    def test_quintuples(self, *, n: int) -> None:
        iterable = ((i, i, i, i, i) for i in range(n))
        result = transpose(iterable)
        assert isinstance(result, tuple)
        first, second, third, fourth, fifth = result
        for part in [first, second, third, fourth, fifth]:
            assert len(part) == n
            for i in part:
                assert isinstance(i, int)
