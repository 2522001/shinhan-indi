import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
import pandas as pd
import GiExpertControl as giLogin
import GiExpertControl as giCapitalizationTRShow
import GiExpertControl as giJongmokRealTime
from TestUI import Ui_MainWindow

main_ui = Ui_MainWindow()

class indiWindow(QMainWindow):
    # UI 선언
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IndiExample")
        giCapitalizationTRShow.SetQtMode(True)
        giCapitalizationTRShow.RunIndiPython()
        giLogin.RunIndiPython()
        giJongmokRealTime.RunIndiPython()
        self.rqidD = {}
        main_ui.setupUi(self)      

        main_ui.pushButton.clicked.connect(self.pushButton_clicked)
        #main_ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        #main_ui.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        giCapitalizationTRShow.SetCallBack('ReceiveData', self.giCapitalizationTRShow_ReceiveData)
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

        TR_Name = "TR_1856_IND"          
        ret = giCapitalizationTRShow.SetQueryName(TR_Name)          
        # print(giCapitalizationTRShow.GetErrorCode())
        # print(giCapitalizationTRShow.GetErrorMessage())
        ret = giCapitalizationTRShow.SetSingleData(0,"0") # 장구분 - 코스피
        ret = giCapitalizationTRShow.SetSingleData(1,"200") # 조회갯수 - 200개
        rqid = giCapitalizationTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name           

    def giCapitalizationTRShow_ReceiveData(self,giCtrl,rqid):
        print("in receive_Data:",rqid)
        print('recv rqid: {}->{}\n'.format(rqid, self.rqidD[rqid]))
        TR_Name = self.rqidD[rqid]
        tr_data_output = []
        output = []

        print("TR_name : ",TR_Name)
        if TR_Name == "SABA200QB":
            nCnt = giCtrl.GetMultiRowCount()
            print("c")
            for i in range(0, nCnt):
                tr_data_output.append([])
                # main_ui.tableWidget_3.setItem(final_rowCount,0,QTableWidgetItem(str(giCtrl.GetSingleData(1)))) # 종목명
                # main_ui.tableWidget_3.setItem(final_rowCount,0,QTableWidgetItem(str(giCtrl.GetSingleData(13)))) # 시가총액
                for j in range(0,2):
                    tr_data_output[i].append(giCtrl.GetMultiData(i, j))
            print(type(tr_data_output))
            print(tr_data_output)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = indiWindow()    
    IndiWindow.show()
    app.exec_()
    
    if IndiWindow.MainSymbol != "":
        giJongmokRealTime.UnRequestRTReg("SC", "")