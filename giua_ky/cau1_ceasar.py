# User function Template for python3

class Solution:
    def __init__(self):
        self.max = None

    def floor(self, root, x):

        if root.data > x:

            return self.max

        elif self.max != None:

            if self.max < root.data:

                self.max = root.data
            else:
                return self.floor(root.right, x)

        else:

            self.max = root.data

            return max(self.floor(root.left, x), self.floor(root.right, x))


# {
# Driver Code Starts
# Initial Template for Python 3

class Node:
    def __init__(self, val):
        self.right = None
        self.data = val
        self.left = None


def insert(tree, val):
    if (tree == None):
        return Node(val)
    if (val < tree.data):
        tree.left = insert(tree.left, val)
    elif (val > tree.data):
        tree.right = insert(tree.right, val)
    return tree


if __name__ == "__main__":
    t = int(input())
    for _ in range(0, t):
        n = int(input())
        arr = list(map(int, input().split()))
        root = None
        for k in arr:
            root = insert(root, k)
        s = int(input())
        obj = Solution()
        print(obj.floor(root, s))
# } Driver Code Ends