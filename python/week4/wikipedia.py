import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}


        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#

        # value から key を抽出
        def get_keys(dictionary, value):
            return [k for k, v in dictionary.items() if v == value]

        # 幅優先探索をして start から goal への経路があるか確認
        def bf_search():
            # 探索待ちのノードを格納するキュー
            todo = collections.deque() 

            start_key = get_keys(self.titles, start)[0]
            goal_key = get_keys(self.titles, goal)[0]

            number_of_steps[start_key] = 0
            test_dict = {}
            start_key.append(test_dict[0])
            todo.append(start_key)

            while todo: # キューが空になるまで探索を繰り返す
                node = todo.popleft() # 先頭を dequeue する
                if node == goal_key: # goal を見つけた場合
                    return get_path(node, number_of_steps[node]) # 最短経路を求める
                for child in self.links[node]: # 子ノードをたどる
                    if number_of_steps[child] == -1: # 未探索の場合
                        number_of_steps[child] = number_of_steps[node] + 1 # step をひとつ進めて辞書に追加
                        todo.append(child) # キューにノードを追加
            return None

        # 最短経路のリストを返す
        # goal を始点として、 bfs で探索した逆順にノードをたどる
        def get_path(node, result):
            path = [goal]
            result -= 1 # goal のひとつ前に戻る

            while result >= 0:
                for key in get_keys(number_of_steps, result):
                    if node in self.links[key]:
                        path.append(self.titles[key])
                        node = key
                        break
                result -= 1

            return path[::-1]

        number_of_steps = {key: -1 for key in self.titles.keys()}
    
        path = bf_search()
        print(" -> ".join(path) if path else "Not Found :(")
    

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        
        # ページランクを計算して、重要度が高いページ Top10 を求める

        pass


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "小野妹子")

    # wikipedia.find_shortest_path("A", "B")
    # wikipedia.find_shortest_path("F", "E")

    wikipedia.find_most_popular_pages()
