import requests
import getAppKey # SK AppKey 불러온다

class SK_API_CLASS:
    '''SK API를 이용해 길찾기를 제공하는 클래스
    종속성 -> getAppKey.py

    @method setHeaders -> POST 통신을 위한 기본 헤더를 설정해주는 함수
    @method returnApiJson -> POST 통신 후 json 형식으로 반환 해주는 함수
    @method returnApiRoute -> 동선 리스트를 반환해주는 함수

    @method apiWalkerStartEnd -> 도보 길찾기를 반환해주는 함수
    - 종속된 메소드 목록
        - returnApiJson
        - returnApiRoute
    '''
    def __init__(self):
        '''
        @var appkey -> SK API 키 값
        @var headers -> POST 통신 기본 헤더 값
        '''
        self.appkey = getAppKey.GetAppKey()
        self.headers = self.setHeaders()

    def debugApiTest(self):
        '''테스트용 이므로 사용 X'''
        url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
        appkey = 'AGDrqSCZzya3GshmeroNH8riWQSANOc868dvdL72'

        # X, Y 좌표 바뀌어 있음
        startX = 126.93489
        startY = 36.76905
        endX = 126.93263
        endY = 36.7737
        startName = '출발지'
        endName = '도착지'

        header = {
            'Accept': 'application/json',
            'Content-Type' : 'application/json',
            'appKey' : self.appkey
        }
        data = {
            "startX": startX,
            "startY": startY,
            "endX": endX,
            "endY": endY,
            "startName": startName,
            "endName": endName
        }

        print(requests.post(url, headers=header, json=data).json())

    def setHeaders(self) -> dict:
        '''헤더 지정 후 헤더를 반환하는 함수
        @var header -> 헤더 값
        @return -> 헤더 딕셔너리 값
        '''
        headers = {
            'Accept': 'application/json',
            'Content-Type' : 'application/json',
            'appKey' : self.appkey
        }

        return headers
    
    def returnApiJson(self, url:str, headers:dict, data:dict) -> str:
        '''API POST 통신 후 응답을 Json으로 반환하는 함수
        @param url -> POST 통신 주소 값
        @param headers -> POST 통신 헤더 값
        @param data -> POST 통신 데이터 값

        @return Json 형식인 POST의 응답
        '''
        return requests.post(url, headers=headers, json=data).json()
    
    def returnApiRoute(self, jsonData:str) -> list:
        '''API POST 통신 후 반환된 Json을 받아 동선 리스트를 반환
        @param jsonData -> Json 형식의 데이터

        @var route_list -> 반환할 동선 리스트
        @var feature -> Json의 features 속성(GeoJSON 형상 정보)
        @var types -> Json의 type 속성 리스트(GeoJSON 유형 정보)
        @var values -> 필요한 동선, 2차원으로 되어있어 1차원으로 변경
        @var value -> 필요한 동선 1차원의 모양을 가진다.

        @return 리스트 형식의 동선 리스트
        '''
        route_list = []

        for feature in jsonData['features']:
            types = feature['geometry']['type']

            if types == "LineString":
                values = feature['geometry']['coordinates']

                for value in values:
                    route_list.append(value)

        return route_list
    
    def apiWalkerStartEnd(self, startPoint:tuple, endPoint:tuple) -> list:
        '''SK API를 이용해 도보 동선을 반환하는 함수
        @param startPoint -> 시작지점 좌표 튜플
        @param endPoint -> 도착지점 좌표 튜플

        @var url -> API 주소값
        @var startX -> 시작지점 위도
        @var startY -> 시작지점 경도
        @var endX -> 도착지점 위도
        @var endY -> 도착지점 경도
        @var startName -> 시작점 명칭
        @var endName -> 도착점 명칭
        @var data -> API POST에 보낼 data 값
        @var jsonData -> Json 형식의 응답 데이터

        @return 2차원 리스트 형식의 동선
        '''
        url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
        startX, startY = startPoint
        endX, endY = endPoint
        startName = 'StartPoint'
        endName = 'EndPoint'

        data = {
            "startX": startX,
            "startY": startY,
            "endX": endX,
            "endY": endY,
            "startName": startName,
            "endName": endName
        }

        jsonData = self.returnApiJson(url, self.headers, data)
        return self.returnApiRoute(jsonData)
