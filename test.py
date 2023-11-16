from datetime import datetime, timedelta

date = 10
print("gkdl")
message = f"[globalJongmokName.strip()] {date} 이동평균선이 정배열된 양지차트입니다."
message += f"\n[globalJongmokName.strip()] {date} 우헤헤"
print(message)

startDate = datetime.now()
endDate = startDate - timedelta(days=5)
startDate = startDate.strftime("%Y%m%d")
endDate = endDate.strftime("%Y%m%d")
print(startDate,endDate)