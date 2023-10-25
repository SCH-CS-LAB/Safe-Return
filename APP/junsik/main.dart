import 'dart:async';
import 'dart:developer' show log;
import 'package:flutter/material.dart';
import 'package:flutter_naver_map/flutter_naver_map.dart';

void main() async {
  await _initialize();
  runApp(NaverMapApp());
}

Future<void> _initialize() async {
  WidgetsFlutterBinding.ensureInitialized();
  await NaverMapSdk.instance.initialize(
      clientId: 's5bm2ba7yr',
      onAuthFailed: (ex) => log("********* 네이버맵 인증오류 : $ex *********"));
}

class NaverMapApp extends StatelessWidget {
  final int? testId;

  const NaverMapApp({super.key, this.testId});

  @override
  Widget build(BuildContext context) => MaterialApp(
      home: testId == null
          ? const FirstPage()
          : TestPage(key: Key("testPage_$testId")));
}

class FirstPage extends StatelessWidget {
  const FirstPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('First Page')),
        body: Center(
            child: ElevatedButton(
                onPressed: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => const TestPage()));
                },
                child: const Text('Go to Second Page'))));
  }
}

class TestPage extends StatefulWidget {
  const TestPage({Key? key}) : super(key: key);

  @override
  State<TestPage> createState() => TestPageState();
}

class TestPageState extends State<TestPage> {
  late NaverMapController _mapController;
  final Completer<NaverMapController> mapControllerCompleter = Completer();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF343945),
      body: Center(
        child: _naverMapSection(), // 네이버 지도 섹션으로 대체
      ),
    );
  }
  void drawPath(NaverMapController controller) {
    final pathOverlay = NPathOverlay(
      coords: [
        NLatLng(37.506932467450326, 127.05578661133796), // 출발지 좌표
        NLatLng(37.606932467450326, 127.05578661133796), // 도착지 좌표
      ],
      color: Colors.blue,
      width: 8.0,
      id: 'walkPath',
    );
    controller.addOverlay(pathOverlay);
  }


  Widget _naverMapSection() {
    return NaverMap(
      options: const NaverMapViewOptions(
        indoorEnable: true,
        locationButtonEnable: false,
        consumeSymbolTapEvents: false,
      ),
      onMapReady: (controller) async {
        _mapController = controller;
        mapControllerCompleter.complete(controller);

        // 네이버 지도가 준비되면 출발지와 도착지 마커를 추가합니다.
        final marker = NMarker(
          id: 'start',
          position: const NLatLng(37.506932467450326, 127.05578661133796),
        );
        final marker1 = NMarker(
          id: 'destination',
          position: const NLatLng(37.606932467450326, 127.05578661133796),
        );

        controller.addOverlayAll({marker, marker1});

        // 경로를 그리기 위해 NPathOverlay를 사용합니다.
        final pathOverlay = NPathOverlay(
          coords: [marker.position, marker1.position],
          color: Colors.blue,
          width: 8.0, id: '',
        );
        controller.addOverlay(pathOverlay);

        // 마커 정보창 설정
        final onMarkerInfoWindow = NInfoWindow.onMarker(id: marker.info.id, text: "출발지");
        marker.openInfoWindow(onMarkerInfoWindow);
        final onMarkerInfoWindow1 = NInfoWindow.onMarker(id: marker1.info.id, text: "도착지");
        marker1.openInfoWindow(onMarkerInfoWindow1);
      },
    );
  }
}

