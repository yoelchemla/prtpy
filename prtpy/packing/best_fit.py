"""
Pack the numbers using the best-fit bin-packing algorithms.

Programmer: Erel Segal-Halevi.
Date: 2022
"""

from typing import Callable, List, Any
from prtpy import outputtypes as out, Bins, printbins
from prtpy.binners import BinsArray


def online(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
)->BinsArray:
    """
        Pack the given items into bins using the online best-fit algorithm.
        The online algorithm handles the items in the order they are given.

        >>> from prtpy.bins import BinsKeepingContents, BinsKeepingSums
        >>> printbins(online(BinsKeepingContents(0), binsize=9, items=[4,7,2,1,5,8,4]))
        Bin #0: [4, 1, 4], sum=9.0
        Bin #1: [7, 2], sum=9.0
        Bin #2: [5], sum=5.0
        Bin #3: [8], sum=8.0
        >>> printbins(online(BinsKeepingContents(0), binsize=18, items=[1,2,10,14,4,10,5]))
        Bin #0: [1, 2, 10, 5], sum=18.0
        Bin #1: [14, 4], sum=18.0
        Bin #2: [10], sum=10.0
        >>> list(online(BinsKeepingSums(0), binsize=18, items=[1,2,10,14,4,10,5]))
        [18.0, 18.0, 10.0]
        """
    binner = bins.get_binner()
    bins = binner.new_bins(1)
    numbins = 1
    for item in items:
        value = valueof(item)
        if value > binsize:
            raise ValueError(f"Item {item} has size {value} which is larger than the bin size {binsize}.")
        ibin = 0
        best_bin = (-1, -1)
        while ibin < numbins:
            new_sum = binner.sums(bins)[ibin] + value
            if new_sum <= binsize and new_sum > best_bin[1]:
                best_bin = (ibin, new_sum)
            ibin += 1

        if best_bin[0] > -1:
            binner.add_item_to_bin(bins, item, best_bin[0])
        else:  # if not added to any bin
            bins = binner.add_empty_bins(bins, 1)
            numbins += 1
            binner.add_item_to_bin(bins, item, ibin)
    return bins


def decreasing(
    bins: Bins,
    binsize: float,
    items: List[any],
    valueof: Callable[[Any], float] = lambda x: x,
)->BinsArray:

    return online(
        bins,
        binsize,
        sorted(items, key=valueof, reverse=True),
        valueof,
    )


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
