#!/usr/bin/env python
"""
Example of using the library interactively on the terminal.

For this example we're using a duplicate finding algorithm from leetcode:

    https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/

"""

import sys

from prettyalgo.pprint import PrettyListPrinter


def main():
    # our input.
    nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]

    # here we use the context manager interface
    with PrettyListPrinter(
        padding=4,
        v_padding=1,
        caption="Remove Duplicates From Sorted Array 2",
        interactive=True,
    ) as pprint:
        # inside is the actual algorithm, and we are free to use pprint.pp calls inside as needed
        i, j = 1, 1
        count = 1
        while i < len(nums):
            # ptrs is an optional dictionary of pointers (indexes) into the list, for display.
            # context is an optional dictionary of auxilliary variables used, for display.
            pprint.pp(nums, ptrs=dict(i=i, j=j), context=dict(count=count))
            if nums[i] == nums[i - 1]:
                count += 1
                if count > 2:
                    i += 1
                    continue
            else:
                count = 1

            nums[j] = nums[i]
            j += 1
            i += 1

        pprint.pp(nums, ptrs=dict(i=i, j=j), context=dict(count=count))


if __name__ == "__main__":
    sys.exit(main())
