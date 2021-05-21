import mysql.connector

mydb = mysql.connector.connect(

	host = "localhost",
	user = "root",
	password = "password",
	database = "student"
)

mycursor = mydb.cursor()

# mycursor.execute("SELECT * FROM student")

# result = mycursor.fetchall()

# for i in result:

        # print(i)

def admin():
    print("admin login")
    username = input(str("username: "))
    password = input(str("Password: "))

    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("incorrect password here")
    else:
        print('login details are unrecognised')
def admin_session():
        while 1:
            print("students enrolled:")
            mycursor.execute("SELECT * FROM student order by student.cutoff DESC")
            myresult=mycursor.fetchall()
            for i in myresult:
                print(i)
            
            print('Do you wish to Modify?y/n')
            user_opt=str(input())
            if user_opt == 'n':
                break
            else:
                studentId=int(input("Enter Student Id: "))
                status=str(input('Enter status: ')) 
                values=(status,studentId)
                try:
                    mycursor.execute("UPDATE student SET status = %s WHERE studentId = %s",values)
                    mycursor.execute("SELECT dept FROM student WHERE studentId = %s",(studentId,))
                    result=mycursor.fetchone()
                    val=(result[0], )
                    mycursor.execute("SELECT availableSeats FROM department WHERE departmentName = %s",val)
                    result=mycursor.fetchone()
                    if result != None and result[0] != 0 and status == 'APPROVED':
                        mycursor.execute("UPDATE department SET availableSeats = availableSeats - 1 WHERE departmentName = %s and availableSeats > 0", val)
                    elif status == 'APPROVED':
                        raise Exception()
                    mydb.commit()
                except:
                    print("Invalid Details Provided!")

            print('Do you wish to continue?y/n')
            user_opt=str(input())
            if user_opt == 'n':
                break
            

                
def student_session():
        print('Available Departments: ')
        mycursor.execute("SELECT * FROM department")
        result=mycursor.fetchall()
        for i in result:
            print(i)
        print("enter the details")
        name=input(str("name: "))
        dept=input(str("dept: "))
        age=input(str("age: "))
        cutoff=input(str("cutoff: "))
        val=(dept, )
        mycursor.execute("SELECT availableSeats FROM department WHERE departmentName = %s",val)
        val=(name,dept,age,cutoff)
        result=mycursor.fetchone()
        print(result)
        if result != None and result[0] > 0 :
            mycursor.execute("INSERT INTO student(name,dept,age,cutoff) VALUES (%s, %s, %s, %s)",val)
            mydb.commit()
            mycursor.execute("SELECT * FROM student")
            result=mycursor.fetchall()
            for i in result:
                print(i)
        else:
            print("You can't apply for this department!")
            
def main():
    print("welcome ")
    print("login as: ")
    print("1.student")
    print("2.admin ")
    user_opt= input(str("login as: "))

    if user_opt == '1' :
         student_session()
    elif user_opt == '2':
         admin()
    else:
         print("invalid number")

main()
