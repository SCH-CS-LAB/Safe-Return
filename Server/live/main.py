from SK_API import SK_API_CLASS

startPoint = (126.93489, 36.76905)  # 순천향대 멀티미디어관
endPoint = (126.93263, 36.7737)     # 고고쓰 순천향대점

sac = SK_API_CLASS()

# sac.debugApiTest()

route = sac.apiWalkerStartEnd(startPoint, endPoint)

print(route)

# 동선 확인을 위한 folium 라이브러리
import folium

centerPoint = (36.77017, 126.93252)     # 순천향대학교
route = [[y, x] for x, y in route] # 위도 경도 값 리버스, 두 라이브러리가 위도 경도 위치가 다르다.

m = folium.Map(location=centerPoint, zoom_start=50)
folium.PolyLine(locations=route, tooltip='Polyline').add_to(m)
m.save('output.html')
