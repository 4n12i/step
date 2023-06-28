#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def find_cross_line(tour, cities):
    """
    交差している2線を探して、それらの始点(or 終点)を交換する

    経路のリストの後ろの方が点と点の距離が長い傾向にあるので、
    リストの後ろから順に交差している線があるか調べる
    """

    def is_cross(a, b, c, d):
        """
        線が交差していたら True を返す
        st < 0 のとき2線(ab, cd)が交差している
        """

        s = (cities[a][0] - cities[b][0]) * (cities[c][1] - cities[a][1]) - (cities[a][1] - cities[b][1]) * (cities[c][0] - cities[a][0])
        t = (cities[a][0] - cities[b][0]) * (cities[d][1] - cities[a][1]) - (cities[a][1] - cities[b][1]) * (cities[d][0] - cities[a][0])
        if s * t > 0:
            return False

        s = (cities[c][0] - cities[d][0]) * (cities[a][1] - cities[c][1]) - (cities[c][1] - cities[d][1]) * (cities[a][0] - cities[c][0])
        t = (cities[c][0] - cities[d][0]) * (cities[b][1] - cities[c][1]) - (cities[c][1] - cities[d][1]) * (cities[b][0] - cities[c][0])
        if s * t > 0:
            return False

        return True


    n = len(tour)
    for i in range(n-1,0,-1):   # TODO: 交差した線がなくなるまで繰り返す
        for k in range(i):  # TODO: k = n-1 のときは k + 1 じゃなくて 0 にする
            if k == i - 1 or k == i - 2:
                continue

            if is_cross(tour[i-1], tour[i], tour[k], tour[k + 1]):
                # print(f"cross a:{tour[i - 1]} b:{tour[i]} c:{tour[k]} d:{tour[k + 1]}, {i-1,i,k,k+1}")

                # 入れ替えた点と点の間の経路を反転する
                if i > k:
                    tour = tour[:k+1] + tour[k+1:i+1][::-1] + tour[i+1:]
                else:
                    tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
                break   
    
    return tour


def solve(cities):
    N = len(cities)

    # 点と点の距離を求めてリストに挿入する
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j]) 

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city] # 経路

    # 経路を求める
    while unvisited_cities:
        # 一番距離が短い点と点のペアを探し、経路 tour に挿入する
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    tour = find_cross_line(tour, cities) # 交差している2線を交換する（2-opt）

    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
