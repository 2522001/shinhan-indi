import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
import pandas as pd
import GiExpertControl as giJongmokTRShow
from indiUI import Ui_MainWindow

main_ui = Ui_MainWindow()

class indiWindow(QMainWindow):

    # UI 선언

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IndiExample")
        giJongmokTRShow.SetQtMode(True)
        giJongmokTRShow.RunIndiPython()
        self.rqidD = {}
        main_ui.setupUi(self)      

        main_ui.pushButton.clicked.connect(self.jongmokRecommendButton_clicked)
        main_ui.pushButton_2.clicked.connect(self.portfolioQueryButton_clicked)
        main_ui.pushButton_3_1.clicked.connect(self.buyButton_clicked)
        main_ui.pushButton_3_2.clicked.connect(self.sellButton_clicked)
        #main_ui.pushButton_5_1.clicked.connect(self.JongmokRealTimeQueryButton_clicked)
        #main_ui.pushButton_5_2.clicked.connect(self.JongmokRealTimeStopButton_clicked)
        giJongmokTRShow.SetCallBack('ReceiveData', self.giJongmokTRShow_ReceiveData)

    # 종목 추천

    def jongmokRecommendButton_clicked(self):
        TR_Name = "TR_1856_IND"          
        ret = giJongmokTRShow.SetQueryName(TR_Name)          
        ret = giJongmokTRShow.SetSingleData(0,"0") # 장구분 - 코스피
        ret = giJongmokTRShow.SetSingleData(1,"200") # 조회갯수 - 200개
        rqid = giJongmokTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name

    def calculateMAButton_clicked(self):
        print("검사1 시작")
        TR_Name = "TR_1843_S" 

        # 클릭된 행에 대한 데이터에 액세스하고 필요한 작업 수행
        button = self.sender()
        index = main_ui.tableWidget.indexAt(button.pos())
        if index.isValid():
            row = index.row()
            jongmokCode = main_ui.tableWidget.item(row, 1).text()
            global globalJongmokName
            globalJongmokName = main_ui.tableWidget.item(row, 2).text()
        
        print("종목코드: ", jongmokCode)

        ret = giJongmokTRShow.SetQueryName(TR_Name)          
        ret = giJongmokTRShow.SetSingleData(0, jongmokCode)  # 종목코드
        ret = giJongmokTRShow.SetSingleData(1, "130")  # 조회갯수
        rqid = giJongmokTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name


    # 나의 투자 분석 조회

    def portfolioQueryButton_clicked(self):
        gaejwa_text = main_ui.lineEdit_2_1.text()
        pw_text = main_ui.lineEdit_2_2.text()

        global targetProfit
        targetProfit_text = main_ui.lineEdit_2_3.text()
        targetProfit = targetProfit_text

        TR_Name = "SABA200QB"          
        ret = giJongmokTRShow.SetQueryName(TR_Name)          
        # print(giJongmokTRShow.GetErrorCode())
        # print(giJongmokTRShow.GetErrorMessage())
        ret = giJongmokTRShow.SetSingleData(0,gaejwa_text)
        ret = giJongmokTRShow.SetSingleData(1,"01")
        ret = giJongmokTRShow.SetSingleData(2,pw_text)
        rqid = giJongmokTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name    
    
        
    def giJongmokTRShow_ReceiveData(self,giCtrl,rqid):
        print("in receive_Data:",rqid)
        print('recv rqid: {}->{}\n'.format(rqid, self.rqidD[rqid]))
        TR_Name = self.rqidD[rqid]
        

        # 코스피 시장 내 시가 총액 규모 상위 200위권 내 종목

        print("TR_name : ",TR_Name)
        if TR_Name == "TR_1856_IND":
            tr_data_output = []
            nCnt = giCtrl.GetMultiRowCount()
            print("c")
            for i in range(0, nCnt):
                tr_data_output.append([])

                previousDayChange = str(giCtrl.GetMultiData(i, 3)) # 상한(1)상승(2)보합(3)하한(4)하락(5)

                if previousDayChange == "2" or previousDayChange == "3": # 전날 대비 상승이거나 보합인 경우만 출력

                    button = QPushButton("검사")
                    main_ui.tableWidget.setCellWidget(i, 0, button)
                    button.clicked.connect(self.calculateMAButton_clicked)

                    main_ui.tableWidget.setItem(i,1,QTableWidgetItem(str(giCtrl.GetMultiData(i, 0)))) # 종목코드
                    main_ui.tableWidget.setItem(i,2,QTableWidgetItem(str(giCtrl.GetMultiData(i, 1)))) # 종목명
                    main_ui.tableWidget.setItem(i,3,QTableWidgetItem(str(giCtrl.GetMultiData(i, 2)))) # 현재가
                    main_ui.tableWidget.setItem(i,4,QTableWidgetItem(previousDayChange)) # 전일대비구분
                    main_ui.tableWidget.setItem(i,5,QTableWidgetItem(str(giCtrl.GetMultiData(i, 4)))) # 전일대비
                    main_ui.tableWidget.setItem(i,6,QTableWidgetItem(str(giCtrl.GetMultiData(i, 5)))) # 전일대비율
                    main_ui.tableWidget.setItem(i,7,QTableWidgetItem(str(giCtrl.GetMultiData(i, 14)))) # 시가총액비중

                    for j in range(1,8):
                        tr_data_output[i].append(giCtrl.GetMultiData(i, j))
            

        if TR_Name == "SABA200QB":
            totalProfit_output = []
            totalProfit = 0
            nCnt = giCtrl.GetMultiRowCount()
            print("c")
            for i in range(0, nCnt):
                main_ui.tableWidget_2.setItem(i,0,QTableWidgetItem(str(giCtrl.GetMultiData(i, 0)))) # 종목코드
                main_ui.tableWidget_2.setItem(i,1,QTableWidgetItem(str(giCtrl.GetMultiData(i, 1)))) # 종목명
                main_ui.tableWidget_2.setItem(i,2,QTableWidgetItem(str(giCtrl.GetMultiData(i, 2)))) # 결제일잔고수량
                main_ui.tableWidget_2.setItem(i,3,QTableWidgetItem(str(giCtrl.GetMultiData(i, 5)))) # 현재가
                main_ui.tableWidget_2.setItem(i,4,QTableWidgetItem(str(giCtrl.GetMultiData(i, 6)))) # 평균단가

                try:
                    profitRate = str((float(giCtrl.GetMultiData(i, 5)) - float(giCtrl.GetMultiData(i, 6))) / float(giCtrl.GetMultiData(i, 6)) * 100)
                except ZeroDivisionError:
                    profitRate = "0"
                main_ui.tableWidget_2.setItem(i,5,QTableWidgetItem(str(profitRate))) # 수익률 ((현재가-평균단가)/평균단가*100)

                try:
                    profit = str((float(giCtrl.GetMultiData(i, 5)) - float(giCtrl.GetMultiData(i, 6))) * float(giCtrl.GetMultiData(i, 2)))
                except ValueError:
                    profit = "0"
                    
                totalProfit_output.append(profit)
                print(totalProfit_output)
                main_ui.tableWidget_2.setItem(i,6,QTableWidgetItem(str(profit))) # 수익 ((현재가-평균단가)*결제일잔고수량)

                main_ui.tableWidget_2.setItem(i,7,QTableWidgetItem(str(giCtrl.GetMultiData(i, 3)))) # 매도미체결수량
                main_ui.tableWidget_2.setItem(i,8,QTableWidgetItem(str(giCtrl.GetMultiData(i, 4)))) # 매수미체결수량

            # 목표 수익 달성률 계산

            print("목표 수익 달성률 계산")

            print("목표수익", targetProfit)

            if targetProfit and not targetProfit.isdigit():
                targetProfitProgress = 0
            else:
                profits = [int(float(profit)) for profit in totalProfit_output]
                print("TARGET PROFIT", targetProfit)
                totalProfit = sum(profits)
                print(totalProfit)
                targetProfitProgress = (totalProfit / int(targetProfit)) * 100
                print(targetProfitProgress)

                if targetProfitProgress > 100:
                    targetProfitProgress = 100
                elif targetProfitProgress < 0:
                    targetProfitProgress = 0

            main_ui.progressBar_2.setProperty("value", targetProfitProgress)

        if TR_Name == "TR_1843_S":
            print("[TR_1843_S] 검사1 시작")

            # 종가 데이터 담기

            nCnt = giCtrl.GetMultiRowCount()

            jongmokClosingPriceDate = []
            jongmokLowPrice = []
            jongmokClosingPrice = []

            for i in range(nCnt):
                date = str(giCtrl.GetMultiData(i, 0)) # 일자
                lowPrice = str(giCtrl.GetMultiData(i, 3)) # 저가
                closingPrice = str(giCtrl.GetMultiData(i, 4)) # 종가
                jongmokClosingPriceDate.append(date)
                jongmokLowPrice.append(int(lowPrice))
                jongmokClosingPrice.append(int(closingPrice))

            print(jongmokClosingPriceDate)
            print(len(jongmokClosingPrice))

            # 이동평균선 구하기

            movingAverages = [5, 20, 60, 120]
            MAList = [] # [[날짜, 현재가, 5일선, 20일선, 60일선, 120일선], ...]
            index = 0

            for i in range(5):
                sublist = []
                sublist.append(jongmokClosingPriceDate[index])  # 날짜
                sublist.append(jongmokLowPrice[index])  # 저가

                for interval in movingAverages:
                    if index + interval <= len(jongmokClosingPrice):
                        print(f"index: {index}, interval: {interval}, sublist: {jongmokClosingPrice[index:index+interval]}")
                        # 현재 날짜부터 지정된 간격 동안의 종가를 추출하여 이동평균 계산
                        average = sum(jongmokClosingPrice[index:index+interval]) / interval
                        sublist.append(int(average))
                    else:
                        sublist.append(None) # 충분한 데이터가 없는 경우 처리
                MAList.append(sublist)
                index += 1

            print(MAList)

            # 이동평균선을 활용한 종목 검사

            for sublist in MAList:
                date = sublist[0]
                currentLowPrice = sublist[1]
                ma5 = sublist[2]
                ma20 = sublist[3]
                ma60 = sublist[4]
                ma120 = sublist[5]

                # 각 날짜에 대해 이동평균선 조건 확인
                if ma5 >= ma20 >= ma60 >= ma120:
                    print(f"{globalJongmokName} 검사1-1 통과 {date} 이동평균선이 정배열된 양지차트입니다.")
                    # item = f"{globalJongmokName} 검사1-1 통과 {date} 이동평균선이 정배열된 양지차트입니다."
                    # test = "검사1-1 통과 이동평균선이 정배열된 양지차트입니다."
                    # print(type(test))
                    # main_ui.listWidget_4.addItem(QListWidegetItem(str(test)))
                    print("여기도됨")

                # 각 날짜에 대해 20일선이 주가보다 작거나 같은지 확인
                percent_difference = ((currentLowPrice - ma20) / currentLowPrice) * 100

                if 0 < percent_difference < 0.2:
                    print(f"{globalJongmokName} 검사1-2 통과 {date} 20일선이 주가보다 {percent_difference:.2f}% 만큼 아래에 있습니다.")
                    #item = QListWidgetItem(f"{globalJongmokName} 검사1-2 통과 {date} 20일선이 주가보다 {percent_difference:.2f}% 만큼 아래에 있습니다.")

            # 화면에 MAList 띄우기, 아래 두 조건 확인을 토대로 알림창에 메시지 (검사 통과 or 미통과)
            print("검사1 종료")

            # 외국인/기관 순매수량이 전체 거래량의 20% 이상 TR_1206 7.누적거래량 16.외국인순매수 22.기관순매수

        if TR_Name == "SABA101U1":
            print("매수/매도")
            nCnt = giCtrl.GetSingleRowCount()
            print("c")
            print(nCnt)
            if nCnt != 0:
                print((str(giCtrl.GetSingleData(0))))
                print((str(giCtrl.GetSingleData(1))))
                print((str(giCtrl.GetSingleData(2))))
                print((str(giCtrl.GetSingleData(3))))
                print((str(giCtrl.GetSingleData(4))))
                print((str(giCtrl.GetSingleData(5))))

                # 새로운 행을 추가할 때  << 여기 수정하기
                new_row = QListWidgetItem()
                main_ui.listWidget_3.addItem(new_row)

                # 주문번호, 메시지1, 메시지2, 메시지3을 리스트에 추가
                new_row.setData(0, str(giCtrl.GetSingleData(0)))  # 주문번호
                new_row.setData(1, str(giCtrl.GetSingleData(3)))  # 메시지1
                new_row.setData(2, str(giCtrl.GetSingleData(4)))  # 메시지2
                new_row.setData(3, str(giCtrl.GetSingleData(5)))  # 메시지3
            else:
                print("주문이 정상적으로 처리되지 않았습니다.")

    # 매수

    def buyButton_clicked(self):
        gaejwa = main_ui.lineEdit_3_1.text()
        pw = main_ui.lineEdit_3_2.text()
        jongmokCode = main_ui.lineEdit_3_3.text()
        amount = main_ui.lineEdit_3_4.text()
        price = main_ui.lineEdit_3_5.text()

        TR_Name = "SABA101U1"          
        ret = giJongmokTRShow.SetQueryName(TR_Name)          

        ret = giJongmokTRShow.SetSingleData(0,gaejwa) # 계좌번호
        ret = giJongmokTRShow.SetSingleData(1,"01") # 계좌상품
        ret = giJongmokTRShow.SetSingleData(2,pw) # 계좌비밀번호
        ret = giJongmokTRShow.SetSingleData(3, "")
        ret = giJongmokTRShow.SetSingleData(4, "")
        ret = giJongmokTRShow.SetSingleData(5,"0") # 선물대용매도여부
        ret = giJongmokTRShow.SetSingleData(6,"00") # 신용거래구분 - 보통
        ret = giJongmokTRShow.SetSingleData(7,"2") # 매도매수구분 - 매수
        ret = giJongmokTRShow.SetSingleData(8,jongmokCode) # 종목코드
        ret = giJongmokTRShow.SetSingleData(9,amount) # 주문수량
        ret = giJongmokTRShow.SetSingleData(10,price) # 주문가격
        ret = giJongmokTRShow.SetSingleData(11,"1") # 정규시간외구분코드 - 정규장
        ret = giJongmokTRShow.SetSingleData(12,"2") # 호가유형코드 - 지정가
        ret = giJongmokTRShow.SetSingleData(13,"0") # 주문조건코드 - 일반
        ret = giJongmokTRShow.SetSingleData(14,"0") # 신용대출통합주문구분코드 - 해당없음
        ret = giJongmokTRShow.SetSingleData(15, "")
        ret = giJongmokTRShow.SetSingleData(16, "") 
        ret = giJongmokTRShow.SetSingleData(17, "")
        ret = giJongmokTRShow.SetSingleData(18, "")
        ret = giJongmokTRShow.SetSingleData(19, "")
        ret = giJongmokTRShow.SetSingleData(20, "") # 프로그램매매여부
        ret = giJongmokTRShow.SetSingleData(21, "Y") # 결과메시지 처리여부

        rqid = giJongmokTRShow.RequestData()
        print(giJongmokTRShow.GetErrorCode())
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name 


    # 매도

    def sellButton_clicked(self):
        gaejwa = main_ui.lineEdit_3_1.text()
        pw = main_ui.lineEdit_3_2.text()
        jongmokCode = main_ui.lineEdit_3_3.text()
        amount = main_ui.lineEdit_3_4.text()
        price = main_ui.lineEdit_3_5.text()

        TR_Name = "SABA101U1"          
        ret = giJongmokTRShow.SetQueryName(TR_Name)          

        ret = giJongmokTRShow.SetSingleData(0,gaejwa) # 계좌번호
        ret = giJongmokTRShow.SetSingleData(1,"01") # 계좌상품
        ret = giJongmokTRShow.SetSingleData(2,pw) # 계좌비밀번호
        ret = giJongmokTRShow.SetSingleData(3, "")
        ret = giJongmokTRShow.SetSingleData(4, "")
        ret = giJongmokTRShow.SetSingleData(5,"0") # 선물대용매도여부
        ret = giJongmokTRShow.SetSingleData(6,"00") # 신용거래구분 - 보통
        ret = giJongmokTRShow.SetSingleData(7,"1") # 매도매수구분 - 매도
        ret = giJongmokTRShow.SetSingleData(8,jongmokCode) # 종목코드
        ret = giJongmokTRShow.SetSingleData(9,amount) # 주문수량
        ret = giJongmokTRShow.SetSingleData(10,price) # 주문가격
        ret = giJongmokTRShow.SetSingleData(11,"1") # 정규시간외구분코드 - 정규장
        ret = giJongmokTRShow.SetSingleData(12,"2") # 호가유형코드 - 지정가
        ret = giJongmokTRShow.SetSingleData(13,"0") # 주문조건코드 - 일반
        ret = giJongmokTRShow.SetSingleData(14,"0") # 신용대출통합주문구분코드 - 해당없음
        ret = giJongmokTRShow.SetSingleData(15, "")
        ret = giJongmokTRShow.SetSingleData(16, "") 
        ret = giJongmokTRShow.SetSingleData(17, "")
        ret = giJongmokTRShow.SetSingleData(18, "")
        ret = giJongmokTRShow.SetSingleData(19, "")
        ret = giJongmokTRShow.SetSingleData(20, "") # 프로그램매매여부
        ret = giJongmokTRShow.SetSingleData(21, "Y") # 결과메시지 처리여부

        rqid = giJongmokTRShow.RequestData()
        print(giJongmokTRShow.GetErrorCode())
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name 



if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = indiWindow()    
    IndiWindow.show()
    app.exec_()