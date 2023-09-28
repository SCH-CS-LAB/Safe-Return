# networkx                     2.8.6
# osmnx                        1.6.0

# 위의 라이브러리 버전 자동 설치(안될수도 있음, 안되면 pip로 직접설치 필요)
import subprocess

lib_name_list = ["networkx==2.8.6","osmnx==1.6.0"]

for i in lib_name_list:
    try:
        subprocess.check_call(["pip", "install", i])
    except subprocess.CalledProcessError:
        print(f"{i} lib install failed.")

import networkx as nx
import osmnx as ox

def return_xy(start, end):
    '''위도와 경도 리스트 반환
    @params start : 시작 지점 위도 경도 튜플
    
    @var point : 지도의 중점
    @var distance : 지도의 거리(중점 기준 표현할 거리)
    
    @params end : 도착 지점 위도 경도 튜플
    @return : 위도 경도 동선 리스트, 총 거리(km)
    '''
    point = (round((start[0]+end[0])/2, 7), round((start[1]+end[1])/2, 7))
    distance = int(max(abs(start[0]-end[0]), abs(start[1]-end[1])) * 1000000 + 1)

    # debug: 변수 값 확인
    print(point, distance)
    
    # 중간점(point) 기준 지도 만들기
    G = ox.graph_from_point(center_point=point, dist=distance, network_type="walk")
    G_proj = ox.project_graph(G)
    
    # 시작점 도착점 지정
    orig_node = ox.nearest_nodes(G, start[0], start[1])
    dest_node = ox.nearest_nodes(G_proj, end[0], end[1])
    
    # 동선 검색
    route = nx.shortest_path(G, orig_node, dest_node, weight='length')
    
    # 거리 계산
    len = nx.shortest_path_length(G, orig_node, dest_node, weight='length') / 1000
    
    # 노드 ID 위도,경도 로 변환 
    nodes = G.nodes
    route_coordinates = [(nodes[node]['y'], nodes[node]['x']) for node in route]
    
    return route_coordinates, round(len, 6)

if __name__ == "__main__":
    start = (36.76916, 126.93509)
    end = (36.78006, 126.93287)
    load_list, distance = return_xy(start, end)
    print(distance)
    print(load_list)