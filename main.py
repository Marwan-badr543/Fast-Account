# you are professional python programmer and inspector , i have a big program made with pyqt5 but it has some issues related to fetching from database happens if database is empty, I will give you function then another function till the program end and i want you to inspect each function and correct these issues but without changing the main goal of the function you just will decrease the errors that may happen under any case and focus more on database ,remember don't change the main goal of the function and don't print any thing in the it as no one will see it and don't make spaces between lines and make an intendent block tab as i'm using class ,if you have any question feel free to ask, speak arabic and tell me about the things you fixed, good luck.
from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox,QPushButton,QMessageBox,QInputDialog,QLineEdit,QLabel,QTextEdit,QHBoxLayout,QSpacerItem
from PyQt5.QtGui import QFont,QIcon
from cashierpro_ui import Ui_MainWindow
import mysql.connector   
from datetime import datetime 
import calendar
from PyQt5.QtCore import QTimer, QDateTime,Qt,QLocale  
from dateutil.relativedelta import relativedelta 
import json
# from escpos.printer import Usb
# C:\Users\hp\AppData\Local\Programs\Python\Python310\Lib\site-packages\escpos
# pyinstaller --onefile --add-data "C:\Users\hp\AppData\Local\Programs\Python\Python310\Lib\site-packages\escpos;escpos" --noconsole updatedMain.py
# 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # Enable high DPI scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)     # Use high DPI icons    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
        self.conn = mysql.connector.connect(
            host="192.168.1.7",  # استبدل بـ عنوان IP للجهاز المركزي
            user="root",      # استبدل باسم المستخدم الذي قمت بإنشائه
            password="777_333_res",  # استبدل بكلمة المرور التي أنشأتها
            database="restaurant",
            port="3306"
            )       
        self.cr = self.conn.cursor()  

#######################################################################################################################################################
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        QLocale.setDefault(locale)
    
        self.setWindowTitle("Fast Account 2")
        self.icon = QIcon('fastAccount.ico')
        self.setWindowIcon(self.icon)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) 
        self.update_time()
        self.currentDate=datetime.now().strftime('%Y-%m-%d')
        self.currentDateTime=datetime.strptime(self.currentDate, "%Y-%m-%d")
        self.current_time = QDateTime.currentDateTime()
        self.formatted_time = self.current_time.toString("yyyy-MM-dd  |  hh:mm:ss")
        self.currentDay=datetime.now().strftime('%d')
        self.currentMonth=datetime.now().strftime('%m')
        self.currentYear=datetime.now().strftime('%Y')
         
        self.cr.execute("CREATE TABLE IF NOT EXISTS departmentsTables (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL)")
        self.cr.execute("CREATE TABLE IF NOT EXISTS productsTables (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,department_id INT)")
        self.cr.execute("CREATE TABLE IF NOT EXISTS departments (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL)")
        self.cr.execute("CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,department_id INT,price DECIMAL(11, 2) NOT NULL DEFAULT 0.00)")
        self.cr.execute("CREATE TABLE IF NOT EXISTS numberOFUnits (PorName TEXT , date DATE NOT NULL, NOU INTEGER )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS MnumberOFUnits (PorName TEXT , date DATE NOT NULL, NOU INTEGER )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS YnumberOFUnits (PorName TEXT , date DATE NOT NULL, NOU INTEGER )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS newShift (expName TEXT , revName TEXT , salesCash DECIMAL(11, 2) , visaCash DECIMAL(11, 2) , expenses DECIMAL(11, 2) , revenues DECIMAL(11, 2), date DATE NOT NULL )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS delivery (name VARCHAR(255) NOT NULL, amount DECIMAL(11, 2) NOT NULL)")
        self.cr.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, adress TEXT, mSalary DECIMAL(11, 2) NOT NULL, id INT AUTO_INCREMENT PRIMARY KEY, phnNmbr TEXT, nmbrOabsnts INTEGER, DOwork TEXT , DOabsence TEXT, DOpresent TEXT) ")        
        self.cr.execute("CREATE TABLE IF NOT EXISTS expenses (expName TEXT ,expense_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS revenues (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS revenuesVisa (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS taxes (name TEXT , amount DECIMAL(11, 2) NOT NULL)")
        self.cr.execute("CREATE TABLE IF NOT EXISTS bonusOrDeduct (empID INTEGER NOT NULL , bonus DECIMAL(11, 2) NOT NULL DEFAULT 0, deduction DECIMAL(11, 2) NOT NULL DEFAULT 0, payable DECIMAL(11, 2) NOT NULL DEFAULT 0,date DATE NOT NULL )")
        self.conn.commit()  

#######################################################  Side bar  #########################################################
        self.ui.frame_2.hide()
        self.ui.pushButton_9.hide()
        self.ui.pushButton.hide()
        self.ui.pushButton_2.hide()
        self.ui.pushButton_10.hide()
        self.ui.casherBtn.hide()
        self.ui.employeeBtn.hide()
        self.ui.recortBtn.hide()
        self.ui.showBtn.hide()
        self.ui.issueBtn.hide()
        self.ui.loginAoUBtn.clicked.connect(self.adminOrUser)
        self.ui.backToCBBtn.clicked.connect(self.to_casher_page)
        self.ui.casherBtn.clicked.connect(self.to_casher_page)
        self.ui.employeeBtn.clicked.connect(self.to_employee_page)
        self.ui.recortBtn.clicked.connect(self.to_record_page)
        self.ui.showBtn.clicked.connect(self.to_show_page)
        self.ui.issueBtn.clicked.connect(self.to_issue_page)
        self.ui.settingBtn.clicked.connect(self.to_setting_page)
        self.ui.tablesBtn.clicked.connect(self.to_table_page)
        self.ui.backFromDailySales.clicked.connect(self.backToShowPage)
        self.ui.backfromMonthlySales.clicked.connect(self.backToShowPage)
        self.ui.backfromYearlySales.clicked.connect(self.backToShowPage)
        self.ui.backfromMIS.clicked.connect(self.backToIssuePage)
        self.ui.backfromTMIS.clicked.connect(self.backToIssuePage)
        self.ui.backfromSMIS.clicked.connect(self.backToIssuePage)
        self.ui.backfromYIS.clicked.connect(self.backToIssuePage)
        self.ui.backFromCashierReport.clicked.connect(self.backToIssuePage)
#######################################################  Cashier Page  #########################################################
        self.ui.valueAddedTax.setReadOnly(True)
        self.ui.serviceTax.setReadOnly(True)
        self.ui.discount.setReadOnly(True)
        self.conn.commit()
        self.cr.execute("SELECT amount FROM taxes WHERE name = 'valueAddedTax'")
        addedTaxAmount = self.cr.fetchone()  
        if addedTaxAmount==None:
            self.cr.execute("INSERT INTO taxes (name, amount) VALUES ('valueAddedTax',0)")
            self.cr.execute("INSERT INTO taxes (name, amount) VALUES ('serviceTax',0)")
            self.cr.execute("INSERT INTO taxes (name, amount) VALUES ('discount',0)")
        self.cr.execute("SELECT amount FROM taxes WHERE name = 'valueAddedTax'")
        valueAddedTax = self.cr.fetchone()  
        self.cr.execute("SELECT amount FROM taxes WHERE name = 'serviceTax'")
        serviceTax = self.cr.fetchone()  
        self.cr.execute("SELECT amount FROM taxes WHERE name = 'discount'")
        discount = self.cr.fetchone()  
        self.ui.valueAddedTax.setText(f"{valueAddedTax[0]} %")
        self.ui.serviceTax.setText(f"{serviceTax[0]}")
        self.ui.discount.setText(f"{discount[0]} %" )
        self.totalList=[]
        self.totalPrice=0
        self.orderedNames=[]
        self.orderedPrices=[]
        self.totalPay1=[]
        self.proID=[]
        self.totalPay2=""
        self.ui.checkBox.setEnabled(False)
        self.number_of_units = 0  
        self.NOU=[]
        self.updatedProNumOfUnits = []    
        self.ui.unit1Btn.clicked.connect(lambda: self.update_units(1))
        self.ui.unit2Btn.clicked.connect(lambda: self.update_units(2))
        self.ui.unit3Btn.clicked.connect(lambda: self.update_units(3))
        self.ui.unit4Btn.clicked.connect(lambda: self.update_units(4))
        self.ui.unit5Btn.clicked.connect(lambda: self.update_units(5))
        self.ui.unit6Btn.clicked.connect(lambda: self.update_units(6))
        self.ui.unit7Btn.clicked.connect(lambda: self.update_units(7))
        self.ui.issueBillBtn.clicked.connect(self.issueBill)
        self.ui.totalBtn.clicked.connect(self.getTotalAfterUpdate)
        
        self.ui.payBtn1.clicked.connect(lambda: self.totalPayf2(1))
        self.ui.payBtn2.clicked.connect(lambda: self.totalPayf2(2))
        self.ui.payBtn3.clicked.connect(lambda: self.totalPayf2(3))
        self.ui.payBtn4.clicked.connect(lambda: self.totalPayf2(4))
        self.ui.payBtn5.clicked.connect(lambda: self.totalPayf2(5))
        self.ui.payBtn6.clicked.connect(lambda: self.totalPayf2(6))
        self.ui.payBtn7.clicked.connect(lambda: self.totalPayf2(7))
        self.ui.payBtn8.clicked.connect(lambda: self.totalPayf2(8))
        self.ui.payBtn9.clicked.connect(lambda: self.totalPayf2(9))
        self.ui.payBtn0.clicked.connect(lambda: self.totalPayf2(0))
        self.ui.payBtn20.clicked.connect(lambda: self.totalPayf1(20))
        self.ui.payBtn50.clicked.connect(lambda: self.totalPayf1(50))
        self.ui.payBtn100.clicked.connect(lambda: self.totalPayf1(100))
        self.ui.payBtn200.clicked.connect(lambda: self.totalPayf1(200))
                              
        # self.title="الصنف".ljust(40)+"السعر".ljust(32)+"العدد".ljust(30)+"الإجمالي".ljust(18)
        # self.title+="--------------------------------------------------------------------------------------------------\n"
        # self.ui.textEdit.append(self.title)
        self.showDepartments()
        self.showDepartmentsTables()
        self.ui.manageDep.clicked.connect(self.manageDepartments)
        self.ui.managePro.clicked.connect(self.manageProducts)
        self.ui.manageDepTables.clicked.connect(self.manageDepartmentsTables)
        self.ui.manageProTables.clicked.connect(self.manageProductsTables)
        self.ui.UpdateTaxBtn.clicked.connect(self.update_tax)
        self.ui.clearCashierBtn.clicked.connect(self.clearCashierData)
        self.ui.unit10Btn_5.clicked.connect(self.update_unitsUP)
        self.ui.unit10Btn_4.clicked.connect(self.update_unitsRow)
        self.ui.label_7.setText(str(self.number_of_units))
        ################# Tables department ###############################
        self.tablesNamelist=[]
        self.table_states = self.load_table_states()
        ################# employees department ###############################

        self.ui.addEmpBtn.clicked.connect(self.addEmployee)
        self.ui.empBtnSrch.clicked.connect(self.searchEmployee)
        self.ui.saveAbsentBtn.clicked.connect(self.EmployeeAbsences)
        self.ui.clearEmpBtn.clicked.connect(self.clearData)
        self.ui.updateEmpBtn.clicked.connect(self.updateEmployeeData)
        self.ui.layoffEmpBtn.clicked.connect(self.layEmployeeOFF)
        #
        self.ui.refreshEmpSalaryBtn.clicked.connect(self.fetch_and_show_employees)
        self.ui.saveBonusOrDeduction.clicked.connect(self.addBonusOrDeduct)
    #######################################################  Record Page  #########################################################
        self.deleveryCB()
        self.ui.addDeliveryBtn.clicked.connect(self.add_delivery)
        self.ui.searchDeliveryBtn.clicked.connect(self.search_delivery)
        self.ui.deleteDeliveryBtn.clicked.connect(self.delete_delivery)
        self.ui.SaveRevAndExpBtn.clicked.connect(self.addExpensesAndRev)
    #######################################################  Show Page  #########################################################
        self.ui.showRevBtn.clicked.connect(self.showDailyRev)
        self.ui.showExpBtn.clicked.connect(self.showExpenses)
        self.ui.printCasherReportBtn.clicked.connect(self.cashierReport)
        self.ui.printDailyUnitsBtn.clicked.connect(self.printDailyUnits)
        self.ui.printMonthlyUnitsBtn.clicked.connect(self.printMonthlyUnits)
        self.ui.printYearlyUnitsBtn.clicked.connect(self.printYearlyUnits)
        self.deleteDMYtables()
    #######################################################  Setting Page  #########################################################
        self.ui.companyName.setText("Fast Account 2")
        self.ui.aboutBtn.clicked.connect(self.aboutMe)

    #######################################################  Issue Page  #########################################################
        self.ui.newShiftBtn.clicked.connect(self.newShift)
        self.ui.printISBtn.clicked.connect(self.IS)
#********************************************************************************************************************************************#
#********************************************************************************************************************************************#
#********************************************************************************************************************************************#
        if self.ui.settingBtn.isChecked()==True:
            self.to_setting_page()
    
    def aboutMe(self):
        QMessageBox.about(self, "عن المطور", """المطور : مروان أشرف\nرقم الهاتف : 01007258086\nالإيميل : marwanbadr514@Gmail.com""")
    
    def adminOrUser(self):
        if self.ui.radioAdminBtn.isChecked()==True:
            if self.ui.passwordAoU.text()=="admin":
                self.ui.casherBtn.show()
                self.ui.employeeBtn.show()
                self.ui.recortBtn.show()
                self.ui.showBtn.show()
                self.ui.issueBtn.show()
                self.ui.frame_2.show()
                self.ui.pushButton.show()
                self.ui.pushButton_10.show()
                self.ui.frame_54.show()  
                self.ui.manageDepTables.show()                
                self.ui.manageProTables.show()                                              
                self.ui.manageDep.show()                
                self.ui.managePro.show()
                self.ui.line_6.show()                
                self.ui.UpdateTaxBtn.show()                                                                              
                self.ui.passwordAoU.setText("")                              
            else:
                self.statusBar().showMessage(f"Incorrect password...", 3000)
        elif self.ui.radioUserBtn.isChecked()==True: 
            if self.ui.passwordAoU.text()=="user":
                self.ui.casherBtn.show()
                self.ui.recortBtn.show()
                self.ui.frame_54.hide()
                self.ui.frame_2.show()
                self.ui.pushButton.show()
                self.ui.pushButton_10.show()  
                self.ui.showBtn.hide()
                self.ui.issueBtn.hide()
                self.ui.employeeBtn.hide()                
                self.ui.manageDepTables.hide()                
                self.ui.manageProTables.hide()                
                self.ui.manageDep.hide()                
                self.ui.managePro.hide()                
                self.ui.line_6.hide()                
                self.ui.UpdateTaxBtn.hide()                
                self.ui.passwordAoU.setText("")              
            else:
                self.statusBar().showMessage(f"Incorrect password...", 3000)
        else:
            self.statusBar().showMessage(f"You must choose Admin or User...", 3000)
    
    def update_time(self):
        current_time = QDateTime.currentDateTime()
        formatted_time = current_time.toString("yyyy-MM-dd  |  hh:mm:ss")
        self.ui.timeLabel.setText(formatted_time)  
        
    def to_casher_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.destinationCB.clear()
        self.ui.destinationCB.addItem("Choose destination")
        self.deleveryCB()
        
    def to_employee_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def to_record_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def to_show_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def to_issue_page(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def to_setting_page(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def to_table_page(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def backToShowPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)
   
    def backToIssuePage(self):
        self.ui.stackedWidget.setCurrentIndex(4)    
#######################################################  Cashier Page  #########################################################
    def get_departments(self):
        self.cr.execute("CREATE TABLE IF NOT EXISTS departments (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL)")
        self.conn.commit()
        self.cr.execute("SELECT id, name FROM departments")
        results = self.cr.fetchall()
        return results 
            
    def get_products(self, department_id):
        self.cr.execute("CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, department_id INT, price DECIMAL(10, 2) NOT NULL DEFAULT 0.00)")
        self.conn.commit()
        self.cr.execute("SELECT id, name, price FROM products WHERE department_id = %s", (department_id,))
        results = self.cr.fetchall()
        return  results
    
    def showDepartments(self):
        try:
            for i in reversed(range(self.ui.departmentGridLayout.count())):
                self.ui.departmentGridLayout.itemAt(i).widget().setParent(None)
            self.cr.execute("SELECT id, name FROM departments")
            self.departments = self.cr.fetchall()
            if not self.departments:
                return []
            for index, (id, name) in enumerate(self.departments):
                btn = QPushButton(name)
                btn.setStyleSheet("""
                QPushButton, QToolButton, QCommandLinkButton {
                    padding: 0 5px;
                    border-style: solid;
                    border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-right-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-bottom-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-left-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-width: 2px;
                    border-radius: 8px;
                    color: #616161;
                    font-weight: bold;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #fbfdfd, stop:0.5 #ffffff, stop:1 #fbfdfd);
                }
                QPushButton::default, QToolButton::default, QCommandLinkButton::default {
                    border: 2px solid transparent;
                    color: #FFFFFF;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);
                }
                QPushButton:hover, QToolButton:hover, QCommandLinkButton:hover {
                    color: #3d3d3d;
                }
                QPushButton:pressed, QToolButton:pressed, QCommandLinkButton:pressed {
                    color: #aeaeae;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);
                }
                QPushButton:disabled, QToolButton:disabled, QCommandLinkButton:disabled {
                    color: #616161;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #dce7eb, stop:0.5 #e0e8eb, stop:1 #dee7ec);
                }
                """)
                btn.setMinimumSize(230, 40)
                btn.setToolTip(f"{name} department")
                btn.setCursor(Qt.PointingHandCursor)
                font = QFont("Arial", 16)
                btn.setFont(font)
                btn.clicked.connect(lambda checked, d=id: self.showProducts(d))
                self.ui.departmentGridLayout.addWidget(btn)
        except Exception:
            pass

    def showProducts(self, department_id):
        # Clear existing product buttons
        for i in reversed(range(self.ui.productGridLayout.count())):
            widget = self.ui.productGridLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        try:
            self.cr.execute("SELECT id, name FROM products WHERE department_id = %s", (department_id,))
            self.products = self.cr.fetchall()
            if self.products:
                for index, (proId, proName) in enumerate(self.products):
                    if proName:  # Ensure product name is not empty
                        btn = QPushButton(proName)
                        btn.setMinimumSize(180, 45)
                        btn.setToolTip(f"{proName}")
                        btn.setCursor(Qt.PointingHandCursor)
                        font = QFont("Arial", 15)
                        btn.setFont(font)
                        self.proID.append(proId)
                        btn.clicked.connect(lambda checked, p=proId: self.on_button_click(p))
                        self.ui.productGridLayout.addWidget(btn, index // 3, index % 3)
            else:
                # Handle the case when no products are found
                pass  # No products to display, you can handle it as needed (e.g., show a message)
        except Exception as e:
            # Handle database connection or query execution errors
            pass  # You can log the error or handle it gracefully

    def manageDepartments(self):
        departments = self.get_departments()
        password, ok = QInputDialog.getText(self, "Password", "Type Password:", QLineEdit.Password)
        if password == "1234":
            choice, ok = QInputDialog.getItem(self, "Add or delete", "Select: ", ["Add", "Delete", "Update"], 0, False)
            if ok and choice:
                while choice == "Add":
                    departments = self.get_departments()
                    names = [name for id, name in departments]
                    textAdded, ok = QInputDialog.getText(self, "Add Department", "Enter department name:")
                    if textAdded and ok:
                        try:
                            if textAdded.strip() == "" or textAdded in names:
                                QMessageBox.warning(self, "Error", "This department already exists or the name is invalid.")
                            else:
                                self.cr.execute("INSERT INTO departments (name) VALUES (%s)", (textAdded,))
                                self.conn.commit()
                                self.showDepartments()
                                self.statusBar().showMessage(f"{textAdded} department was added...", 3000)
                        except Exception as e:
                            # معالجة الخطأ وإظهار رسالة مناسبة
                            self.conn.rollback()
                            QMessageBox.warning(self, "Error", f"Failed to add department: {str(e)}")
                    elif not ok:
                        break

                while choice == "Delete":
                    if departments:
                        names = [name for id, name in departments]
                        textDeleted, ok = QInputDialog.getItem(self, "Delete Department", "Departments: ", names, 0, False)
                        if textDeleted and ok:
                            try:
                                self.cr.execute("SELECT id FROM departments WHERE name = %s", (textDeleted,))
                                self.id_depdeleted = self.cr.fetchone()
                                idd=self.id_depdeleted[0]
                                #
                                self.cr.execute("SELECT name FROM products WHERE department_id = %s", (idd,))
                                self.prodeletedNames = self.cr.fetchall()
                                for n in self.prodeletedNames:
                                    self.cr.execute("DELETE FROM numberofunits WHERE PorName = %s", (n[0],))
                                    self.cr.execute("DELETE FROM Mnumberofunits WHERE PorName = %s", (n[0],))
                                    self.cr.execute("DELETE FROM Ynumberofunits WHERE PorName = %s", (n[0],))
                                #
                                self.cr.execute("DELETE FROM products WHERE department_id = %s", (idd,))
                                self.cr.execute("DELETE FROM departments WHERE name = %s", (textDeleted,))
                                self.conn.commit()
                                self.showDepartments()
                                self.statusBar().showMessage(f"{textDeleted} department was deleted...", 3000)
                            except Exception as e:
                                self.conn.rollback()
                                QMessageBox.warning(self, "Error", f"Failed to delete department: {str(e)}")
                        elif not ok:
                            break
                    else:
                        QMessageBox.warning(self, "Error", f"There is no departments to delete")  
                        break

                while choice == "Update":
                    departments = self.get_departments()
                    if departments:
                        names = [name for id, name in departments]
                        textUpCh, ok = QInputDialog.getItem(self, "Update Department", "Departments: ", names, 0, False)
                        if textUpCh and ok:
                            textUpdated, ok = QInputDialog.getText(self, "Update Department", "Enter department's new name:")
                            if textUpdated and ok:
                                if textUpdated.strip() == "" or textUpdated in names:
                                    QMessageBox.warning(self, "Error", "This department already exists or the name is invalid.")
                                else:
                                    try:
                                        self.cr.execute("UPDATE departments SET name = %s WHERE name = %s", (textUpdated, textUpCh))
                                        self.conn.commit()
                                        self.showDepartments()
                                        self.statusBar().showMessage(f"{textUpCh} was updated to {textUpdated}...", 3000)
                                    except Exception as e:
                                        self.conn.rollback()
                                        QMessageBox.warning(self, "Error", f"Failed to update department: {str(e)}")
                            elif not ok:
                                break
                        elif not ok:
                            break
                    else:
                        QMessageBox.warning(self, "Error", f"There is no departments to update")  
                        break
        else:
            self.statusBar().showMessage("ERROR: Wrong Password...", 3000)

    def manageProducts(self, department_id):
        password, ok = QInputDialog.getText(self, "Password", "Type Password:", QLineEdit.Password)
        departments = self.get_departments()
        if departments:
            if password == "0258":
                names = [name for id, name in departments]
                choisD, ok = QInputDialog.getItem(self, "Select Department", "Select department: ", names, 0, False)
                if choisD and ok:
                    self.cr.execute("SELECT id FROM departments WHERE name = %s", (choisD,))
                    department_record = self.cr.fetchone()
                    if not department_record:
                        QMessageBox.warning(self, "Error", "Selected department does not exist.")
                        return

                    choice, ok = QInputDialog.getItem(self, "Add , Delete or Update", "Select: ", ["Add", "Delete", "Update"], 0, False)
                    department_id = department_record[0]
                    # إضافة منتج
                    while ok and choice == "Add":
                        textAdded, ok = QInputDialog.getText(self, "Add Product", f"Enter Product name ( {choisD} ):")
                        if not textAdded or not ok:
                            break
                        products = self.get_products(department_id)
                        pronames = [name for id, name, *rest in products]
                        
                        if textAdded in pronames:
                            QMessageBox.warning(self, "Error", "This product already exists.")
                        else:
                            priceAdded, ok = QInputDialog.getText(self, "Add Product", f"Enter Product price ( {choisD} ):")
                            if not ok or not priceAdded:
                                break
                            try:
                                priceAdded = float(priceAdded)
                                self.cr.execute("INSERT INTO products (name, department_id, price) VALUES (%s, %s, %s)", (textAdded, department_id, priceAdded))
                                self.cr.execute("INSERT INTO numberOFUnits (PorName, date, NOU) VALUES (%s, %s, %s)", (textAdded, self.currentDate, 0))
                                self.cr.execute("INSERT INTO MnumberOFUnits (PorName, date, NOU) VALUES (%s, %s, %s)", (textAdded, self.currentDate, 0))
                                self.cr.execute("INSERT INTO YnumberOFUnits (PorName, date, NOU) VALUES (%s, %s, %s)", (textAdded, self.currentDate, 0))
                                self.conn.commit()
                                self.showProducts(department_id)
                                self.statusBar().showMessage(f"{textAdded} product was added...", 3000)
                            except ValueError:
                                QMessageBox.warning(self, "Error", "Please enter a valid price.")
                            except Exception as e:
                                self.conn.rollback()
                                QMessageBox.warning(self, "Error", f"Failed to add product: {str(e)}")

                    # حذف منتج
                    while ok and choice == "Delete":
                        products = self.get_products(department_id)
                        if products:
                            pronames = [name for id, name, *rest in products]
                            productDeleted, ok = QInputDialog.getItem(self, "Delete Product", f"Select product from {choisD}:", pronames, 0, False)
                            if not ok or not productDeleted:
                                break
                            try:
                                for prod_id, name, *rest in products:
                                    if name == productDeleted:
                                        self.cr.execute("DELETE FROM products WHERE id = %s", (prod_id,))
                                        self.cr.execute("DELETE FROM numberOFUnits WHERE PorName = %s", (productDeleted,))
                                        self.cr.execute("DELETE FROM MnumberOFUnits WHERE PorName = %s", (productDeleted,))
                                        self.cr.execute("DELETE FROM YnumberOFUnits WHERE PorName = %s", (productDeleted,))
                                        self.conn.commit()
                                        self.showProducts(department_id)
                                        self.statusBar().showMessage(f"{productDeleted} product was deleted...", 3000)
                                        break
                            except Exception as e:
                                self.conn.rollback()
                                QMessageBox.warning(self, "Error", f"Failed to delete product: {str(e)}")
                        else:
                            QMessageBox.warning(self, "Error", "No products found in this department.")
                            break

                    # تحديث منتج
                    while ok and choice == "Update":
                        products = self.get_products(department_id)
                        if products:
                            pronames = [name for id, name, *rest in products]
                            productToUpdate, ok = QInputDialog.getItem(self, "Update Product", f"Select product from {choisD}:", pronames, 0, False)
                            if not ok or not productToUpdate:
                                break
                            
                            for prod_id, name, *rest in products:
                                if name == productToUpdate:
                                    current_price = rest[0] if rest else ''
                                    new_name, ok_name = QInputDialog.getText(self, "Update Product Name", "Enter new product name:", text=name)
                                    new_price, ok_price = QInputDialog.getText(self, "Update Product Price", "Enter new product price:", text=str(current_price))
                                    if not new_name or not new_price:
                                        QMessageBox.warning(self, "Error", "Invalid entries.")
                                        break
                                    if new_name in pronames:
                                        QMessageBox.warning(self, "Error", "This product already exists.")
                                    else:
                                        try:
                                            f_price = float(new_price)
                                            self.cr.execute("UPDATE numberOFUnits SET PorName = %s WHERE PorName = %s", (new_name, productToUpdate))
                                            self.cr.execute("UPDATE MnumberOFUnits SET PorName = %s WHERE PorName = %s", (new_name, productToUpdate))
                                            self.cr.execute("UPDATE YnumberOFUnits SET PorName = %s WHERE PorName = %s", (new_name, productToUpdate))
                                            self.cr.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (new_name, f_price, prod_id))
                                            self.conn.commit()
                                            self.showProducts(department_id)
                                            self.statusBar().showMessage(f"{productToUpdate} product was updated to {new_name}...", 3000)
                                        except ValueError:
                                            QMessageBox.warning(self, "Error", "Please enter a valid price.")
                                        except Exception as e:
                                            self.conn.rollback()
                                            QMessageBox.warning(self, "Error", f"Failed to update product: {str(e)}")
                        else:
                            QMessageBox.warning(self, "Error", "No products found in this department.")
            else:
                self.statusBar().showMessage("ERROR: Wrong Password...", 3000)
        else:
            QMessageBox.warning(self, "Error", "There is no departments.")
    def get_departmentsTables(self):
        self.cr.execute("CREATE TABLE IF NOT EXISTS departmentsTables (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL)")
        self.conn.commit()
        self.cr.execute("SELECT id, name FROM departmentsTables")
        departments = self.cr.fetchall()
        return departments if departments else []  # التأكد من أن الاسترجاع يحتوي على نتائج

    def get_productsTables(self, department_id):
        self.cr.execute("CREATE TABLE IF NOT EXISTS productsTables (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,department_id INT)")
        self.conn.commit()
        self.cr.execute("SELECT id, name FROM productsTables WHERE department_id = %s", (department_id,))
        products = self.cr.fetchall()
        return products if products else []  # التأكد من وجود منتجات

    def showDepartmentsTables(self):
        for i in reversed(range(self.ui.departmentGridLayoutTables.count())):
            self.ui.departmentGridLayoutTables.itemAt(i).widget().setParent(None)
        
        self.cr.execute("SELECT id, name FROM departmentsTables")
        self.departments = self.cr.fetchall()

        if self.departments:  # التأكد من وجود أقسام
            for index, (id, name) in enumerate(self.departments):
                btn = QPushButton(name)
                btn.setStyleSheet("""
                QPushButton, QToolButton, QCommandLinkButton {
                    padding: 0 5px;
                    border-style: solid;
                    border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-right-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-bottom-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-left-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);
                    border-width: 2px;
                    border-radius: 8px;
                    color: #616161;
                    font-weight: bold;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #fbfdfd, stop:0.5 #ffffff, stop:1 #fbfdfd);
                }
                QPushButton::default, QToolButton::default, QCommandLinkButton::default {
                    border: 2px solid transparent;
                    color: #FFFFFF;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);
                }
                QPushButton:hover, QToolButton:hover, QCommandLinkButton:hover {
                    color: #3d3d3d;
                }
                QPushButton:pressed, QToolButton:pressed, QCommandLinkButton:pressed {
                    color: #aeaeae;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);
                }
                QPushButton:disabled, QToolButton:disabled, QCommandLinkButton:disabled {
                    color: #616161;
                    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #dce7eb, stop:0.5 #e0e8eb, stop:1 #dee7ec);
                }
                """)
                btn.setMinimumSize(230, 40)
                btn.setToolTip(f"{name} department")
                btn.setCursor(Qt.PointingHandCursor)
                font = QFont("Arial", 15)
                btn.setFont(font)
                btn.clicked.connect(lambda checked, d=id: self.showProductsTables(d))  
                self.ui.departmentGridLayoutTables.addWidget(btn)

    def showProductsTables(self, department_id):
        for i in reversed(range(self.ui.productGridLayoutTables.count())):
            self.ui.productGridLayoutTables.itemAt(i).widget().setParent(None)

        table_states = self.load_table_states()
        self.cr.execute("SELECT id, name FROM productsTables WHERE department_id = %s", (department_id,))
        self.products = self.cr.fetchall()

        if self.products:  # التأكد من وجود منتجات
            for index, (proId, proName) in enumerate(self.products):
                btn = QPushButton(proName)
                btn.setCheckable(True)
                btn.setToolTip(f"{proName}")
                btn.setCursor(Qt.PointingHandCursor)
                btn.setMinimumSize(180, 110)
                font = QFont("Arial", 16)
                btn.setFont(font)
                if table_states.get(proName, False):
                    btn.setChecked(True)
                    btn.setStyleSheet("background-color: red; color:white;")
                else:
                    btn.setChecked(False)
                    btn.setStyleSheet("""background-color: rgb(255,255,255);""")
                btn.clicked.connect(lambda clicked, p=proId, name=proName, b=btn: self.toggle_name_table(p, b, name))
                self.ui.productGridLayoutTables.addWidget(btn, index // 4, index % 4)

    def manageDepartmentsTables(self):
        departments = self.get_departmentsTables()
        password, ok = QInputDialog.getText(self, "Password", "Type Password:", QLineEdit.Password)
        if password == "1234":
            choice, ok = QInputDialog.getItem(self, "Add , delete or update", "Select: ", ["Add", "Delete", "Update"], 0, False)
            if ok and choice:
                while choice == "Add":
                    departments = self.get_departmentsTables()
                    names = [name for id, name in departments]
                    textAdded, ok = QInputDialog.getText(self, "Add Department", "Enter department name:")
                    if textAdded and ok:
                        try:
                            if textAdded in names:
                                QMessageBox.warning(self, "Error", "This department already exists.")
                            else:    
                                self.cr.execute("INSERT INTO departmentsTables (name) VALUES (%s)", (textAdded,))
                                self.conn.commit()
                                self.showDepartmentsTables()
                                self.statusBar().showMessage(f"{textAdded} department was added...", 3000)
                        except Exception as e:
                            QMessageBox.critical(self, "Error", f"Error adding department: {str(e)}")
                            self.conn.rollback()
                    elif not ok :
                        break    
                while choice == "Delete":
                    if departments:
                        names = [name for id, name in departments]
                        textDeleted, ok = QInputDialog.getItem(self, "Delete Department", "Departments: ", names, 0, False)
                        if textDeleted and ok:
                            try:
                                self.cr.execute("DELETE FROM departmentsTables WHERE name = %s", (textDeleted,))
                                self.conn.commit()
                                self.showDepartmentsTables()
                                self.statusBar().showMessage(f"{textDeleted} department was deleted...", 3000)
                            except Exception as e:
                                QMessageBox.critical(self, "Error", f"Error deleting department: {str(e)}")
                                self.conn.rollback()
                        elif not ok:
                            break        
                    else:
                        QMessageBox.warning(self, "Error", "There is no departments to delete.")
                        break
                        
                while choice == "Update":
                    departments = self.get_departmentsTables()
                    if departments:
                        names = [name for id, name in departments]
                        textUpCh, ok = QInputDialog.getItem(self, "Update Department", "Departments: ", names, 0, False)
                        if textUpCh and ok:
                            textUpdated, ok = QInputDialog.getText(self, "Update Department", "Enter department's new name:")
                            if textUpdated and ok:
                                if textUpdated in names:
                                    QMessageBox.warning(self, "Error", "This department name already exists.")
                                else:
                                    try:
                                        self.cr.execute("UPDATE departmentsTables SET name = %s WHERE name = %s", (textUpdated, textUpCh))
                                        self.conn.commit()
                                        self.showDepartmentsTables()
                                        self.statusBar().showMessage(f"{textUpCh} was updated to {textUpdated}...", 3000)
                                    except Exception as e:
                                        QMessageBox.critical(self, "Error", f"Error updating department: {str(e)}")
                                        self.conn.rollback()
                            elif not ok:
                                break
                        elif not ok:
                            break
                    else:
                        QMessageBox.warning(self, "Error", "There is no departments to update.")
                        break
        else:
            self.statusBar().showMessage("ERROR: Wrong Password...", 3000)

    def manageProductsTables(self, department_id):
        password, ok = QInputDialog.getText(self, "Password", "Type Password:", QLineEdit.Password)
        if password == "0258":
            departments = self.get_departmentsTables()
            if departments:
                names = [name for id, name in departments]
                choisD, ok = QInputDialog.getItem(self, "Select Department", "Select department: ", names, 0, False)
                if choisD and ok:
                    self.cr.execute("SELECT id FROM departmentsTables WHERE name = %s", (choisD,))
                    department_record = self.cr.fetchone()
                    if department_record:
                        department_id = department_record[0]
                        choice, ok = QInputDialog.getItem(self, "Add , delete or update", "Select: ", ["Add", "Delete", "Update"], 0, False)

                        # Adding a new table
                        while ok and choice == "Add":
                            textAdded, ok = QInputDialog.getText(self, "Add Table", f"Enter table name( {choisD} ):")
                            self.cr.execute("CREATE TABLE IF NOT EXISTS productsTables (id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(255) NOT NULL,department_id INT)")
                            self.conn.commit()
                            self.cr.execute("SELECT id, name FROM productsTables ")
                            products = self.cr.fetchall()
                            if products:
                                pronames = [name for id, name, *rest in products]
                                if textAdded and ok:
                                    if textAdded in pronames:
                                        QMessageBox.warning(self, "Error", "This table already exists.")
                                    else:
                                        try:
                                            self.cr.execute("INSERT INTO productsTables (name, department_id) VALUES (%s, %s)", (textAdded, department_id))
                                            self.conn.commit()
                                            self.showProductsTables(department_id)
                                            self.statusBar().showMessage(f"{textAdded} table was added...", 3000)
                                        except Exception as e:
                                            QMessageBox.critical(self, "Error", f"Error adding table: {str(e)}")
                                            self.conn.rollback()
                                else:
                                    QMessageBox.warning(self, "Error", "Please enter a valid table name.")
                                if not ok:
                                    break

                        # Deleting a table
                        while ok and choice == "Delete":
                            products = self.get_productsTables(department_id)
                            if products:
                                pronames = [name for id, name, *rest in products]
                                productDeleted, ok = QInputDialog.getItem(self, "Delete Table", f"Select table from {choisD}:", pronames, 0, False)
                                if productDeleted and ok:
                                    try:
                                        for prod_id, name, *rest in products:
                                            if name == productDeleted:
                                                self.cr.execute("DELETE FROM productsTables WHERE id = %s", (prod_id,))
                                                self.conn.commit()
                                                self.showProductsTables(department_id)
                                                self.statusBar().showMessage(f"{productDeleted} table was deleted...", 3000)
                                                break
                                    except Exception as e:
                                        QMessageBox.critical(self, "Error", f"Error deleting table: {str(e)}")
                                        self.conn.rollback()
                                if not ok:
                                    break
                            else:
                                QMessageBox.warning(self, "Error", "No tables found in this department.")
                                break

                        # Updating a table
                        while ok and choice == "Update":
                            products = self.get_productsTables(department_id)
                            if products:
                                pronames = [name for id, name, *rest in products]
                                productToUpdate, ok = QInputDialog.getItem(self, "Update Table", f"Select table from {choisD}:", pronames, 0, False)
                                if productToUpdate and ok:
                                    new_name, ok_name = QInputDialog.getText(self, "Update Table Name", "Enter new table name:", text=productToUpdate)
                                    if new_name in pronames:
                                        QMessageBox.warning(self, "Error", "This table name already exists.")
                                    else:
                                        try:
                                            if ok_name:
                                                for prod_id, name, *rest in products:
                                                    if name == productToUpdate:
                                                        self.cr.execute("UPDATE productsTables SET name = %s WHERE id = %s", (new_name, prod_id))
                                                        self.conn.commit()
                                                        self.showProductsTables(department_id)
                                                        self.statusBar().showMessage(f"{productToUpdate} table was updated to {new_name}...", 3000)
                                                        break
                                        except Exception as e:
                                            QMessageBox.critical(self, "Error", f"Error updating table: {str(e)}")
                                            self.conn.rollback()
                                    if not ok_name:
                                        break
                            else:
                                QMessageBox.warning(self, "Error", "No tables found in this department.")
                                break
            else:
                QMessageBox.warning(self, "Error", "No departments found.")
        else:
            self.statusBar().showMessage("ERROR: Wrong Password...", 3000)

    def toggle_table(self, tID, button):
        self.cr.execute("SELECT name FROM productsTables WHERE id = %s", (tID,))
        tableData = self.cr.fetchone()
        name = tableData[0]
        if button.isChecked():
            button.setStyleSheet("background-color: red; color:white;")  # Checked style
        else:
            button.setStyleSheet("background-color: rgb(255,255,255);")  # Default style
        self.save_table_states(name, button.isChecked())
    
    def save_table_states(self, name, is_checked):
        try:
            with open("table_states.json", "r") as f:
                states = json.load(f)
        except FileNotFoundError:
            states = {}
        states[name] = is_checked
        with open("table_states.json", "w") as f:
            json.dump(states, f)
    
    def load_table_states(self):
        try:
            with open("table_states.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def toggle_name_table(self,tID, button,name):
            self.toggle_table( tID, button)
            self.list_of_tables_name(name,button)
    
    def update_units(self, value):
        self.number_of_units = value
        self.ui.label_7.setText(str(self.number_of_units))
    def update_unitsUP(self):
        self.number_of_units += 1
        self.ui.label_7.setText(str(self.number_of_units))

    def update_unitsRow(self):
        if self.number_of_units >0:
            self.number_of_units -= 1
        self.ui.label_7.setText(str(self.number_of_units))

    def showInText(self, proID):
        try:
            if self.ui.tablesBtn.isChecked() or self.ui.deliveryBtn.isChecked() or self.ui.takeAwayBtn.isChecked():
                self.cr.execute("SELECT name, price FROM products WHERE id = %s", (proID,))
                productData = self.cr.fetchone()
                if productData:
                    name = productData[0]
                    price = productData[1]
                    self.total = float(price) * self.number_of_units
                    self.totalList.append(self.total)
                    self.orderedNames.append(name)
                    self.orderedPrices.append(price)
                    self.NOU.append(self.number_of_units)
                else:
                    return  # Exit if the product doesn't exist
            self.putProducts() 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Show in text Error: {str(e)}")


    def putProducts(self):
        # try:
            # Clear existing widgets
            for i in reversed(range(self.ui.showProsGridLayOut.count())):
                item = self.ui.showProsGridLayOut.itemAt(i)
                if item is not None and isinstance(item.layout(), QHBoxLayout):  # Check for QHBoxLayout
                    layout = item.layout()
                    for j in reversed(range(layout.count())):  # Clear the widgets in the QHBoxLayout
                        widget = layout.itemAt(j).widget()
                        if widget is not None:
                            widget.setParent(None)
                    self.ui.showProsGridLayOut.removeItem(item)  # Remove the QHBoxLayout from the parent layout

            if self.orderedNames:
                n = 0
                for index, name in enumerate(self.orderedNames):
                    namelabel = QLabel(f"{self.orderedNames[n]}")
                    namelabel.setStyleSheet('font-size: 15pt;')
                    namelabel.setMinimumHeight(50)
                    priceLabel = QLabel(f"{self.orderedPrices[n]}")
                    priceLabel.setStyleSheet('font-size: 15pt;')
                    totalLabel = QLabel(f"{self.totalList[n]}")
                    totalLabel.setStyleSheet('font-size: 15pt;')
                    numberOfunits = QTextEdit(f"{self.NOU[n]}")
                    numberOfunits.setStyleSheet('font-size: 12pt;')
                    numberOfunits.setMaximumHeight(30)
                    numberOfunits.setMaximumWidth(55)
                    deleteunit = QPushButton(f"-")  # إنشاء زر جديد لكل منتج
                    deleteunit.setStyleSheet('font-size: 12pt;')
                    deleteunit.setMinimumHeight(20)
                    deleteunit.setMinimumWidth(30)
                    deleteunit.setMaximumWidth(30)

                    n += 1

                    # Create a horizontal layout for each product
                    hLayout = QHBoxLayout()
                    hLayout.addWidget(totalLabel)
                    hLayout.addWidget(priceLabel)
                    hLayout.addWidget(namelabel)
                    hLayout.addWidget(numberOfunits)
                    hLayout.addWidget(deleteunit)

                    # ربط الزر بوظيفة getProductNameDetails وتمرير اسم المنتج
                    deleteunit.clicked.connect(lambda _, pname=name: self.deleteParticularPro(pname))

                    # Add the horizontal layout to the grid layout
                    row = index  # Use the index to set the row position
                    column = 0   # Starting column, can be adjusted if needed
                    self.ui.showProsGridLayOut.addLayout(hLayout, row, column)  # Add layout at specified position
                    
                # self.number_of_units = 0
                # self.ui.label_7.setText("0")
        # except Exception as e:
        #     QMessageBox.critical(self, "Error", f"Error while put products: {str(e)}")

    def deleteParticularPro(self, product_name):
        try:
            ind=self.orderedNames.index(product_name)
            self.orderedNames.pop(ind)
            self.NOU.pop(ind)
            self.orderedPrices.pop(ind)
            self.totalList.pop(ind)
            
            self.putProducts()
            self.showinTotalPrice()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error while delete last product: {str(e)}")

    def getTotalAfterUpdate(self):
        try:
            for i in range(self.ui.showProsGridLayOut.count()):
                item = self.ui.showProsGridLayOut.itemAt(i)
                
                if isinstance(item, QHBoxLayout):  # إذا كان العنصر تخطيط أفقي (QHBoxLayout)

                    for j in range(item.count()):
                        widget = item.itemAt(j).widget()

                        if isinstance(widget, QTextEdit):  # إذا كان العنصر QTextEdit
                            units_value = widget.toPlainText()  # الحصول على النص داخل الـ QTextEdit
                            self.updatedProNumOfUnits.append(int(units_value))
            if self.updatedProNumOfUnits:
                self.NOU=self.updatedProNumOfUnits 
                self.NOU.append(self.number_of_units)
                
                n=0
                lenName=len(self.orderedNames)
                funTotal=[]
                while n < lenName:
                    proTotal=(self.NOU[n])*(self.orderedPrices[n])
                    funTotal.append(float(proTotal))
                    n+=1
                self.totalList=funTotal
            self.showinTotalPrice()
            self.putProducts()
            self.updatedProNumOfUnits=[]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid entries: {str(e)}")

        
    def showinTotalPriceTables(self):
        self.valueAddedTax=float(self.ui.valueAddedTax.text().strip("%"))
        self.serviceTax=float(self.ui.serviceTax.text().strip("%"))
        self.discount=float(self.ui.discount.text().strip("%"))
        totalOrder=float(sum(self.totalList))
        self.totalPrice=totalOrder+self.serviceTax+(totalOrder*(self.valueAddedTax/100))-(totalOrder*(self.discount/100))
        rtp=round(self.totalPrice,3)
        self.ui.totalPrice.setText(f"{str(rtp)} E£")
        
    def showinTotalPriceTakeAway(self):
        self.valueAddedTax=float(self.ui.valueAddedTax.text().strip("%"))
        self.serviceTax=float(self.ui.serviceTax.text().strip("%"))
        self.discount=float(self.ui.discount.text().strip("%"))
        totalOrder=float(sum(self.totalList)) 
        self.totalPrice=totalOrder+(totalOrder*(self.valueAddedTax/100))-(totalOrder*(self.discount/100))
        rtp=round(self.totalPrice,3)
        self.ui.totalPrice.setText(f"{str(rtp)} E£")
        
    def showinTotalPriceDelivery(self):
        CCBT=self.ui.destinationCB.currentText()    
        if CCBT=="Choose destination":
            QMessageBox.warning(self, "No Selection", "Please select delivery destination.")
        else:
            self.cr.execute("SELECT amount FROM delivery WHERE name = %s", (CCBT,))    
            destAmount=self.cr.fetchone()
            if destAmount:   
                dA=float(destAmount[0])
                self.valueAddedTax=float(self.ui.valueAddedTax.text().strip("%"))
                self.discount=float(self.ui.discount.text().strip("%"))
                totalOrder=float(sum(self.totalList)) 
                self.totalPrice=totalOrder+dA+(totalOrder*(self.valueAddedTax/100))-(totalOrder*(self.discount/100))
                rtp=round(self.totalPrice,3)
                self.ui.totalPrice.setText(f"{str(rtp)} E£")

    def showinTotalPrice(self):
        if self.ui.tablesBtn.isChecked():
            self.showinTotalPriceTables()
        elif self.ui.deliveryBtn.isChecked():
            self.showinTotalPriceDelivery()
        elif self.ui.takeAwayBtn.isChecked():
            self.showinTotalPriceTakeAway()
        else:
             QMessageBox.warning(self, "No Selection", "Please select either 'Delivery' , 'Tables' or 'Take Away' before making an order.")
    
    def showinTotalPrice2(self):
        if self.ui.tablesBtn.isChecked():
            self.showinTotalPriceTables()
        elif self.ui.deliveryBtn.isChecked():
            self.showinTotalPriceDelivery()
        elif self.ui.takeAwayBtn.isChecked():
            self.showinTotalPriceTakeAway()

    def on_button_click(self, proID):
        self.getTotalAfterUpdate()
        self.showInText(proID)  
        self.showinTotalPrice2()

        
    def list_of_tables_name(self,name,button):
        if button.isChecked()==True:
            self.tablesNamelist.append(name)
        elif button.isChecked()==False:
            for n in self.tablesNamelist:
                if n==name:
                    ind=self.tablesNamelist.index(n)
                    del self.tablesNamelist[ind]

    def totalPayf1(self,val):
        self.totalPay1.append(val)
        if self.totalPay2=="":
            ftotal=self.totalPay2+"0"
            totalpayed=sum(self.totalPay1)+float(ftotal)
            if totalpayed>=self.totalPrice:
                rem=totalpayed-self.totalPrice
                rrem=round(rem,3)
                self.ui.remainToCl.setText(f"{str(rrem)} E£")
                self.ui.checkBox.setChecked(True)
        else:
            totalpayed=sum(self.totalPay1)+float(self.totalPay2)
            if totalpayed>=self.totalPrice:
                rem=totalpayed-self.totalPrice
                rrem=round(rem,3)
                self.ui.remainToCl.setText(f"{str(rrem)} E£")
                self.ui.checkBox.setChecked(True)

    def totalPayf2(self,val):
       self.totalPay2+=str(val)
       self.intTotalPay=float(self.totalPay2)+sum(self.totalPay1)
       if self.intTotalPay>=self.totalPrice:
           rem=self.intTotalPay-self.totalPrice
           rrem=round(rem,3)
           self.ui.remainToCl.setText(f"{str(rrem)} E£")
           self.ui.checkBox.setChecked(True)
    
    def create_invoice(self):
        try:
            from reportlab.pdfgen import canvas 
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from bidi.algorithm import get_display
            import arabic_reshaper 
            from reportlab.lib.pagesizes import A4

            ComName = self.ui.companyName.text()
            cashierName = self.ui.cashierName.text()
            tax = float(self.ui.valueAddedTax.text().strip("%"))
            serviceTax = float(self.ui.serviceTax.text())
            discount = float(self.ui.discount.text().strip("%"))
            total = ((self.ui.totalPrice.text()).strip("E£"))
            destination = self.ui.destinationCB.currentText()

            try:
                if destination != "Choose destination":
                    self.cr.execute("SELECT amount FROM delivery WHERE name = %s", (destination,))
                    amount = self.cr.fetchone()
                    delAmount = amount[0]
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

            pdfmetrics.registerFont(TTFont('Amiri','Amiri-Regular.ttf'))

            lenName = len(self.orderedNames)
            if self.ui.deliveryBtn.isChecked():
                page_hieght=155+(lenName*10)
            elif self.ui.tablesBtn.isChecked():
                page_hieght=145+(lenName*10)
            else:
                page_hieght=135+(lenName*10)
                    
            height=page_hieght-10
            invoiceFile=canvas.Canvas('myInvoice.pdf',pagesize=(80,page_hieght))

            ComNtext=str(ComName)
            resherped_ComNtext=arabic_reshaper.reshape(ComNtext)
            bidi_ComNtext=get_display(resherped_ComNtext)
            invoiceFile.setFont("Amiri",8)
            invoiceFile.drawString(20,height,bidi_ComNtext)

            height-=15

            chtext=f"الكاشير : {cashierName}"
            resherped_casher=arabic_reshaper.reshape(chtext)
            bidi_casher=get_display(resherped_casher)
            invoiceFile.setFont("Amiri",5)
            invoiceFile.drawString(25,height,bidi_casher)

            height-=10
            
            now = datetime.now() 
            self.formatted_now = now.strftime("%Y-%m-%d | %H:%M:%S")        
                
            dateAtime=f"التاريخ : {str(self.formatted_now)}"
            resherped_dateAtime=arabic_reshaper.reshape(dateAtime)
            bidi_dateAtime=get_display(resherped_dateAtime)
            invoiceFile.drawString(13,height,bidi_dateAtime)
            
            if self.ui.deliveryBtn.isChecked():            
                height-=10
                
                dateAtime=f"الوجهة : {destination}"
                resherped_dateAtime=arabic_reshaper.reshape(dateAtime)
                bidi_dateAtime=get_display(resherped_dateAtime)
                invoiceFile.drawString(38,height,bidi_dateAtime)
                        
            height-=5
            invoiceFile.setLineWidth(.5)
            invoiceFile.line(5,height ,75,height )
            height-=15
            invoiceFile.setLineWidth(.3)
            invoiceFile.rect(3,height,75,10 )
            height+=5
            ############
            invoiceFile.setFont("Amiri",5)
            sanf="الصنف"
            resherped_sanf=arabic_reshaper.reshape(sanf)
            bidi_sanf=get_display(resherped_sanf)
            invoiceFile.drawString(46,height,bidi_sanf)

            si3r="السعر"
            resherped_si3r=arabic_reshaper.reshape(si3r)
            bidi_si3r=get_display(resherped_si3r)
            invoiceFile.drawString(25,height,bidi_si3r)

            el3dad="العدد"
            resherped_3dad=arabic_reshaper.reshape(el3dad)
            bidi_el3dad=get_display(resherped_3dad)
            invoiceFile.drawString(68,height,bidi_el3dad)

            egmali="الإجمالي"
            resherped_egmali=arabic_reshaper.reshape(egmali)
            bidi_egmali=get_display(resherped_egmali)
            invoiceFile.drawString(4,height,bidi_egmali)

            height-=12

            totalL=[]
            lenName = len(self.orderedNames)
            ln = 0
            while ln < lenName:
                name = self.orderedNames[ln]
                units =(self.NOU[ln])
                price =(self.orderedPrices[ln])
                total_price =(self.totalList[ln])

                invoiceFile.setFont("Amiri",4)
                proName=str(name)
                resherped_proName=arabic_reshaper.reshape(proName)
                bidi_proName=get_display(resherped_proName)
                invoiceFile.drawString(43,height,bidi_proName)
                
                proNunits=str(units)
                resherped_proNunits=arabic_reshaper.reshape(proNunits)
                bidi_proNunits=get_display(resherped_proNunits)
                invoiceFile.drawString(72,height,bidi_proNunits)
                
                proPrice=str(price)
                resherped_proPrice=arabic_reshaper.reshape(proPrice)
                bidi_proPrice=get_display(resherped_proPrice)
                invoiceFile.drawString(25,height,bidi_proPrice)
                
                prototal_price=str(total_price)
                resherped_prototal_price=arabic_reshaper.reshape(prototal_price)
                bidi_prototal_price=get_display(resherped_prototal_price)
                invoiceFile.drawString(4,height,bidi_prototal_price)

                        #         name = name[:18] + "..." if len(name) > 18 else name
                ln+=1
                height-=10
                totalL.append(float(total_price))
            
            invoiceFile.setFont("Amiri",5)
            totalPs=f"المجموع : {str(sum(totalL))}"
            resherped_totalPs=arabic_reshaper.reshape(totalPs)
            bidi_totalPs=get_display(resherped_totalPs)
            invoiceFile.drawString(43,height,bidi_totalPs)

            height-=4
            invoiceFile.setLineWidth(.3)
            invoiceFile.line(5,height ,75,height)
            #################
            TtL=sum(totalL)
            if self.ui.tablesBtn.isChecked():
                if tax != 0:
                    height-=10 
                    ttax=round(((tax/100)*TtL),2)                   
                    addedTax=f"الضريبة (%{tax}): {ttax}"
                    resherped_addedTax=arabic_reshaper.reshape(addedTax)
                    bidi_addedTax=get_display(resherped_addedTax)
                    invoiceFile.drawString(36,height,bidi_addedTax)
                    
                if serviceTax != 0:
                    height-=10                                        
                    serveceTAX=f"ضريبة الخدمة : {serviceTax}"
                    resherped_serveceTAX=arabic_reshaper.reshape(serveceTAX)
                    bidi_serveceTAX=get_display(resherped_serveceTAX)
                    invoiceFile.drawString(43,height,bidi_serveceTAX)
                                        
                if discount != 0:
                    height-=10 
                    tdiscount=round(((discount/100)*TtL),2)  
                    serveceTAX=f"الخصم (%{discount}): ( {tdiscount} )"
                    resherped_serveceTAX=arabic_reshaper.reshape(serveceTAX)
                    bidi_serveceTAX=get_display(resherped_serveceTAX)
                    invoiceFile.drawString(29,height,bidi_serveceTAX)
                                                                                  
            elif self.ui.deliveryBtn.isChecked():
                if tax != 0:
                    height-=10  
                    ttax=round(((tax/100)*TtL),2)                   
                    addedTax=f"الضريبة (%{tax}): {ttax}"
                    resherped_addedTax=arabic_reshaper.reshape(addedTax)
                    bidi_addedTax=get_display(resherped_addedTax)
                    invoiceFile.drawString(36,height,bidi_addedTax)
                    
                if delAmount != 0:
                    height-=10                    
                    deliveryTax=f"خدمة توصيل : {delAmount}"
                    resherped_deliveryTax=arabic_reshaper.reshape(deliveryTax)
                    bidi_deliveryTax=get_display(resherped_deliveryTax)
                    invoiceFile.drawString(43,height,bidi_deliveryTax)
                    
                if discount != 0:
                    height-=10  
                    tdiscount=round(((discount/100)*TtL),2)  
                    serveceTAX=f"الخصم (%{discount}): ( {tdiscount} )"
                    resherped_serveceTAX=arabic_reshaper.reshape(serveceTAX)
                    bidi_serveceTAX=get_display(resherped_serveceTAX)
                    invoiceFile.drawString(29,height,bidi_serveceTAX)
                    
            elif self.ui.takeAwayBtn.isChecked():
                if tax != 0:
                    height-=10
                    ttax=round(((tax/100)*TtL),2)                   
                    addedTax=f"الضريبة (%{tax}): {ttax}"
                    resherped_addedTax=arabic_reshaper.reshape(addedTax)
                    bidi_addedTax=get_display(resherped_addedTax)
                    invoiceFile.drawString(36,height,bidi_addedTax)
                    
                if discount != 0:
                    height-=10  
                    tdiscount=round(((discount/100)*TtL),2)  
                    serveceTAX=f"الخصم (%{discount}): ( {tdiscount} )"
                    resherped_serveceTAX=arabic_reshaper.reshape(serveceTAX)
                    bidi_serveceTAX=get_display(resherped_serveceTAX)
                    invoiceFile.drawString(29,height,bidi_serveceTAX)
            height-=10          
            invoiceFile.setLineWidth(.3)
            invoiceFile.line(5,height ,75,height)

            height-=13 
            
            invoiceFile.setLineWidth(.3)
            invoiceFile.rect(34,height,41,10 )
            height+=5  
            
            invoiceFile.setFont("Amiri",5)
            rtotal=round(float(total),2)
            Ftotal=f"الإجمالي : {rtotal}"
            resherped_Ftotal=arabic_reshaper.reshape(Ftotal)
            bidi_Ftotal=get_display(resherped_Ftotal)
            invoiceFile.drawString(35,height,bidi_Ftotal)

            height-=10
            
            invoiceFile.line(5,height ,75,height )

            height-=6

            invoiceFile.setFont("Amiri",5)
            invoiceFile.drawString(18,height,"Fast Account program")
            height-=6
            invoiceFile.drawString(10,height,"Developed by : Marwan Ashraf")
            height-=6
            invoiceFile.drawString(23,height,"01007258086")


            invoiceFile.showPage()
            invoiceFile.save()           
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def issueBill(self): 
        try:
            self.deleteDMYtables()
            if self.ui.payCashBtn.isChecked():
                destination = self.ui.destinationCB.currentText()
                if destination == "Choose destination" and self.ui.deliveryBtn.isChecked():
                    QMessageBox.warning(self, "No Selection", "Please select delivery destination before making an order.")  
                else:      
                    self.cr.execute("CREATE TABLE IF NOT EXISTS revenues (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
                    if self.ui.totalPrice.text().strip("E£") != "":
                        tp=float(self.ui.totalPrice.text().strip("E£"))
                        self.cr.execute("INSERT INTO revenues (revName, revenue_date, amount) VALUES (%s, %s ,%s)",('مبيعات كاشير', self.currentDate, tp))
                        self.cr.execute("INSERT INTO newShift (revName, salesCash , date) VALUES ( %s ,%s ,%s)",('CashierRevenueCash', tp, self.currentDate))
                        lens=len(self.orderedNames)
                        name=self.orderedNames
                        s=0
                        while s < lens:
                            self.cr.execute("SELECT NOU FROM numberOFUnits WHERE PorName = %s", (name[s],))
                            cur_NOU=self.cr.fetchone()
                            new_NOU=(cur_NOU[0] + self.NOU[s]) if cur_NOU and len(cur_NOU) > 0 else self.NOU[s]
                            self.cr.execute("SELECT NOU FROM MnumberOFUnits WHERE PorName = %s", (name[s],))
                            Mcur_NOU=self.cr.fetchone()
                            Mnew_NOU=(Mcur_NOU[0] + self.NOU[s]) if Mcur_NOU and len(Mcur_NOU) > 0 else self.NOU[s]
                            self.cr.execute("SELECT NOU FROM YnumberOFUnits WHERE PorName = %s", (name[s],))
                            Ycur_NOU=self.cr.fetchone()
                            Ynew_NOU=(Ycur_NOU[0] + self.NOU[s]) if Ycur_NOU and len(Ycur_NOU) > 0 else self.NOU[s]
                            self.cr.execute("UPDATE numberOFUnits SET NOU = %s WHERE PorName = %s", (new_NOU, name[s]))
                            self.cr.execute("UPDATE MnumberOFUnits SET NOU = %s WHERE PorName = %s", (Mnew_NOU, name[s]))
                            self.cr.execute("UPDATE YnumberOFUnits SET NOU = %s WHERE PorName = %s", (Ynew_NOU, name[s]))
                            self.cr.execute("SELECT price FROM products WHERE name = %s", (name[s],))
                            oname=self.cr.fetchone()
                            self.orderedPrices.append(oname[0] if oname and len(oname) > 0 else 0)
                            s+=1
                        
                        
                        self.create_invoice()  
                        
                        self.clearCashierData()                        
                        self.putProducts()
            elif self.ui.payVisaBtn.isChecked():
                destination = self.ui.destinationCB.currentText()
                if destination == "Choose destination" and self.ui.deliveryBtn.isChecked():
                    QMessageBox.warning(self, "No Selection", "Please select delivery destination before making an order.")    
                else:                
                    self.cr.execute("CREATE TABLE IF NOT EXISTS revenuesVisa (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL)")
                    if self.ui.totalPrice.text().strip("E£") != "":
                        tp=float(self.ui.totalPrice.text().strip("E£"))
                        self.cr.execute("INSERT INTO revenuesVisa (revName, revenue_date, amount) VALUES (%s, %s ,%s)",('مبيعات كاشير فيزا', self.currentDate, tp))
                        self.cr.execute("INSERT INTO newShift (revName, VisaCash , date) VALUES ( %s ,%s ,%s)",('CashierRevenueVisa', tp, self.currentDate))
                        lens=len(self.orderedNames)
                        name=self.orderedNames
                        s=0
                        while s < lens:
                            self.cr.execute("SELECT NOU FROM numberOFUnits WHERE PorName = %s", (name[s],))
                            cur_NOU=self.cr.fetchone()
                            new_NOU=(cur_NOU[0] + self.NOU[s]) if cur_NOU and len(cur_NOU) > 0 else self.NOU[s]
                            self.cr.execute("SELECT NOU FROM MnumberOFUnits WHERE PorName = %s", (name[s],))
                            Mcur_NOU=self.cr.fetchone()
                            Mnew_NOU=(Mcur_NOU[0] + self.NOU[s]) if Mcur_NOU and len(Mcur_NOU) > 0 else self.NOU[s]
                            self.cr.execute("SELECT NOU FROM YnumberOFUnits WHERE PorName = %s", (name[s],))
                            Ycur_NOU=self.cr.fetchone()
                            Ynew_NOU=(Ycur_NOU[0] + self.NOU[s]) if Ycur_NOU and len(Ycur_NOU) > 0 else self.NOU[s]
                            self.cr.execute("UPDATE numberOFUnits SET NOU = %s WHERE PorName = %s", (new_NOU, name[s]))
                            self.cr.execute("UPDATE MnumberOFUnits SET NOU = %s WHERE PorName = %s", (Mnew_NOU, name[s]))
                            self.cr.execute("UPDATE YnumberOFUnits SET NOU = %s WHERE PorName = %s", (Ynew_NOU, name[s]))
                            self.cr.execute("SELECT price FROM products WHERE name = %s", (name[s],))
                            oname=self.cr.fetchone()
                            self.orderedPrices.append(oname[0] if oname and len(oname) > 0 else 0)
                            s+=1
                            
                        self.create_invoice()   

                        self.clearCashierData()                        

                        self.putProducts()
            else:
                QMessageBox.warning(self, "No Selection", "Please select either 'Cash' or 'Visa' before making an order.")    
            self.conn.commit()       
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error while issue bill {e}.")

    def clearCashierData(self):
        self.ui.remainToCl.setText(f"0 E£")
        self.ui.totalPrice.setText(f"0 E£")
        self.totalPrice=0
        self.totalPay2=""
        self.totalPay1=[]
        self.orderedNames=[]
        self.NOU=[]
        self.orderedPrices=[]
        self.totalList=[]
        self.ui.checkBox.setChecked(False)
        self.putProducts()
    
    def update_tax(self,checked):
        if checked:
            password, ok = QInputDialog.getText(self, "Password", "Type Password:", QLineEdit.Password)
            if password == "0147":
                self.ui.valueAddedTax.setReadOnly(False)
                self.ui.serviceTax.setReadOnly(False)
                self.ui.discount.setReadOnly(False)
        else:
            try:
                valueAddedTax=float(self.ui.valueAddedTax.text().strip("%"))
                serviceTax=float(self.ui.serviceTax.text().strip("%"))
                discount=float(self.ui.discount.text().strip("%"))
                self.cr.execute("UPDATE taxes SET amount= %s  WHERE name=%s",(valueAddedTax,'valueAddedTax'))
                self.cr.execute("UPDATE taxes SET amount= %s  WHERE name=%s",(serviceTax,'serviceTax'))
                self.cr.execute("UPDATE taxes SET amount= %s  WHERE name=%s",(discount,'discount'))
                self.conn.commit()
                self.ui.valueAddedTax.setReadOnly(True)
                self.ui.serviceTax.setReadOnly(True)
                self.ui.discount.setReadOnly(True)
            except:
                QMessageBox.warning(self, "Error", "Invalid entries.")
    
    def deleveryCB(self):
        self.cr.execute("SELECT name FROM delivery ")
        names=self.cr.fetchall()
        for name in names:
            self.ui.destinationCB.addItem(name[0])
    
    ############################################################ record management ##########################################################
    def search_delivery(self):
        delSearched = self.ui.searchDelivery.text().strip()
        if not delSearched:
            self.ui.deliveryPlace.setText("")
            self.ui.deliveryAmount.setText("")
            self.statusBar().showMessage("Please enter a delivery name.", 3000)
            return
        try:
            self.cr.execute("SELECT name, amount FROM delivery WHERE name = %s", (delSearched,))
            delName = self.cr.fetchone()
            if delName:
                name, amount = delName
                self.ui.deliveryPlace.setText(name)
                self.ui.deliveryAmount.setText(str(amount))
            else:
                self.ui.deliveryPlace.setText("")
                self.ui.deliveryAmount.setText("")
                self.statusBar().showMessage(f"'{delSearched}' does not exist...", 3000)
        except Exception as e:
            self.ui.deliveryPlace.setText("")
            self.ui.deliveryAmount.setText("")
            self.statusBar().showMessage(f"Error occurred: {str(e)}", 3000)

    def add_delivery(self):
        try:
            self.cr.execute("CREATE TABLE IF NOT EXISTS delivery (name VARCHAR(255) NOT NULL, amount DECIMAL(11, 2) NOT NULL)")
            try:
                delPlace = self.ui.deliveryPlace.text().strip()
                delAmount = float(self.ui.deliveryAmount.text().strip())
            except:
                QMessageBox.warning(self, "Error", "Invalid entries.")
                

            delAmount = float(delAmount)
            
            self.cr.execute("SELECT name FROM delivery WHERE name = %s", (delPlace,))
            existing = self.cr.fetchone()
            
            if existing:
                QMessageBox.warning(self, "Error", "This name already exists.")
            else:
                self.cr.execute("INSERT INTO delivery (name, amount) VALUES (%s, %s)", (delPlace, delAmount))
                self.conn.commit()
                self.statusBar().showMessage(f"{delPlace} was added with an amount of {delAmount} E£...", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")


    def delete_delivery(self):
        try:
            delPlace = self.ui.deliveryPlace.text().strip()
            
            if not delPlace:
                QMessageBox.warning(self, "Error", "Please enter a delivery name to delete.")
                return

            self.cr.execute("DELETE FROM delivery WHERE name = %s", (delPlace,))
            if self.cr.rowcount > 0:
                self.conn.commit()
                self.statusBar().showMessage(f"'{delPlace}' was deleted...", 3000)
                self.ui.deliveryPlace.setText("")
                self.ui.deliveryAmount.setText("")
            else:
                QMessageBox.warning(self, "Error", f"No delivery found with the name '{delPlace}'.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")   

    def addExpensesAndRev(self):
        # Create tables if they do not exist
        self.cr.execute("CREATE TABLE IF NOT EXISTS expenses (expName TEXT ,expense_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
        self.cr.execute("CREATE TABLE IF NOT EXISTS revenues (revName TEXT, revenue_date DATE NOT NULL, amount DECIMAL(11, 2) NOT NULL)")

        # Handle Expenses
        acTypsOfExp = self.ui.AccTypesOfExp.currentText()
        expAmount = self.ui.expAmount.text().strip()
        expName = self.ui.normTypesOfExp.text().strip()
        
        if self.validate_expense(acTypsOfExp, expAmount, expName):
            self.insert_expense(acTypsOfExp, expAmount, expName)

        # Handle Revenues
        acTypsOfRev = self.ui.AccTypesOfRevenues.currentText()
        revAmount = self.ui.RevenueAmount.text().strip()
        revName = self.ui.normTypesOfRevenues.text().strip()

        if self.validate_revenue(acTypsOfRev, revAmount, revName):
            self.insert_revenue(acTypsOfRev, revAmount, revName)

        self.conn.commit()

    def validate_expense(self, acTypsOfExp, expAmount, expName):
        if acTypsOfExp == "None" and expAmount == "" and expName == "":
            return False
        if acTypsOfExp != "None" and expAmount != "" and expName != "":
            QMessageBox.warning(self, "ERROR", "You must write one type of expense.")
            return False
        if acTypsOfExp == "None" and expAmount != "" and expName == "":
            QMessageBox.warning(self, "ERROR", "You must write the type of expense.")
            return False
        if expAmount == "" and acTypsOfExp != "None" and expName != "":
            QMessageBox.warning(self, "ERROR", "You must type the amount of expense.")
            return False
        return True

    def insert_expense(self, acTypsOfExp, expAmount, expName):
        try:
            intExpAmount = float(expAmount)
            if acTypsOfExp != "None":
                name_to_insert = acTypsOfExp
            else:
                name_to_insert = expName

            self.cr.execute("INSERT INTO expenses (expName, expense_date, amount) VALUES (%s, %s, %s)", 
                            (name_to_insert, self.currentDate, intExpAmount))
            self.cr.execute("INSERT INTO newShift (expName, expenses, date) VALUES (%s, %s, %s)", 
                            (name_to_insert, intExpAmount, self.currentDate))
            self.statusBar().showMessage(f"The expenses have been increased by {intExpAmount}", 3000)
            self.ui.expAmount.setText("")
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid entries for the expense amount.")

    def validate_revenue(self, acTypsOfRev, revAmount, revName):
        if acTypsOfRev == "None" and revAmount == "" and revName == "":
            return False
        if acTypsOfRev != "None" and revAmount != "" and revName != "":
            QMessageBox.warning(self, "ERROR", "You must write one type of revenue.")
            return False
        if acTypsOfRev == "None" and revAmount != "" and revName == "":
            QMessageBox.warning(self, "ERROR", "You must write the type of revenue.")
            return False
        if revAmount == "" and acTypsOfRev != "None" and revName != "":
            QMessageBox.warning(self, "ERROR", "You must type the amount of revenue.")
            return False
        return True

    def insert_revenue(self, acTypsOfRev, revAmount, revName):
        try:
            intRevAmount = float(revAmount)
            if acTypsOfRev != "None":
                name_to_insert = acTypsOfRev
            else:
                name_to_insert = revName

            self.cr.execute("INSERT INTO revenues (revName, revenue_date, amount) VALUES (%s, %s, %s)", 
                            (name_to_insert, self.currentDate, intRevAmount))
            self.cr.execute("INSERT INTO newShift (revName, revenues, date) VALUES (%s, %s, %s)", 
                            (name_to_insert, intRevAmount, self.currentDate))
            self.statusBar().showMessage(f"The revenues have been increased by {intRevAmount}", 3000)
            self.ui.RevenueAmount.setText("")
        except ValueError:
            QMessageBox.warning(self, "ERROR", "Invalid entries for the revenue amount.")    
    ############################################################ employment management ##########################################################
    def searchEmployee(self):
        self.deleteDMYtables()
        self.cr.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, adress TEXT, mSalary DECIMAL(11, 2) NOT NULL, id INT AUTO_INCREMENT PRIMARY KEY, phnNmbr TEXT, nmbrOabsnts INTEGER, DOwork TEXT , DOabsence TEXT, DOpresent TEXT)  ")
        self.currentday=int(datetime.now().strftime('%d'))
        self.currentmonth=int(datetime.now().strftime('%m'))
        self.currentyear=int(datetime.now().strftime('%Y'))
        self.days_in_month=calendar.monthrange(self.currentyear,self.currentmonth)[1]
        if self.ui.comboBoxEmpSrch.currentText()=="Search With":
            self.statusBar().showMessage("You must choose what you want to search with...",3000)
        elif self.ui.comboBoxEmpSrch.currentText()=="Name":
            try:
                name=self.ui.textExpSrch.text().strip().title()
                self.cr.execute(f"SELECT nmbrOabsnts, DOwork FROM employees WHERE name='{name}'")
                result=self.cr.fetchone()
                if result:
                    self.numberofabsences=result[0]
                    self.frstDateOfWrk=result[1]
                    if self.frstDateOfWrk:
                        self.frstDayOfWrk=self.frstDateOfWrk[8:]
                        self.frstmnthYearOfWrk=self.frstDateOfWrk[:7]
                        self.currentDate=datetime.now().strftime('%Y-%m-%d')
                        self.currentmonthYear=datetime.now().strftime('%Y-%m')
                        self.currentDay=datetime.now().strftime('%d')
                        self.daysofwordpayaple=int(self.currentDay)-int(self.numberofabsences)
                        self.cr.execute(f"SELECT * FROM employees WHERE name='{name}'")
                        self.allEmpData=self.cr.fetchall()
                        if self.allEmpData:
                            self.Ename=self.allEmpData[0][0]
                            self.Eadress=self.allEmpData[0][1]
                            self.Esalary=self.allEmpData[0][2]
                            self.Eid=self.allEmpData[0][3]
                            self.Ephnnmbr=self.allEmpData[0][4]
                            self.EnmbrAbsnc=self.allEmpData[0][5]
                            self.EstrtWrk=self.allEmpData[0][6]
                            self.updateUI()
                            self.calculatePayable()
                        else:
                            self.clearUI()
                            self.statusBar().showMessage("This name does not exist...",3000)
                else:
                    self.clearUI()
                    self.statusBar().showMessage("This name does not exist...",3000)
            except:
                self.clearUI()
                self.statusBar().showMessage("An error occurred...",3000)
        elif self.ui.comboBoxEmpSrch.currentText()=="ID":
            try:
                emp_id=self.ui.textExpSrch.text().strip()
                self.cr.execute(f"SELECT nmbrOabsnts, DOwork FROM employees WHERE id='{emp_id}'")
                result=self.cr.fetchone()
                if result:
                    self.numberofabsences=result[0]
                    self.frstDateOfWrk=result[1]
                    if self.frstDateOfWrk:
                        self.frstDayOfWrk=self.frstDateOfWrk[8:]
                        self.frstmnthYearOfWrk=self.frstDateOfWrk[:7]
                        self.currentDate=datetime.now().strftime('%Y-%m-%d')
                        self.currentmonthYear=datetime.now().strftime('%Y-%m')
                        self.currentDay=datetime.now().strftime('%d')
                        self.daysofwordpayaple=int(self.currentDay)-int(self.numberofabsences)
                        self.cr.execute(f"SELECT * FROM employees WHERE id='{emp_id}'")
                        self.allEmpData=self.cr.fetchall()
                        if self.allEmpData:
                            self.Ename=self.allEmpData[0][0]
                            self.Eadress=self.allEmpData[0][1]
                            self.Esalary=self.allEmpData[0][2]
                            self.Eid=self.allEmpData[0][3]
                            self.Ephnnmbr=self.allEmpData[0][4]
                            self.EnmbrAbsnc=self.allEmpData[0][5]
                            self.EstrtWrk=self.allEmpData[0][6]
                            self.updateUI()
                            self.calculatePayable()
                        else:
                            self.clearUI()
                            self.statusBar().showMessage("This ID does not exist...",3000)
                else:
                    self.clearUI()
                    self.statusBar().showMessage("This ID does not exist...",3000)
            except:
                self.clearUI()
                self.statusBar().showMessage("An error occurred...",3000)

    def calculatePayable(self):
        if self.frstmnthYearOfWrk != self.currentmonthYear:
            self.Epyable=self.calculatePayableForPreviousMonth()
        else:
            self.Epyable=self.calculatePayableForCurrentMonth()
        self.roundedEpyable=round(self.Epyable,2)
        self.ui.empPayable.setText(f"{self.roundedEpyable:,} E£")

    def calculatePayableForPreviousMonth(self):
        self.cr.execute(f"SELECT bonus FROM bonusOrDeduct WHERE empID='{int(self.ui.empId.text().strip())}'")
        self.curBonus=self.cr.fetchall()
        self.cr.execute(f"SELECT deduction FROM bonusOrDeduct WHERE empID='{int(self.ui.empId.text().strip())}'")
        self.curdeduction=self.cr.fetchall()
        if self.curdeduction:
            bonus=self.curBonus[0][0]
            deduct=self.curdeduction[0][0]
        else:
            bonus=0
            deduct=0
        if self.days_in_month==30:
            return (self.Esalary/30*self.daysofwordpayaple)+bonus-deduct
        elif self.days_in_month==31:
            return (self.Esalary/31*self.daysofwordpayaple)+bonus-deduct
        elif self.days_in_month==28:
            return (self.Esalary/28*self.daysofwordpayaple)+bonus-deduct
        elif self.days_in_month==29:
            return (self.Esalary/29*self.daysofwordpayaple)+bonus-deduct

    def calculatePayableForCurrentMonth(self):
        self.cr.execute(f"SELECT bonus FROM bonusOrDeduct WHERE empID='{int(self.ui.empId.text().strip())}'")
        self.curBonus=self.cr.fetchall()
        self.cr.execute(f"SELECT deduction FROM bonusOrDeduct WHERE empID='{int(self.ui.empId.text().strip())}'")
        self.curdeduction=self.cr.fetchall()
        if self.curdeduction:
            bonus=self.curBonus[0][0]
            deduct=self.curdeduction[0][0]
        else:
            bonus=0
            deduct=0
        dailyPayable=self.Esalary/self.days_in_month
        currentDayPlusOne=int(self.currentDay)+1
        daysOfWork=currentDayPlusOne-int(self.frstDayOfWrk)-int(self.numberofabsences)
        return (daysOfWork*dailyPayable)+bonus-deduct

    def updateUI(self):
        self.ui.empName.setText(f"{self.Ename}")
        self.ui.empAdress.setText(f"{self.Eadress}")
        self.ui.empMsalary.setText(f"{self.Esalary} E£")
        self.ui.empDateWrk.setText(f"{self.EstrtWrk}")
        self.ui.empId.setText(f"{self.Eid}")
        self.ui.empPhnNmbr.setText(f"{self.Ephnnmbr}")
        self.ui.empNmbrAbsncs.setText(f"{self.EnmbrAbsnc}")
        

    def clearUI(self):
        self.ui.empName.setText("")
        self.ui.empAdress.setText("")
        self.ui.empMsalary.setText("")
        self.ui.empDateWrk.setText("")
        self.ui.empId.setText("")
        self.ui.empPhnNmbr.setText("")
        self.ui.empNmbrAbsncs.setText("")
        self.ui.empPayable.setText("")
        
    def addBonusOrDeduct(self):
        try:
            if self.ui.bonusRadioButton.isChecked():
                if self.ui.bonusOrDeductionAmount!="" :
                    if self.ui.empId.text().strip() !="":
                        self.cr.execute("CREATE TABLE IF NOT EXISTS bonusOrDeduct (empID INTEGER NOT NULL , bonus DECIMAL(11, 2) NOT NULL DEFAULT 0, deduction DECIMAL(11, 2) NOT NULL DEFAULT 0, payable DECIMAL(11, 2) NOT NULL DEFAULT 0,date DATE NOT NULL )")
                        self.cr.execute(f"SELECT bonus FROM bonusOrDeduct WHERE empID='{int(self.ui.empId.text().strip())}'")
                        self.curBonus=self.cr.fetchall()
                        newBonus=float(self.ui.bonusOrDeductionAmount.text())
                        if self.curBonus:
                            updatedBonus=newBonus+float(self.curBonus[0][0])
                            self.cr.execute("UPDATE bonusOrDeduct SET bonus=%s ,date=%s WHERE empID=%s  ",(updatedBonus,self.currentDate,int(self.ui.empId.text().strip())))
                            self.ui.bonusOrDeductionAmount.setText("")
                            self.statusBar().showMessage("The bonus has been added...",3000)
                        else:
                            self.cr.execute("INSERT INTO bonusOrDeduct(bonus,date ,empID) VALUES (%s,%s,%s)  ",(newBonus,self.currentDate,int(self.ui.empId.text().strip())))                    
                            self.ui.bonusOrDeductionAmount.setText("")
                            self.statusBar().showMessage("The bonus has been added...",3000)
                else:
                    QMessageBox.warning(self, "Error", "Invalid entries")    
            elif self.ui.deductionRadioButton.isChecked():
                if self.ui.bonusOrDeductionAmount!="" :
                    if self.ui.empId.text().strip() !="":
                        self.cr.execute("CREATE TABLE IF NOT EXISTS bonusOrDeduct (empID INTEGER NOT NULL , bonus DECIMAL(11, 2) NOT NULL DEFAULT 0, deduction DECIMAL(11, 2) NOT NULL DEFAULT 0, payable DECIMAL(11, 2) NOT NULL DEFAULT 0,date DATE NOT NULL )")
                        self.cr.execute(f"SELECT deduction FROM bonusOrDeduct WHERE empID='{int(self.ui.empId.text().strip())}'")
                        self.curdeduction=self.cr.fetchall()
                        newdeduction=float(self.ui.bonusOrDeductionAmount.text())
                        if self.curdeduction:
                            updateddeduction=newdeduction+float(self.curdeduction[0][0])
                            self.cr.execute("UPDATE bonusOrDeduct SET deduction=%s ,date=%s WHERE empID=%s  ",(updateddeduction,self.currentDate,int(self.ui.empId.text().strip())))
                            self.ui.bonusOrDeductionAmount.setText("")
                            self.statusBar().showMessage("The deduction has been added...",3000)
                        else:
                            self.cr.execute("INSERT INTO bonusOrDeduct(deduction,date ,empID) VALUES (%s,%s,%s)  ",(newdeduction,self.currentDate,int(self.ui.empId.text().strip())))                    
                            self.ui.bonusOrDeductionAmount.setText("")
                            self.statusBar().showMessage("The deduction has been added...",3000)
            self.conn.commit()     
        except Exception as e :
            QMessageBox.warning(self, "Error", f"Invalid entries:{e}")
    def EmployeeAbsences(self):
        self.cr.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, adress TEXT, mSalary DECIMAL(11, 2) NOT NULL, id INT AUTO_INCREMENT PRIMARY KEY, phnNmbr TEXT, nmbrOabsnts INTEGER, DOwork TEXT , DOabsence TEXT, DOpresent TEXT)  ")
        try:    
            self.cr.execute(f"SELECT name, DOabsence FROM employees") 
            self.allEmpNamesAbsence=self.cr.fetchall()
            if self.allEmpNamesAbsence:
                self.currentmonthh=datetime.now().strftime('%m')
                if self.ui.comboBoxEmpSrch.currentText()=="Name":
                    for emp in self.allEmpNamesAbsence:
                        name,absences=emp
                        if absences[5:7] != self.currentmonthh:
                            self.cr.execute(f"UPDATE employees SET nmbrOabsnts=0 WHERE name='{name}'")
                    self.cr.execute(f"SELECT DOwork FROM employees WHERE name='{self.ui.textExpSrch.text().strip().title()}' ") 
                    self.frstDateOfWrk=self.cr.fetchone()
                    self.cr.execute(f"SELECT DOpresent FROM employees WHERE name='{self.ui.textExpSrch.text().strip().title()}' ") 
                    self.dateOfPresent=self.cr.fetchone()
                    self.cr.execute(f"SELECT DOabsence FROM employees WHERE name='{self.ui.textExpSrch.text().strip().title()}' ") 
                    self.dateOfLastAbsence=self.cr.fetchone()
                    self.currentDate=datetime.now().strftime('%Y-%m-%d')
                    self.cr.execute(f"SELECT nmbrOabsnts FROM employees WHERE name='{self.ui.textExpSrch.text().strip().title()}' ") 
                    self.numberofabsences=self.cr.fetchone()
                    if self.frstDateOfWrk and self.dateOfPresent and self.dateOfLastAbsence and self.numberofabsences:
                        self.newNumberOfAbsences=self.numberofabsences[0]+1
                        self.numberOpresents=self.numberofabsences[0]-1

                        if self.ui.radioAbsent.isChecked()==True:
                            if str(self.dateOfLastAbsence[0])!=self.currentDate:
                                self.cr.execute(f"UPDATE employees SET nmbrOabsnts={self.newNumberOfAbsences} WHERE name='{self.ui.textExpSrch.text().strip().title()}' ")
                                self.statusBar().showMessage("The employee's absence has been saved...",3000)
                                self.cr.execute(f"UPDATE employees SET DOabsence={self.currentDate} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                            elif str(self.frstDateOfWrk[0])==self.currentDate:
                                self.statusBar().showMessage("The employee can't be absent on the first day of his work...",3000)
                            else:
                                self.statusBar().showMessage("The employee's absence has been saved before...",3000)
                        elif self.ui.radioPresent.isChecked()==True:
                            if str(self.dateOfLastAbsence[0])!=self.currentDate:
                                pass
                            elif str(self.dateOfLastAbsence[0])==self.currentDate:
                                if str(self.frstDateOfWrk[0])!=self.currentDate:
                                    if str(self.dateOfPresent[0])!=self.currentDate:
                                        self.cr.execute(f"UPDATE employees SET nmbrOabsnts={self.numberOpresents} WHERE name='{self.ui.textExpSrch.text().strip().title()}' ")
                                        self.cr.execute(f"UPDATE employees SET DOpresent={self.currentDate} WHERE name='{self.ui.textExpSrch.text().strip().title()}' ")
                                        self.statusBar().showMessage("The employee's presence has been saved...",3000)
                                    else:
                                        self.statusBar().showMessage("The employee's presence has been saved before...",3000)
                                else:
                                    self.statusBar().showMessage("The employee can't be absent on the first day of his work...",3000)
                        else:
                            self.statusBar().showMessage("You must choose present or absent...",3000)
        except:
            self.statusBar().showMessage("This name does not exist...",3000)
        try:
            if self.ui.comboBoxEmpSrch.currentText()=="ID":
                if self.allEmpNamesAbsence:
                    for emp in self.allEmpNamesAbsence:
                        name,absences=emp
                        if absences[5:7] != self.currentmonthh:
                            self.cr.execute(f"UPDATE employees SET nmbrOabsnts=0 WHERE name='{name}'")

                    self.cr.execute(f"SELECT DOwork FROM employees WHERE id='{self.ui.textExpSrch.text().strip()}' ") 
                    self.frstDateOfWrk=self.cr.fetchone()
                    self.cr.execute(f"SELECT DOpresent FROM employees WHERE id='{self.ui.textExpSrch.text().strip()}' ") 
                    self.dateOfPresent=self.cr.fetchone()
                    self.cr.execute(f"SELECT DOabsence FROM employees WHERE id='{self.ui.textExpSrch.text().strip()}' ") 
                    self.dateOfLastAbsence=self.cr.fetchone()
                    self.currentDate=datetime.now().strftime('%Y-%m-%d')
                    self.cr.execute(f"SELECT nmbrOabsnts FROM employees WHERE id='{self.ui.textExpSrch.text().strip()}' ") 
                    self.numberofabsences=self.cr.fetchone()
                    if self.frstDateOfWrk and self.dateOfPresent and self.dateOfLastAbsence and self.numberofabsences:
                        self.newNumberOfAbsences=self.numberofabsences[0]+1
                        self.numberOpresents=self.numberofabsences[0]-1
                        if self.ui.radioAbsent.isChecked()==True:
                            if str(self.dateOfLastAbsence[0])!=self.currentDate:
                                self.cr.execute(f"UPDATE employees SET nmbrOabsnts={self.newNumberOfAbsences} WHERE id='{self.ui.textExpSrch.text().strip()}' ")
                                self.statusBar().showMessage("The employee's absence has been saved...",3000)
                                self.cr.execute(f"UPDATE employees SET DOabsence='{self.currentDate}' WHERE id='{self.ui.textExpSrch.text().strip()}'")
                            elif str(self.frstDateOfWrk[0])==self.currentDate:
                                self.statusBar().showMessage("The employee can't be absent on the first day of his work...",3000)
                            else:
                                self.statusBar().showMessage("The employee's absence has been saved before...",3000)
                        elif self.ui.radioPresent.isChecked()==True:
                            if str(self.dateOfLastAbsence[0])!=self.currentDate:
                                pass
                            elif str(self.dateOfLastAbsence[0])==self.currentDate:
                                if str(self.frstDateOfWrk[0])!=self.currentDate:
                                    if str(self.dateOfPresent[0])!=self.currentDate:
                                        self.cr.execute(f"UPDATE employees SET nmbrOabsnts={self.numberOpresents} WHERE id='{self.ui.textExpSrch.text().strip()}' ")
                                        self.cr.execute(f"UPDATE employees SET DOpresent='{self.currentDate}' WHERE id='{self.ui.textExpSrch.text().strip()}' ")
                                        self.statusBar().showMessage("The employee's presence has been saved...",3000)
                                    else:
                                        self.statusBar().showMessage("The employee's presence has been saved before...",3000)
                                else:
                                    self.statusBar().showMessage("The employee can't be absent on the first day of his work...",3000)
                        else:
                            self.statusBar().showMessage("You must choose present or absent...",3000)
        except:
            self.statusBar().showMessage("This id does not exist...",3000)
        self.conn.commit()

    def addEmployee(self):
        self.cr.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, adress TEXT, mSalary DECIMAL(11, 2) NOT NULL, id INT AUTO_INCREMENT PRIMARY KEY, phnNmbr TEXT, nmbrOabsnts INTEGER, DOwork TEXT , DOabsence TEXT, DOpresent TEXT) ")
        self.empName=self.ui.empName.text().strip().title()
        self.empAdress=self.ui.empAdress.toPlainText().title().strip()
        self.empMsalary=self.ui.empMsalary.text().strip()
        self.empPhnNmbr=self.ui.empPhnNmbr.text().strip()
        self.currentDate=datetime.now().strftime('%Y-%m-%d')
        self.cr.execute(f"SELECT name FROM employees") 
        self.allEmpNames=self.cr.fetchall()
        self.cr.execute(f"SELECT phnNmbr FROM employees") 
        self.allEmpPhnNumbers=self.cr.fetchall()
        try:
            if self.allEmpNames ==[]:
                self.cr.execute(f"INSERT INTO employees(name, adress,mSalary,phnNmbr, nmbrOabsnts, DOwork, DOabsence, DOpresent) VALUES ('{self.empName}','{self.empAdress}',{float(self.empMsalary)},'{(self.empPhnNmbr)}',0,'{self.currentDate}','{self.currentDate}','{self.currentDate}')")
                self.statusBar().showMessage("The employee has been added...",3000)
            else:
                for name in self.allEmpNames:
                    if self.empName == name[0]:
                        self.EmloyeeName=True
                        break
                    else:
                        self.EmloyeeName=False    
                #
                for number in self.allEmpPhnNumbers:
                    if (self.empPhnNmbr) == number[0]:
                        self.EmployeePhoneNumber=True
                        break
                    else:
                        self.EmployeePhoneNumber=False
                #            
                if self.empName=='':
                    self.statusBar().showMessage("You must add employee's name...",3000)
                elif self.empMsalary=="":
                    self.statusBar().showMessage("You must add employee's monthly salary...",3000)
                elif self.empAdress=="":
                    self.statusBar().showMessage("You must add employee's adress...",3000)
                elif self.empPhnNmbr=="":
                    self.statusBar().showMessage("You must add employee's phone number...",3000)
                elif self.EmloyeeName==True:
                    self.statusBar().showMessage("This name is already exist...",3000)
                elif self.EmployeePhoneNumber==True:
                    self.statusBar().showMessage("This phone number is already exist...",3000)
                #
                else:
                    self.cr.execute("""
                        INSERT INTO employees (
                            name, adress, mSalary,  phnNmbr, nmbrOabsnts, DOwork, DOabsence, DOpresent
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (self.empName, self.empAdress, float(self.empMsalary),self.empPhnNmbr,0,self.currentDate,self.currentDate,self.currentDate ))
                    self.statusBar().showMessage("The employee has been added...",3000)
        except:
            self.statusBar().showMessage("ERROR : Invalid entries...",3000)     
        #
        self.conn.commit()

    def clearData(self):
        self.ui.empName.setText("")
        self.ui.empAdress.setText("")
        self.ui.empMsalary.setText("")
        self.ui.empDateWrk.setText("")
        self.ui.empId.setText("")
        self.ui.empPhnNmbr.setText("")
        self.ui.empNmbrAbsncs.setText("")
        self.ui.empPayable.setText("")
        self.ui.textExpSrch.setText("")

    def updateEmployeeData(self):      
        self.empName=self.ui.empName.text().strip().title()
        self.empAdress=self.ui.empAdress.toPlainText().title().strip()
        self.empMsalary=self.ui.empMsalary.text().strip()
        self.empPhnNmbr=self.ui.empPhnNmbr.text().strip()
        self.empId=(self.ui.empId.text().strip())
        self.empDateOfStrtWrk=self.ui.empDateWrk.text()
        self.empNmbrOfAbcences=self.ui.empNmbrAbsncs.text()
        #
        self.updatedSalary=self.empMsalary[:-2]
        #
        if self.ui.comboBoxEmpSrch.currentText()=="Search with":
           self.statusBar().showMessage("You must choose what you want to search with...",3000)
        # try:
        if self.ui.comboBoxEmpSrch.currentText()=="Name":
            self.cr.execute(f"SELECT * FROM employees WHERE name='{self.ui.textExpSrch.text().strip().title()}' ") 
            self.allEmpData=self.cr.fetchall()
            if self.allEmpData:
            #
                self.Ename=self.allEmpData[0][0]
                self.Eadress=self.allEmpData[0][1]
                self.Esalary=self.allEmpData[0][2]
                self.Eid=self.allEmpData[0][3]
                self.Ephnnmbr=self.allEmpData[0][4]
                self.EnmbrAbsnc=self.allEmpData[0][5]
                self.EstrtWrk=self.allEmpData[0][6]
                self.EDabsence=self.allEmpData[0][7]
                self.EDpresent=self.allEmpData[0][8]
                #
                self.cr.execute(f"SELECT name FROM employees") 
                self.allEmpNames=self.cr.fetchall()
                self.cr.execute(f"SELECT id FROM employees") 
                self.allEmpIDs=self.cr.fetchall()
                self.cr.execute(f"SELECT phnNmbr FROM employees") 
                self.allEmpPhnNumbers=self.cr.fetchall()
                #
                for name in self.allEmpNames:
                    if self.empName == name[0]:
                        self.EmloyeeName=True
                        break
                    else:
                        self.EmloyeeName=False    
                #
                for id in self.allEmpIDs:
                    if int(self.empId) == int(id[0]):
                        self.EmployeeID=True
                        break
                    elif int(self.empId) != int(id[0]):
                        self.EmployeeID=False                
                #    
                for number in self.allEmpPhnNumbers:
                    if (self.empPhnNmbr) == number[0]:
                        self.EmployeePhoneNumber=True
                        break
                    else:
                        self.EmployeePhoneNumber=False
                #            
                if self.EmloyeeName==True and self.EmployeePhoneNumber==True and self.EmployeeID==True:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
                #
                elif self.EmloyeeName==False and self.EmployeeID==True and self.EmployeePhoneNumber==True:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
                #
                elif self.EmloyeeName==True and self.EmployeeID==False and self.EmployeePhoneNumber==True:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
                #
                elif self.EmloyeeName==True and self.EmployeeID==True and self.EmployeePhoneNumber==False:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
                #
                elif self.EmloyeeName==False and self.EmployeeID==False and self.EmployeePhoneNumber==True:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
                #
                elif self.EmloyeeName==False and self.EmployeeID==True and self.EmployeePhoneNumber==False:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
                #
                elif self.EmloyeeName==True and self.EmployeeID==False and self.EmployeePhoneNumber==False:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
                #
                elif self.EmloyeeName==False and self.EmployeeID==False and self.EmployeePhoneNumber==False:
                    self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE name='{self.ui.textExpSrch.text().strip().title()}'")
                    self.statusBar().showMessage("Employee's data has been updated...",3000)
        # except:
        #    self.statusBar().showMessage("Employee's name does not exist...",3000) 

        try:    
            if self.ui.comboBoxEmpSrch.currentText()=="ID":
                self.cr.execute(f"SELECT * FROM employees WHERE id='{self.ui.textExpSrch.text().strip().title()}' ") 
                self.allEmpData=self.cr.fetchall()
                if self.allEmpData:
                #
                    self.Ename=self.allEmpData[0][0]
                    self.Eadress=self.allEmpData[0][1]
                    self.Esalary=self.allEmpData[0][2]
                    self.Eid=self.allEmpData[0][3]
                    self.Ephnnmbr=self.allEmpData[0][4]
                    self.EnmbrAbsnc=self.allEmpData[0][5]
                    self.EstrtWrk=self.allEmpData[0][6]
                    self.EDabsence=self.allEmpData[0][7]
                    self.EDpresent=self.allEmpData[0][8]
                    #
                    self.cr.execute(f"SELECT name FROM employees") 
                    self.allEmpNames=self.cr.fetchall()
                    self.cr.execute(f"SELECT id FROM employees") 
                    self.allEmpIDs=self.cr.fetchall()
                    self.cr.execute(f"SELECT phnNmbr FROM employees") 
                    self.allEmpPhnNumbers=self.cr.fetchall()
                    #
                    for name in self.allEmpNames:
                        if self.empName == name[0]:
                            self.EmloyeeName=True
                            break
                        else:
                            self.EmloyeeName=False    
                    #
                    for id in self.allEmpIDs:
                        if int(self.empId) == int(id[0]):
                            self.EmployeeID=True
                            break
                        elif int(self.empId) != int(id[0]):
                            self.EmployeeID=False                
                    #    
                    for number in self.allEmpPhnNumbers:
                        if (self.empPhnNmbr) == number[0]:
                            self.EmployeePhoneNumber=True
                            break
                        else:
                            self.EmployeePhoneNumber=False
                    #            
                    if self.EmloyeeName==True and self.EmployeePhoneNumber==True and self.EmployeeID==True:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
                    #
                    elif self.EmloyeeName==False and self.EmployeeID==True and self.EmployeePhoneNumber==True:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
                    #
                    elif self.EmloyeeName==True and self.EmployeeID==False and self.EmployeePhoneNumber==True:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
                    #
                    elif self.EmloyeeName==True and self.EmployeeID==True and self.EmployeePhoneNumber==False:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
                    #
                    elif self.EmloyeeName==False and self.EmployeeID==False and self.EmployeePhoneNumber==True:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
                    #
                    elif self.EmloyeeName==False and self.EmployeeID==True and self.EmployeePhoneNumber==False:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
                    #
                    elif self.EmloyeeName==True and self.EmployeeID==False and self.EmployeePhoneNumber==False:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
                    #
                    elif self.EmloyeeName==False and self.EmployeeID==False and self.EmployeePhoneNumber==False:
                        self.cr.execute(f"UPDATE employees SET adress='{self.empAdress}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET mSalary={float(self.updatedSalary)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET phnNmbr='{(self.empPhnNmbr)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET id={int(self.empId)} WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.cr.execute(f"UPDATE employees SET name='{(self.empName)}' WHERE id='{self.ui.textExpSrch.text().strip().title()}'")
                        self.statusBar().showMessage("Employee's data has been updated...",3000)
        except:
           self.statusBar().showMessage("Employee's id does not exist...",3000) 

        self.conn.commit()

    def layEmployeeOFF(self):
        try:   
            self.EName=self.ui.empName.text().strip().title()
            if self.EName=="":
                pass
            else:
                self.cr.execute(f"DELETE FROM employees WHERE name = '{self.EName}'")
                self.conn.commit()
                self.ui.empName.setText("")
                self.ui.empAdress.setText("")
                self.ui.empMsalary.setText("")
                self.ui.empDateWrk.setText("")
                self.ui.empId.setText("")
                self.ui.empPhnNmbr.setText("")
                self.ui.empNmbrAbsncs.setText("")
                self.ui.empPayable.setText("")

                self.statusBar().showMessage("This employee has been layed off ...",3000)
        except:
           self.statusBar().showMessage("This name does not exist ...",3000)      
        
    def fetch_and_show_employees(self):
        self.deleteDMYtables()        
        try:
            
            self.cr.execute("SELECT name, DOabsence FROM employees")
            self.allEmpNamesAbsence = self.cr.fetchall()
            self.currentmonthh = datetime.now().strftime('%m')
            for emp in self.allEmpNamesAbsence:
                if emp[1]:  # تحقق من وجود تاريخ الغياب
                    name, dateAbsences = emp
                    if dateAbsences[5:7] != self.currentmonthh:
                        self.cr.execute("UPDATE employees SET nmbrOabsnts=0 WHERE name=%s", (name,))
            self.cr.execute("SELECT name, id, mSalary, nmbrOabsnts FROM employees")
            employees = self.cr.fetchall()
            if not employees:  # تحقق مما إذا كانت قائمة الموظفين فارغة
                self.ui.empLastMslry.setHtml("<p>لا توجد بيانات موظفين.</p>")
                return
            emp_data = ""
            for emp in employees:
                name, emp_id, salary, numOFAbsnc = emp
                self.cr.execute(f"SELECT bonus FROM bonusOrDeduct WHERE empID={emp_id}")
                self.curBonus=self.cr.fetchall()
                self.cr.execute(f"SELECT deduction FROM bonusOrDeduct WHERE empID={emp_id}")
                self.curdeduction=self.cr.fetchall()
                if self.curdeduction:
                    bonus=self.curBonus[0][0]
                    deduct=self.curdeduction[0][0]
                else:
                    bonus=0
                    deduct=0
                    
                self.currentmonth = int(datetime.now().strftime('%m'))
                self.currentyear = int(datetime.now().strftime('%Y'))
                self.currentday = int(datetime.now().strftime('%d'))
                self.days_in_month = calendar.monthrange(self.currentyear, self.currentmonth)[1]
                self.cr.execute("SELECT DOwork FROM employees WHERE name=%s", (name,))
                self.frstDateOfWrk = self.cr.fetchone()
                if self.frstDateOfWrk:  # تحقق من وجود تاريخ العمل
                    self.frstDayOfWrk = self.frstDateOfWrk[0][8:]
                    self.frstmnthYearOfWrk = self.frstDateOfWrk[0][:7]
                    self.currentmonthYear = datetime.now().strftime('%Y-%m')
                    if self.frstmnthYearOfWrk != self.currentmonthYear:
                        daysOfWork = self.currentday
                    else:
                        daysOfWork = self.currentday - int(self.frstDayOfWrk) + 1
                    payable = ((salary / self.days_in_month) * (daysOfWork - numOFAbsnc))
                    roundedpyable = (round(payable, 2))+bonus-deduct
                    emp_data += f"""
                        <p style="text-align: left;">
                            &nbsp;&nbsp;الإسم: {name}<br>
                            &nbsp;&nbsp;رقم(ID): {emp_id}<br>
                            &nbsp;&nbsp;المرتب: {salary}<br>
                            &nbsp;&nbsp;عدد مرات الغياب: {numOFAbsnc}<br>
                            &nbsp;&nbsp;الحافز: {bonus:,} E£<br>
                            &nbsp;&nbsp;الخصم: {deduct:,} E£<br>
                            &nbsp;&nbsp;المبلغ المستحق: {roundedpyable:,} E£
                        </p>
                        <p style="text-align: right;">{"-" * 40}</p>
                    """
            self.ui.empLastMslry.setHtml(emp_data)
        except mysql.connector.Error as err:
            self.ui.empLastMslry.setPlainText(f"Error fetching employee data: {err}")
        self.conn.commit()
    ############################################################ show management ##########################################################
    def showDailyRev(self):
        try:
            selected_date = self.ui.dateEditRev.date()  
            formatted_date = selected_date.toString("yyyy-MM-dd")  
            
            self.cr.execute("CREATE TABLE IF NOT EXISTS revenues (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
            self.cr.execute("CREATE TABLE IF NOT EXISTS revenuesVisa (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
            self.cr.execute("SELECT * FROM revenues WHERE revenue_date = %s", (formatted_date,))
            current_day_revenues= self.cr.fetchall()
            self.cr.execute("SELECT * FROM revenuesVisa WHERE revenue_date = %s", (formatted_date,))
            current_day_revenuesVisa= self.cr.fetchall()
            alRevs=[]
            revenuesText=""
            if current_day_revenues:
                for a in current_day_revenues:
                    name , date , amount = a
                    alRevs.append(amount)
                    revenuesText+=f"{date}           {amount:.2f}           {name} \n\n"
            if current_day_revenuesVisa:
                for a in current_day_revenuesVisa:
                    name , date , amount = a
                    alRevs.append(amount)
                    revenuesText+=f"{date}           {amount:.2f}           {name} \n\n"
            self.ui.showRevLbl.setText(revenuesText)
            self.ui.revAmountText.setText(f"{sum(alRevs)} E£")
            if not current_day_revenues and not current_day_revenuesVisa:
                self.ui.showRevLbl.setText(f"لا يوجد إيرادات مسجلة في تاريخ : {formatted_date}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def showExpenses(self):
        try:
            self.cr.execute("CREATE TABLE IF NOT EXISTS expenses (expName TEXT ,expense_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
            expense_text = ""
            alExps=[]
            selected_date = self.ui.dateEdit.date()  
            formatted_date = selected_date.toString("yyyy-MM-dd")  
            self.cr.execute("SELECT * FROM expenses WHERE expense_date = %s", (formatted_date,))
            expensesDate = self.cr.fetchall()
            if expensesDate:
                for n in expensesDate:
                    name, date, amount = n
                    expense_text += f"{date}           {amount:.2f}           {name} \n\n"
                    alExps.append(amount)
            self.ui.showExpLbl.setText(expense_text)
            self.ui.expAmountText.setText(f"{sum(alExps)} E£")
            if not expensesDate:
                self.ui.showExpLbl.setText(f"لا يوجد مصروفات مسجلة في تاريخ : {formatted_date}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def deleteDMYtables(self):
        # Fetch the last dates from each table
        self.cr.execute("SELECT date FROM numberOFUnits")
        Ddate = self.cr.fetchall()  
        self.cr.execute("SELECT date FROM MnumberOFUnits")
        Mdate = self.cr.fetchall()  
        self.cr.execute("SELECT date FROM YnumberOFUnits")
        Ydate = self.cr.fetchall()  

        # Initialize last date variables
        last_day, last_month, last_year = None, None, None

        # Get last day, month, and year if available
        if Ddate:
            last_day = int(str(Ddate[0][0])[8:])
        if Mdate:
            last_month = int(str(Mdate[0][0])[5:7])
        if Ydate:
            last_year = int(str(Ydate[0][0])[:4])

        # Current date components
        intCurDay = int(self.currentDay)
        intCurMonth = int(self.currentMonth)
        intCurYear = int(self.currentYear)

        # Update day table if the day has changed
        if last_day is not None and last_day != intCurDay:
            self.cr.execute("SELECT PorName FROM numberOFUnits")
            names = self.cr.fetchall()
            for n in names:
                self.cr.execute("UPDATE numberOFUnits SET NOU = %s, date = %s WHERE PorName = %s", (0, self.currentDate, n[0]))

        # Update month table if the month has changed
        if last_month is not None and last_month != intCurMonth:
            self.cr.execute("SELECT PorName FROM MnumberOFUnits")
            names = self.cr.fetchall()
            for n in names:
                self.cr.execute("UPDATE MnumberOFUnits SET NOU = %s, date = %s WHERE PorName = %s", (0, self.currentDate, n[0]))

        # Update year table if the year has changed
        if last_year is not None and last_year != intCurYear:
            self.cr.execute("SELECT PorName FROM YnumberOFUnits")
            names = self.cr.fetchall()
            for n in names:
                self.cr.execute("UPDATE YnumberOFUnits SET NOU = %s, date = %s WHERE PorName = %s", (0, self.currentDate, n[0]))

        self.cr.execute("CREATE TABLE IF NOT EXISTS bonusOrDeduct (empID INTEGER NOT NULL , bonus DECIMAL(11, 2) NOT NULL DEFAULT 0, deduction DECIMAL(11, 2) NOT NULL DEFAULT 0, payable DECIMAL(11, 2) NOT NULL DEFAULT 0,date DATE NOT NULL )")
        self.cr.execute(f"SELECT date FROM bonusOrDeduct ")
        self.date=self.cr.fetchall()
        self.cr.execute(f"SELECT bonus FROM bonusOrDeduct ")
        self.Bonus=self.cr.fetchall()
        self.cr.execute(f"SELECT deduction FROM bonusOrDeduct ")
        self.deduct=self.cr.fetchall()
        self.cr.execute(f"SELECT empID FROM bonusOrDeduct ")
        self.empID=self.cr.fetchall()
        if self.empID:
            last_month_emp = int(str(self.date[0][0])[5:7])
            if last_month_emp is not None and last_month_emp != intCurMonth:
                for i in self.empID:
                    self.cr.execute("UPDATE bonusOrDeduct SET bonus = %s ,deduction=%s , date = %s WHERE empID = %s", (0 ,0 , self.currentDate, i[0]))

        # Commit the changes to the database
        self.conn.commit()

    def printDailyUnits(self):
        self.deleteDMYtables()
        self.ui.stackedWidget.setCurrentIndex(8)
        self.cr.execute("SELECT porName , NOU FROM numberofunits ")
        dailyUnits = self.cr.fetchall()
        if dailyUnits:
            compName=self.ui.companyName.text()
            content= f"""
            <p style="font-family:'Arial'; font-size:30px; text-align:center; color:black;">
                <strong>{compName}</strong>
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
                ----------------------------------------------
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
                عدد الوحدات المباعة في يوم<br>
                {self.currentDate}<br>
            </p>"""
            for nn in dailyUnits:
                name,number = nn          
                content+=f"""
                <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                    &nbsp;{name}  :  {number}<br>
                    ------------------------------------
                </p>"""

            self.ui.dailysalesText.setHtml(content)

    def printMonthlyUnits(self):
        self.deleteDMYtables()
        self.ui.stackedWidget.setCurrentIndex(9)
        current_date = datetime.strptime(self.currentDate, "%Y-%m-%d")
        old_datemonth = current_date - relativedelta(months=1)
        old_datemonth_only_date = old_datemonth.date()
        self.cr.execute("SELECT porName , NOU FROM mnumberofunits ")
        dailyUnits = self.cr.fetchall()
        if dailyUnits:
            compName=self.ui.companyName.text()
            content= f"""
            <p style="font-family:'Arial'; font-size:30px; text-align:center; color:black;">
                <strong>{compName}</strong>
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
                ----------------------------------------------
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
                عدد الوحدات المباعة لشهر<br>
                {self.currentDate[:7]}<br>
            </p>"""
            for nn in dailyUnits:
                name,number = nn          
                content+=f"""
                <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                    &nbsp;{name}  :  {number}<br>
                    ------------------------------------
                </p>"""

            self.ui.monthlySalestext.setHtml(content)

    def printYearlyUnits(self):
        self.deleteDMYtables()
        self.ui.stackedWidget.setCurrentIndex(10) 
        current_date = datetime.strptime(self.currentDate, "%Y-%m-%d")        
        old_dateYear = current_date - relativedelta(months=12)
        old_dateYear_only_date = old_dateYear.date()        
        self.cr.execute("SELECT porName , NOU FROM ynumberofunits ")
        dailyUnits = self.cr.fetchall()
        if dailyUnits:
            compName=self.ui.companyName.text()
            content= f"""
            <p style="font-family:'Arial'; font-size:30px; text-align:center; color:black;">
                <strong>{compName}</strong>
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
                ----------------------------------------------
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
                عدد الوحدات المباعة لسنة<br>
                {self.currentDate[:4]}<br>
            </p>"""
            for nn in dailyUnits:
                name,number = nn          
                content+=f"""
                <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                    &nbsp;{name}  :  {number}<br>
                    ------------------------------------
                </p>"""

            self.ui.yearlySalesText.setHtml(content)

    ############################################################ Issue management ##########################################################

    def cashierReport(self):
        self.cr.execute("CREATE TABLE IF NOT EXISTS newShift (expName TEXT , revName TEXT , salesCash DECIMAL(10, 2) , visaCash DECIMAL(10, 2) , expenses DECIMAL(10, 2) , revenues DECIMAL(10, 2), date DATE NOT NULL )")
        self.cr.execute("SELECT * FROM newShift ")
        csherInfo = self.cr.fetchall()
        cashierName=(self.ui.cashierName.text()).strip()
        if cashierName=="":
            QMessageBox.warning(self, "Error", "You must type cashier name.")
        else:    
            self.ui.stackedWidget.setCurrentIndex(7)
            cshList=[]
            vsaList=[]
            expList=[]
            revList=[]
            revNameList=[]
            exNameList=[]
            if csherInfo:
                for data in csherInfo:
                    exName,revName,SalesCash,VisaCash,exps,revs,date=data
                    if SalesCash!=None:
                        cshList.append(SalesCash)
                    if VisaCash!=None:
                        vsaList.append(VisaCash)
                    if exps!=None:
                        expList.append(exps)
                    if revs!=None:
                        revList.append(revs)    
                    if revName!=None and revName!="CashierRevenueVisa" and revName!="CashierRevenueCash":
                        revNameList.append(revName)
                    if exName!=None and exName!="CashierRevenueVisa" and exName!="CashierRevenueCash":
                        exNameList.append(exName)
            TcshList=sum(cshList)    
            TvsaList=sum(vsaList)    
            TexpList=sum(expList)    
            TrevList=sum(revList)    
            totalRevenues=TrevList+TvsaList+TcshList
            compName=self.ui.companyName.text()
            casherName=self.ui.cashierName.text()
            content= f"""
            <p style="font-family:'Arial'; font-size:30px; text-align:center; color:black;">
                <strong>{compName}</strong>
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
                ----------------------------------------------
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                إسم الكاشير : {casherName}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  التاريخ : {self.currentDate}
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
            &nbsp;__________________________________________________________<br><br>
            
            &nbsp;مبيعات ( نقدية ): {TcshList:,} <br>
                <br>            
            &nbsp;مبيعات ( فيزا ) :&nbsp;&nbsp; {TvsaList:,} <br>
            ---------------------------------- <br>
            &nbsp;إجمالي المبيعات : &nbsp;{TvsaList+TcshList:,} <br>
                <br>
            &nbsp;إيرادات مسجلة : &nbsp;{TrevList:,} <br>
            ---------------------------------- <br>
            &nbsp;إجمالي النقدية :&nbsp;&nbsp; {TrevList+TcshList:,} <br>
                <br>
            &nbsp;مصروفات مسجلة :        ({TexpList:,}) <br>            
            ---------------------------------- <br>
            </p>"""
            if (TrevList+TcshList)-TexpList>=0:
                content+=f"""
                <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                &nbsp;صافي النقدية :&nbsp;&nbsp; {((TrevList+TcshList)-TexpList):,} <br>
                </p>"""
            elif (TrevList+TcshList)-TexpList<0:
                content+=f"""
                <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                &nbsp;صافي النقدية :&nbsp;&nbsp;( {(str((TrevList+TcshList)-TexpList))[1:]} )<br>
                </p>"""

            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
            ---------------------------------- <br>
                <br>            
            &nbsp;إجمالي إيرادات الشيفت :        {totalRevenues:,} <br><br>
            &nbsp;إجمالي مصروفات الشيفت :        ({TexpList:,}) <br>
            </p>"""
            
            if totalRevenues>=TexpList:
                content+=f"""
                <p style="font-family:'Arial'; font-size:25px; text-align:left; color:black;">
                    فائض : {totalRevenues-TexpList:,}
                </p>"""
            else:
                content+=f"""
                <p style="font-family:'Arial'; font-size:25px; text-align:left; color:black;">
                    عجز : ({(str(totalRevenues-TexpList))[1:]})<br><br>
                </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
            &nbsp;_____________________________________________________<br>
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:25px; text-align:left; color:black;">
            &nbsp;<strong>بيان الإيرادات</strong><br>
            </p>"""
            if revList!=[]:
                lenr=len(revNameList)
                r=0
                while r < lenr:
                    content+=f"""
                    <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                    &nbsp;{revNameList[r]}  :  {revList[r]:,}<br>
                    -----------------------------
                    </p>"""
                    r+=1
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
            &nbsp;_____________________________________________________<br>
            </p>"""
            content+=f"""
            <p style="font-family:'Arial'; font-size:25px; text-align:left; color:black;">
            &nbsp;<strong>بيان المصروفات</strong><br>
            </p>"""
            if expList!=[]:                
                lenx=len(exNameList)
                n=0
                while n < lenx:
                    content+=f"""
                    <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                    &nbsp;{exNameList[n]}  :  {expList[n]:,}<br>
                    -----------------------------
                    </p>"""
                    n+=1
            self.ui.cashierReportText.setHtml(content)

    def newShift(self):
        self.cr.execute("TRUNCATE TABLE newShift")

    def IS(self):
        fselected_date = self.ui.fromISDate.date()  
        FitstFormatted_date = fselected_date.toString("yyyy-MM-dd")  

        sselected_date = self.ui.toISDate.date()  
        LastFormatted_date = sselected_date.toString("yyyy-MM-dd")  
        
        self.ui.stackedWidget.setCurrentIndex(11)
        self.cr.execute("CREATE TABLE IF NOT EXISTS revenues (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
        self.cr.execute("SELECT  revName, amount FROM revenues WHERE revenue_date BETWEEN %s AND %s;",(FitstFormatted_date,LastFormatted_date))
        current_month_revenues= self.cr.fetchall()
        self.cr.execute("CREATE TABLE IF NOT EXISTS revenuesVisa (revName TEXT ,revenue_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
        self.cr.execute("SELECT  revName, amount FROM revenuesVisa WHERE revenue_date BETWEEN %s AND %s;",(FitstFormatted_date,LastFormatted_date))
        current_month_revenuesVisa= self.cr.fetchall()
        current_date = datetime.strptime(self.currentDate, "%Y-%m-%d")        
        old_dateMonth = current_date - relativedelta(months=1)
        old_dateMonth_only_date = old_dateMonth.date()        
        revVisaList=[]
        if current_month_revenuesVisa:
            for rvv in current_month_revenuesVisa:
                name,amount=rvv
                revVisaList.append(amount)
        salesrevList=[]
        rentrevList=[]
        interestrevList=[]
        saleCapitalrevList=[]
        advertiserevList=[]
        returninvestmentrevList=[]
        feesrevList=[]
        othersrevList=[]
        if current_month_revenues:
            for rv in current_month_revenues:
                name,amount=rv
                if name=="مبيعات كاشير" or name=="المبيعات":
                    salesrevList.append(amount)
                elif name=="الإيجارات" :
                    rentrevList.append(amount)
                elif name=="إيرادات الفائدة" :
                    interestrevList.append(amount)
                elif name=="بيع الأصول" :
                    saleCapitalrevList.append(amount)
                elif name=="إيرادات الإعلانات" :
                    advertiserevList.append(amount)
                elif name=="العائد من الاستثمارات" :
                    returninvestmentrevList.append(amount)
                elif name=="التعويضات والغرامات" :
                    feesrevList.append(amount)
                else:
                    othersrevList.append(amount)

        compName=self.ui.companyName.text()
        content= f"""
        <p style="font-family:'Arial'; font-size:30px; text-align:center; color:black;">
            <strong>{compName}</strong>
        </p>"""
        content+=f"""
        <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
            ----------------------------------------------
        </p>"""
        content+=f"""
        <p style="font-family:'Arial'; font-size:20px; text-align:center; color:black;">
            قائمة دخل<br>
            من<br>
            {FitstFormatted_date}<br>
            إلى<br>
            {LastFormatted_date}<br>
            ------------------------------<br>
        </p>"""
        revName=[]
        revAmount=[]
        TsalesR=(sum(salesrevList))+(sum(revVisaList))
        TrentR=sum(rentrevList)
        TinterestR=sum(interestrevList)
        TsaleCapitalR=sum(saleCapitalrevList)
        TadvertiseR=sum(advertiserevList)
        TinvsetR=sum(returninvestmentrevList)
        TfeesR=sum(feesrevList)
        TotherR=sum(othersrevList)
        if TsalesR>0:
            revName.append("المبيعات")
            revAmount.append(TsalesR)
        if TrentR>0:
            revName.append("الإيجارات")
            revAmount.append(TrentR)
        if TinterestR>0:
            revName.append("إيرادات الفائدة")
            revAmount.append(TinterestR)
        if TsaleCapitalR>0:
            revName.append("بيع الأصول")
            revAmount.append(TsaleCapitalR)
        if TadvertiseR>0:
            revName.append("إيرادات الإعلانات")
            revAmount.append(TadvertiseR)
        if TinvsetR>0:
            revName.append("العائد من الاستثمارات")
            revAmount.append(TinvsetR)
        if TfeesR>0:
            revName.append("التعويضات والغرامات")
            revAmount.append(TfeesR)
        if TotherR>0:
            revName.append("إيرادات اخرى")
            revAmount.append(TotherR)
        content+=f"""
        <p style="font-family:'Arial'; font-size:25px; text-align:left; color:black;">
           &nbsp;<strong> الإيرادات</strong>
        </p>"""
        lenl=len(revName)
        l=0
        while l<lenl:
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                &nbsp;{revName[l]}   :  {revAmount[l]:,}
            </p>"""
            l+=1
        content+=f"""
        <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
            <br>&nbsp;<u>إجمالي الإيرادات  :   {sum(revAmount):,}</u><br>
        </p>"""
        content+=f"""
        <p style="font-family:'Arial'; font-size:25px; text-align:left; color:black;">
           &nbsp;<strong> المصروفات</strong>
        </p>"""
        self.cr.execute("CREATE TABLE IF NOT EXISTS expenses (expName TEXT ,expense_date DATE NOT NULL,amount DECIMAL(11, 2) NOT NULL )")
        self.cr.execute("SELECT  expName, amount FROM expenses WHERE expense_date BETWEEN %s AND %s;",(FitstFormatted_date,LastFormatted_date))
        current_month_expenses= self.cr.fetchall()
        purchaseExList=[]
        saleExList=[]
        operationExList=[]
        managementExList=[]
        financeExList=[]
        foundationExList=[]
        transationExList=[]
        shareGoodsExList=[]
        advertiseExList=[]
        salaryExList=[]
        rentExList=[]
        interestExpList=[]
        otherExList=[]
        if current_month_expenses:
            for ex in current_month_expenses:
                name,amount=ex
                if name=="مصروفات الشراء":
                    purchaseExList.append(amount)
                elif name=="مصروفات البيع":
                    saleExList.append(amount)
                elif name=="مصروفات التشغيل":
                    operationExList.append(amount)
                elif name=="مصروفات إدارية وعمومية":
                    managementExList.append(amount)
                elif name=="مصروفات مالية وتمويلية":
                    financeExList.append(amount)
                elif name=="مصروفات التأسيس":
                    foundationExList.append(amount)
                elif name=="مصروفات شحن ونقل المشتريات":
                    transationExList.append(amount)
                elif name=="مصروفات شحن ونقل وتوزيع البضاعة":
                    shareGoodsExList.append(amount)
                elif name=="مصروفات الدعاية والإعلان":
                    advertiseExList.append(amount)
                elif name=="رواتب الموظفين":
                    salaryExList.append(amount)
                elif name=="مصروفات استئجار":
                    rentExList.append(amount)
                elif name=="مصروفات الفائدة":
                    interestExpList.append(amount)
                else:
                    otherExList.append(amount)
        exName=[]        
        exAmount=[]
        Tpurchasex=sum(purchaseExList)
        Tsalesx=sum(saleExList)
        Toperatex=sum(operationExList)
        Tmanagex=sum(managementExList)
        Tfinancex=sum(financeExList)
        Tfoundationx=sum(foundationExList)
        Ttransationx=sum(transationExList)
        Tsharegoodsx=sum(shareGoodsExList)
        Tadvertisex=sum(advertiseExList)
        Tsalaryx=sum(salaryExList)
        Trentx=sum(rentExList)
        Tinterestx=sum(interestExpList)
        Totherx=sum(otherExList)
        if Tpurchasex>0:
            exName.append("مصروفات الشراء")
            exAmount.append(Tpurchasex)
        if Tsalesx>0:
            exName.append("مصروفات البيع")
            exAmount.append(Tsalesx)
        if Toperatex>0:
            exName.append("مصروفات التشغيل")
            exAmount.append(Toperatex)
        if Tmanagex>0:
            exName.append("مصروفات إدارية وعمومية")
            exAmount.append(Tmanagex)
        if Tfinancex>0:
            exName.append("مصروفات مالية وتمويلية")
            exAmount.append(Tfinancex)
        if Tfoundationx>0:
            exName.append("مصروفات التأسيس")
            exAmount.append(Tfoundationx)
        if Ttransationx>0:
            exName.append("مصروفات شحن المشتريات")
            exAmount.append(Ttransationx)
        if Tsharegoodsx>0:
            exName.append("مصروفات توزيع البضاعة")
            exAmount.append(Tsharegoodsx)
        if Tadvertisex>0:
            exName.append("مصروفات الدعاية والإعلان")
            exAmount.append(Tadvertisex)
        if Tsalaryx>0:
            exName.append("رواتب الموظفين")
            exAmount.append(Tsalaryx)
        if Trentx>0:
            exName.append("مصروفات استئجار")
            exAmount.append(Trentx)
        if Tinterestx>0:
            exName.append("مصروفات الفائدة")
            exAmount.append(Tinterestx)
        if Totherx>0:
            exName.append("مصروفات اخرى")
            exAmount.append(Totherx)
        lenh=len(exName)
        h=0
        while h<lenh:
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                &nbsp;{exName[h]}   :  {exAmount[h]:,}
            </p>"""
            h+=1
        content+=f"""
        <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
            <br>&nbsp;<u>إجمالي المصروفات  :   ( {sum(exAmount):,} )</u>
        </p>"""
        netIncomee=float(sum(revAmount))-float(sum(exAmount))
        netIncome=round(netIncomee,2)
        if netIncome>0:
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                <br>&nbsp;<u>صافي الدخل   :   {netIncome:,}</u>
            </p>"""
        elif netIncome<0:
            content+=f"""
            <p style="font-family:'Arial'; font-size:20px; text-align:left; color:black;">
                <br>&nbsp;<u><strong>صافي الدخل   :   ( {(str(netIncome))[1:]} )</strong></u>
            </p>"""
        self.ui.MISText.setHtml(content)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
