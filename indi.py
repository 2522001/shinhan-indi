import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
import pandas as pd
import GiExpertControl as giLogin
import GiExpertControl as giStockTRShow
import GiExpertControl as giJongmokRealTime
from TestUI import Ui_MainWindow

main_ui = Ui_MainWindow()

class indiWindow(QMainWindow):
    # UI 선언
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IndiExample")
        giStockTRShow.SetQtMode(True)
        giStockTRShow.RunIndiPython()
        giLogin.RunIndiPython()
        giJongmokRealTime.RunIndiPython()
        self.rqidD = {}
        main_ui.setupUi(self)      

        main_ui.pushButton.clicked.connect(self.pushButton_clicked)
        main_ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        main_ui.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        giStockTRShow.SetCallBack('ReceiveData', self.giStockTRShow_ReceiveData)
        giJongmokRealTime.SetCallBack('ReceiveRTData', self.giJongmokRealTime_ReceiveRTData)
        
        print(giLogin.GetCommState())
        if giLogin.GetCommState() == 0: # 정상
            print("")        
        elif  giLogin.GetCommState() == 1: # 비정상
        #본인의 ID 및 PW 넣으셔야 합니다.
            login_return = giLogin.StartIndi('아이디','비밀번호','공인인증서 비밀번호', 'C:\\SHINHAN-i\\indi\\GiExpertStarter.exe')
            if login_return == True:
                print("INDI 로그인 정보","INDI 정상 호출")
            else:
                print("INDI 로그인 정보","INDI 호출 실패")                    

    def pushButton_clicked(self):
        gaejwa_text = main_ui.textEdit.toPlainText()
        pw_text = main_ui.textEdit_2.toPlainText()
        sellBuy_text = main_ui.textEdit_3.toPlainText()
        # jongmokCode_text = main_ui.textEdit_4.toPlainText()
        # amount_text = main_ui.textEdit_5.toPlainText()
        # price_text = main_ui.textEdit_6.toPlainText()

        TR_Name = "SABA101U1"          
        ret = giStockTRShow.SetQueryName(TR_Name)          
        # print(giStockTRShow.GetErrorCode())
        # print(giStockTRShow.GetErrorMessage())
        ret = giStockTRShow.SetSingleData(0,gaejwa_text) # 계좌번호
        ret = giStockTRShow.SetSingleData(1,"01") # 계좌상품
        ret = giStockTRShow.SetSingleData(2,pw_text) # 계좌비밀번호
        ret = giStockTRShow.SetSingleData(5,"0") # 선물대용매도여부
        ret = giStockTRShow.SetSingleData(6,"00") # 신용거래구분 - 보통
        ret = giStockTRShow.SetSingleData(7,sellBuy_text) # 매도매수구분
        ret = giStockTRShow.SetSingleData(8,jongmokCode_text) # 종목코드
        ret = giStockTRShow.SetSingleData(9,amount_text) # 주문수량
        ret = giStockTRShow.SetSingleData(10,price_text) # 주문가격
        ret = giStockTRShow.SetSingleData(11,"1") # 정규시간외구분코드 - 정규장
        ret = giStockTRShow.SetSingleData(12,"2") # 호가유형코드 - 지정가
        ret = giStockTRShow.SetSingleData(13,"0") # 주문조건코드 - 일반
        ret = giStockTRShow.SetSingleData(14,"0") # 신용대출통합주문구분코드 - 해당없음
        rqid = giStockTRShow.SetSingleData(21, "Y") # 결과메시지 처리여부
        rqid = giStockTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name           
        
    def giStockTRShow_ReceiveData(self,giCtrl,rqid):
        print("in receive_Data:",rqid)
        print('recv rqid: {}->{}\n'.format(rqid, self.rqidD[rqid]))
        TR_Name = self.rqidD[rqid]
        print("TR_name : ",TR_Name)

        if TR_Name == "SABA101U1":
            main_ui.tableWidget_3.insertRow(main_ui.tableWidget_3.rowCount())
            final_rowCount = main_ui.tableWidget_3.rowCount() - 1
            main_ui.tableWidget_3.setItem(final_rowCount,0,QTableWidgetItem(str(giCtrl.GetSingleData(0)))) # 주문번호
            main_ui.tableWidget_3.setItem(final_rowCount,1,QTableWidgetItem(str(giCtrl.GetSingleData(3)))) # 메시지1
            main_ui.tableWidget_3.setItem(final_rowCount,2,QTableWidgetItem(str(giCtrl.GetSingleData(4)))) # 메시지2
            main_ui.tableWidget_3.setItem(final_rowCount,3,QTableWidgetItem(str(giCtrl.GetSingleData(5)))) # 메시지3

                       


    def pushButton_2_clicked(self):      
        jongmokCode = main_ui.textEdit_7.toPlainText()
        rqid = giJongmokRealTime.RequestRTReg("SC",jongmokCode)
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid)) 

    def giJongmokRealTime_ReceiveRTData(self,giCtrl,RealType):
        if RealType == "SC":
            main_ui.tableWidget_2.insertRow(main_ui.tableWidget_2.rowCount())
            final_rowCount = main_ui.tableWidget_2.rowCount() - 1
            main_ui.tableWidget_2.setItem(final_rowCount,0,QTableWidgetItem(str(giCtrl.GetSingleData(1))))
            main_ui.tableWidget_2.setItem(final_rowCount,1,QTableWidgetItem(str(giCtrl.GetSingleData(2))))
            main_ui.tableWidget_2.setItem(final_rowCount,2,QTableWidgetItem(str(giCtrl.GetSingleData(3))))
            main_ui.tableWidget_2.setItem(final_rowCount,3,QTableWidgetItem(str(giCtrl.GetSingleData(6))))
    
    def pushButton_3_clicked(self):
        giJongmokRealTime.UnRequestRTReg("SC", "")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = indiWindow()    
    IndiWindow.show()
    app.exec_()
    
    if IndiWindow.MainSymbol != "":
        giJongmokRealTime.UnRequestRTReg("SC", "")