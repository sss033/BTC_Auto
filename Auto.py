import pyupbit
import pandas as pd
import time

# 업비트 API 키 설정
access_key = "AEYnkYU1rRF9xxxCbB3mvbQrFmyxclP7WXxMMpWJ"
secret_key = "76HnxAkSl5VMsv3xpbSwebwr0reqxVIfSRPpY8Yj"
upbit = pyupbit.Upbit(access_key, secret_key)

# 매매에 사용할 코인 및 금액 설정
target_coin = "BTC"
buy_amount = 100000  # 매수할 금액 (원)

# 전략에 필요한 파라미터 설정
short_window = 10  # 단기 이동평균 기간
long_window = 30   # 장기 이동평균 기간
rsi_threshold = 30  # RSI 매수 기준
macd_short = 12     # MACD 단기 기간
macd_long = 26      # MACD 장기 기간
macd_signal = 9     # MACD 시그널 기간

# 주기적으로 매매 시그널을 확인하는 함수
def check_signal():
    while True:
        try:
            # 현재 시세 정보 가져오기
            df = pyupbit.get_ohlcv(f"{target_coin}-KRW", interval="minute5", count=long_window)
            
            # 이동평균 계산
            df['short_MA'] = df['close'].rolling(window=short_window).mean()
            df['long_MA'] = df['close'].rolling(window=long_window).mean()

            # RSI 계산
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14, min_periods=1).mean()
            avg_loss = loss.rolling(window=14, min_periods=1).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # MACD 계산
            df['MACD'] = df['close'].ewm(span=macd_short).mean() - df['close'].ewm(span=macd_long).mean()
            df['Signal'] = df['MACD'].ewm(span=macd_signal).mean()

            # 매매 신호 확인 및 실행
            if df.iloc[-1]['short_MA'] > df.iloc[-1]['long_MA'] and rsi.iloc[-1] > rsi_threshold and df.iloc[-1]['MACD'] > df.iloc[-1]['Signal']:
                balance = upbit.get_balance("KRW")
                if balance >= buy_amount:
                    upbit.buy_market_order(f"{target_coin}-KRW", buy_amount)
                    print(f"매수 완료: {target_coin}을 {buy_amount}원에 구매")
            else:
                # 다른 매매 전략 추가 가능
                pass
                
            # 5분마다 반복
            time.sleep(300)

        except Exception as e:
            print(e)
            time.sleep(1)

# 매매 시작
check_signal()
