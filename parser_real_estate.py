import csv,glob
import sqlite3

#설명: csv 형식의 부동산자료들을 real_estate_transactions.db

column_names = [
  "시군구",
  "번지",
  "본번",
  "부번",
  "단지명",
  "전용면적",
  "계약년월",
  "계약일",
  "거래금액",
  "동",
  "층",
  "매수자",
  "매도자",
  "건축년도",
  "도로명",
  "해제사유발생일",
  "거래유형",
  "중개사소재지",
  "등기일자"
]



# SQLite 데이터베이스 파일 경로
sqlite_file_path = "real_estate_transactions.db"

# 테이블 이름
table_name = "transactions"

# SQLite 연결 객체 생성
connection = sqlite3.connect(sqlite_file_path)

for csv_file_path in glob.glob("*.csv"):
  print (csv_file_path)
  num = 0
  with open(csv_file_path, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    # 커서 객체 생성
    cursor = connection.cursor()
    for row in reader:
      if num < 16:
        pass
      else:
        tmp = list()
        for r in row[1:]:
          tmp.append(r.strip())
          cursor.execute("""INSERT OR IGNORE INTO transactions ("시군구","번지","본번","부번","단지명","전용면적","계약년월","계약일","거래금액","동","층","매수자","매도자","건축년도","도로명","해제사유발생일","거래유형","중개사소재지","등기일자") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (tmp),)
          # 커밋
          connection.commit()
          
      num+=1
        

# 연결 닫기
connection.close()
