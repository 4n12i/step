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

        """
        あるページから別のページへの最短経路を出力する
        """

        # value から key を抽出
        def get_keys(dictionary, value):
            return [k for k, v in dictionary.items() if v == value]

        # 幅優先探索をして start から goal への経路があるか確認
        def bf_search():
            todo = collections.deque() # 探索待ちのノードを格納するキュー
            distance = {key: -1 for key in self.titles.keys()} # 未探索: -1, 探索済み: startからの距離

            start_key = get_keys(self.titles, start)[0]
            goal_key = get_keys(self.titles, goal)[0]

            distance[start_key] = 0
            todo.append(start_key)

            while todo: # キューが空になるまで探索を繰り返す
                node = todo.popleft() # 先頭を dequeue する

                if node == goal_key: # goal を見つけた場合
                    return get_path(node, distance) # 最短経路を求める

                for child in self.links[node]: # 子ノードをたどる
                    if distance[child] == -1: # 未探索の場合
                        distance[child] = distance[node] + 1 # 距離を更新して辞書に追加
                        todo.append(child) # キューにノードを追加

            return None

        # goal を始点として bfs で探索した逆順にノードをたどり、最短経路を返す
        def get_path(node, distance):
            path = [goal]
            step = distance[node] - 1

            while step >= 0: # start に到着するまで繰り返す
                for key in get_keys(distance, step):  # 距離 step のノードを取得する
                    if node in self.links[key]: # node の親ノードである場合
                        path.append(self.titles[key]) # 経路に加える
                        node = key
                        break
                step -= 1

            return path[::-1]

        path = bf_search()
        print(" -> ".join(path) if path else "Not Found :(")
        
        return
    

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#

        """
        ページランクを計算して、重要度が高いページ Top10 を求める
        ループの前後において小数点以下2位で丸めたページランクが等しい場合、収束したとみなす
        """

        # 100% を全ノードに均等に分配する
        def give_to_all_nodes(received, a_pagerank):
            new = a_pagerank / len(received)
            for i in received.keys():
                received[i] += new


        # ページランクを更新
        def update_pagerank(pagerank, received):
            for i in pagerank.keys():
                pagerank[i], received[i] = received[i], 0


        # ページランクが収束しているか確認する
        def check_convergence(pagerank, received):
            for i in pagerank.keys():
                if not round(pagerank[i], 2) == round(received[i], 2):
                    return False
            return True


        # [DEBUG] タイトルとページランクを出力
        def print_status(pagerank):
            for value in pagerank.values:
                print(f"{value},", end="")
            print()


        # ページランクを計算する
        def get_pageranks():
            # 1. 全部のノードに初期値 1.0 を与える
            pagerank = {key:1 for key in self.titles.keys()} # 各ノードのページランク
            received = {key:0 for key in self.titles.keys()} # 受け取ったページランクの合計値

            # [DEBUG] カラムを出力
            # for title in self.titles.values():
            #     print(f"{title},", end="")
            # print()

            while True:
                # 2. 各ノードのページランクを隣接ノードに均等に振り分ける
                for key, value in pagerank.items():
                    next_nodes = self.links[key] # 隣接ノードのリスト

                    if len(next_nodes) == 0: # 隣接ノードがないとき
                        give_to_all_nodes(received, value) # 100% を全ノードに分配
                    else:
                        new = value * 0.85 / len(next_nodes) # 85% を隣接ノードに分配
                        for i in next_nodes:
                            received[i] += new
                        give_to_all_nodes(received, value * 0.15) # 15% を全ノードに分配

                print_status(pagerank)
                if check_convergence(pagerank, received): # 収束していたらループを終了する
                    return pagerank

                # 3. 各ノードのページランクを、受け取ったページランクの合計値に更新する
                update_pagerank(pagerank, received)

        # 重要度が高いページ Top10 を出力する
        id_and_rank = [(key, value) for key, value in get_pageranks().items()]
        popular_pages = sorted(id_and_rank, key=lambda x: x[1], reverse=True)[:10]

        # print("Popular pages")
        for i, r in popular_pages:
            print(f"{self.titles[i]}")

        return


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
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "小野妹子")
    wikipedia.find_most_popular_pages()
