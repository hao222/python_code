# -*- coding:utf-8 -*-
# @author wuhao
# @date 2022/2/18
import queue
# 二叉树 遍历 求深度
class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.right = right
        self.left = left


def tree_depth(tree):
    if not tree:
        return 0
    else:
        return max(tree_depth(tree.left), tree_depth(tree.right)) + 1


def tree_width(tree):
    """
    加上lis 可以得到二叉树的层次遍历结果，用队列的性质
    get()其实相当于python里面的pop()，只不过pop()可以出任意位置的数，而get()只能是最先进的那个数
    :param tree:
    :return:
    """
    if tree == None:
        return 0
    else:
        q = queue.Queue()
        lis = []
        n = 1
        q.put(tree)
        winth = 0
        max_winth = 0
        while not q.empty():
            for i in range(n):
                temp = q.get()
                lis.append(temp.data)
                if temp.left:
                    q.put(temp.left)
                    winth += 1
                if temp.right:
                    q.put(temp.right)
                    winth += 1
            n = winth
            if max_winth < winth:
                max_winth = winth
            winth = 0
        return max_winth, lis


if __name__ == "__main__":
    tree = Node('D', Node('B', Node('A'), Node('C')), Node('E', right=Node('G', Node('F'))))
    print(tree_depth(tree))
    print(tree_width(tree))
