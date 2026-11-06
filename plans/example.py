# Example plan: one lesson from sources/example.txt. Copy this shape for your own source.
URL = "https://example.com/python-lists"
LESSONS = [
  dict(name="Python lists: indexing, slicing and sorting",
       section="Python lists",
       points=[
         "Why lists: one name for many values kept in order. nums = [3, 1, 2]. Indexing starts at 0, so nums[0] is 3; nums[-1] is 2 because negative indexes count from the end. Common mistake: nums[3] on a 3-item list raises IndexError.",
         "A slice copies a range and excludes the end index: nums[0:2] is [3, 1], not [3, 1, 2]. Because it is a copy, changing the slice leaves nums alone.",
         "Lists are mutable: nums.append(5) changes nums itself and returns None. Common mistake: nums = nums.append(5) leaves nums as None.",
         "sorted(nums) returns a new sorted list and leaves nums alone; nums.sort() sorts nums in place and returns None. Use sorted when you still need the original order.",
       ],
       checks=[
         ("nums[0] is 3", r"nums\[0\]"),
         ("negative index", r"nums\[-1\]"),
         ("slice excludes end", r"nums\[0:2\]"),
         ("append returns None", r"append\(5\)"),
         ("sorted vs sort", r"sorted\(nums\)"),
       ]),
]
