
import os

import sqlite3
import time
from tkinter import E
from types import NoneType

import pandas as pd

import const
from utils import Time


class DemoAccount:
    # db = sqlite3.connect(f'.{os.sep}db{os.sep}DemoAcc.db', uri=True, isolation_level=None)
    # cur = db.cursor()
    # fee_market = 0.9996
    # fee_limit = 0.9998
    # trades_table = 'trades'
    # orders_table = 'orders'
    # cur.execute(f'create table if not exists {trades_table}(eventTime,eventEnd,symbol,open_price,average_price,close_price,quantity,amount,side,balance,pnl_percentage,pnl_profit_part,pnl_profit,fee,inPossition,order_count)')
    # cur.execute(f'create table if not exists {orders_table}(eventTime,symbol,price,quantity,amount,side,balance)') #add fee and other column
    # cur.execute(f'create table if not exists balance(eventTime,balance)')
    # try:
    #     inPossitionStatus = dict(cur.execute(f'select * from inPossition').fetchall())
    # except Exception:
    #     tickerLst = const.TICKERS + ['BTCUSDT']
    #     inPossitionStatusDict={t:False for t in tickerLst}
    #     cur.execute(f'create table if not exists inPossition(symbol TEXT,status INTEGER)')
    #     cur.executemany(f'insert into inPossition values(?,?)', ((k,v) for k,v in inPossitionStatusDict.items()))
    #     db.commit()
    #     inPossitionStatus = dict(cur.execute(f'select * from inPossition').fetchall())

    @classmethod
    def drop_tables(cls):
        cls.cur.execute(f'drop table if exists {cls.trades_table}')
        cls.cur.execute(f'drop table if exists {cls.orders_table}')
        cls.cur.execute(f'drop table if exists balance')
        cls.db.commit()

    def __init__(self, balance, db_name):
        self.db_name = db_name
        self.tickerLst = const.TICKERS + ['BTCUSDT'] +['1000PEPEUSDT']
        # self.symbol = symbol.upper()
        self.db = sqlite3.connect(f'.{os.sep}demoaccdb{os.sep}{self.db_name}.db', uri=True, isolation_level=None)
        self.cur = self.db.cursor()
        self.fee_market = 0.9996
        self.fee_limit = 0.9998
        self.trades_table = 'trades'
        self.orders_table = 'orders'
        self.cur.execute(
            f"""create table if not exists {self.trades_table}(eventTime,eventEnd,symbol,open_price,average_price,
            close_price,quantity,amount,side,balance,pnl_percentage,pnl_profit_part,pnl_profit,fee,inPossition,
            order_count,tp,sl,tp_trail,sl_trail,trail_status)"""
            )
        self.cur.execute(f'create table if not exists {self.orders_table}(eventTime,symbol,price,quantity,amount,side,balance)') #add fee and other column
        self.cur.execute(f'create table if not exists balance(eventTime,balance)')
       
        try:
            self.inPossitionStatus = dict(self.cur.execute(f'select * from inPossition').fetchall())
        except Exception:
            # self.tickerLst = const.TICKERS + ['BTCUSDT']
            inPossitionStatusDict={t:False for t in self.tickerLst}
            self.cur.execute(f'create table if not exists inPossition(symbol TEXT,status INTEGER)')
            self.cur.executemany(f'insert into inPossition values(?,?)', ((k,v) for k,v in inPossitionStatusDict.items()))
            self.db.commit()
            self.inPossitionStatus = dict(self.cur.execute(f'select * from inPossition').fetchall())

        query = 'select balance from balance order by rowid desc limit 1'
        try:
            # with self.db as conn:
            #     cur = conn.cursor()
            #     self.balance = cur.execute(query).fetchone()[0]
            self.balance = self.cursor(query)[0]
            
        except TypeError:
            self.ts = Time.get_timestamp()
            query = 'insert into balance values(?,?)'
            self.balance = balance
            self.execute(query, (self.ts,self.balance))
        else: print(f'Connected to {self.db_name}.db'.__repr__())
    

    def drop_tables(self):
        self.cur.execute(f'drop table if exists {self.trades_table}')
        self.cur.execute(f'drop table if exists {self.orders_table}')
        self.cur.execute(f'drop table if exists balance')
        self.db.commit()

    def create_connection(self, db_name_):
        query = f'file:.{os.sep}db{os.sep}{db_name_}.db?mode=ro'
        connection = sqlite3.connect(query, uri=True, isolation_level=None)
        return connection
    
    def execute(self, query, values):
        with self.db as conn:
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            cur.close()
    
    def cursor(self, query, values=None):
        with self.db as conn:
            cur = conn.cursor()
            if values:
                res = cur.execute(query, values)
                conn.commit()
            res = cur.execute(query).fetchone()
        return res

    def cursormany(self, query, values=None):
        with self.db as conn:
            cur = conn.cursor()
            if values:
                res = cur.execute(query, values)
                conn.commit()
            res = cur.execute(query)
        return res
    
    @staticmethod
    def get_status_static(symbol, db_name):
        db = sqlite3.connect(f'.{os.sep}db{os.sep}{db_name}.db', uri=True, isolation_level=None)
        cur = db.cursor()
        status = cur.execute(f"select status from inPossition where symbol='{symbol}'").fetchone()[0]
        return status

    def get_status(self, all=None):
        if all=='all':
            self.inPossitionStatus = dict(self.cur.execute(f'select * from inPossition').fetchall())
            return self.inPossitionStatus
        if self.symbol == "PEPEUSDT":
            self.symbol = '1000'+ self.symbol
        status = self.cursor(f"select status from inPossition where symbol='{self.symbol}'")
        if type(status) == NoneType:
            return False
        else: 
            return status[0]
    
    def update_status(self,value):
        self.value = value
        self.execute(f"update inPossition set symbol=?,status=? where symbol='{self.symbol}'",(self.symbol,self.value))

    def get_balance(self):
        query = 'select balance from balance order by rowid desc limit 1'
        self.balance = self.cursor(query)[0]
        return self.balance

    def update_balace(self, balance):
        self.balance = balance
        self.ts = Time.get_timestamp()
        query = f'insert into balance values(?,?)'
        self.execute(query, (self.ts,self.balance))

    def select_last_trade(self):
        try:
            query = f"select * from {self.trades_table} where symbol=='{self.symbol}' and inPossition==1 order by rowid desc limit 1"
            res = pd.read_sql(query,self.db)
            res.iloc[0]
        except IndexError:
            return False
        except Exception as ex:
            print(ex, 'SSSSSSSSSSFDFSFSF 152')
            return False
        return res

    def get_current_price(self,symbol=None):
        if symbol:
            self.symbol = symbol.upper()
        if self.symbol == '1000PEPEUSDT':
            self.symbol = 'PEPEUSDT'
        query = f'select t from {self.symbol}_trades order by rowid desc limit 1'
        connection = self.create_connection(self.symbol)
        with connection as conn:
            cur = conn.cursor()
            last_price = cur.execute(query).fetchone()[0]
            cur.close()
        return float(last_price)
    
    def calculate_pnl_all(self, show_df=False):
        
        for symbol in self.tickerLst:
            self.symbol = symbol.upper()
            if self.get_status() == 1:
                # print(f'Begin update pnl for {self.symbol}')
                self.df = self.select_last_trade()
                self.initial = self.df['average_price'].iloc[0]
                self.side = self.df['side'].iloc[0]
                self.final = self.get_current_price(self.symbol)
                self.quantity = self.df['quantity'].iloc[0]
                self.df['close_price'] = self.final
                self.df['eventEnd'] = Time.get_timestamp()
                
                #XXX обновляет все пнл
                self.df['balance'] = self.get_balance()
                
                if self.side == 'SHORT':
                    if self.initial < self.final: #-
                        self.pnl_percentage = ((self.final-self.initial)/self.initial)*-100
                        self.pnl_profit = abs(self.quantity*self.final-self.df['amount'].iloc[0])*-1
                    else: #+
                        self.pnl_percentage = ((self.initial-self.final)/self.initial)*100
                        self.pnl_profit = self.df['amount'].iloc[0]-self.quantity*self.final
                else: #long
                    if self.initial < self.final: #+
                        self.pnl_percentage = ((self.final-self.initial)/self.initial)*100
                        self.pnl_profit = abs(self.quantity*self.final-self.df['amount'].iloc[0])
                    else: #-
                        self.pnl_percentage = ((self.initial-self.final)/self.initial)*-100
                        self.pnl_profit = abs(self.df['amount'].iloc[0]-self.quantity*self.final)*-1
                self.df['pnl_percentage'],self.df['pnl_profit']=round(self.pnl_percentage,3), round(self.pnl_profit)
                self.df['pnl_profit'] += self.df['pnl_profit_part'].iloc[0] - self.df['fee'].iloc[0]
                query = f"update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,average_price=?,close_price=?,\
                    quantity=?,amount=?,side=?,balance=?,\
                    pnl_percentage=?,pnl_profit_part=?,pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=? where eventTime={self.df['eventTime'].iloc[0]}"
                self.execute(self.query_update_trade, tuple(self.df.values[0]))
                if show_df:
                    print(self.select_last_trade().T)
            else: pass

    def calculate_pnl(self, autopilot: tuple = None, autopilot_trail:tuple = None, trail_update: bool = False, show_df=False):
        """ Calculate pnl for given trade. Use params for simple TP/SL strategy.\n
            :autopilot: tuple(TakeProfit,StopLoss)\n
            :autopilot_trail: same as autopilot\n
            :trail_update: update current 'autopilot_trail' args\n

            :return: pnl%
            """
        #if not in pos not calc this code
        status = self.get_status()
        ### print(status, self.symbol,'calc pnl^^^^') 
        if status == 0:
            return False
        self.df = self.select_last_trade()
        if type(self.df) == bool and status == 1:
            self.update_status(0)
            return False
        #XXX обновляет все пнл
        self.df['balance'] = self.get_balance()

        self.initial = self.df['average_price'].iloc[0]
        self.side = self.df['side'].iloc[0]
        self.final = self.get_current_price(self.symbol)
        self.quantity = self.df['quantity'].iloc[0]
        self.df['close_price'] = self.final
        self.df['eventEnd'] = Time.get_timestamp()
        if self.side == 'SHORT':
            if self.initial < self.final: #-
                self.pnl_percentage = ((self.final-self.initial)/self.initial)*-100
                # self.pnl_profit = abs(self.quantity*self.final-self.df['amount'].iloc[0])*-1
                self.pnl_profit = self.df['amount'].iloc[0] * self.pnl_percentage / 100
            else: #+
                self.pnl_percentage = ((self.initial-self.final)/self.initial)*100
                # self.pnl_profit = self.df['amount'].iloc[0]-self.quantity*self.final
                self.pnl_profit = self.df['amount'].iloc[0] * self.pnl_percentage / 100
        else: #long
            if self.initial < self.final: #+
                self.pnl_percentage = ((self.final-self.initial)/self.initial)*100
                # self.pnl_profit = abs(self.quantity*self.final-self.df['amount'].iloc[0])
                self.pnl_profit = self.df['amount'].iloc[0] * self.pnl_percentage / 100
            else: #-
                self.pnl_percentage = ((self.initial-self.final)/self.initial)*-100 #-100
                # self.pnl_profit = abs(self.df['amount'].iloc[0]-self.quantity*self.final)*-1 #-1
                self.pnl_profit = self.df['amount'].iloc[0] * self.pnl_percentage / 100


        self.df['pnl_percentage'],self.df['pnl_profit']=round(self.pnl_percentage,3), round(self.pnl_profit,3)
        self.df['pnl_profit'] += self.df['pnl_profit_part'].iloc[0] - self.df['fee'].iloc[0]
        query = f"update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,average_price=?,close_price=?,\
            quantity=?,amount=?,side=?,balance=?,\
            pnl_percentage=?,pnl_profit_part=?,pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=? where eventTime={self.df['eventTime'].iloc[0]}"
        
        self.query_update_trade = f"""update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,
        average_price=?,close_price=?,quantity=?,amount=?,side=?,balance=?,pnl_percentage=?,pnl_profit_part=?,
        pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=?,trail_status=? where eventTime={self.df['eventTime'].iloc[0]}"""
        
        #STRATEGY FOR TAKE\STOP FOR THIS TIME 
        if trail_update and autopilot and autopilot_trail:
            self.df['trail_status'] = 0

        if autopilot and not autopilot_trail:
            self.df["tp"],self.df["sl"] = autopilot
            if self.pnl_percentage >= self.df["tp"].iloc[0] or self.pnl_percentage < self.df["sl"].iloc[0]*-1:
                self.close_possition(calculate=False)
                return True
            else: return False
        if autopilot and autopilot_trail:
            if self.df['trail_status'].iloc[0] == 0 and not trail_update:
                self.df["tp"],self.df["sl"] = autopilot
                self.df['tp_trail'],self.df['sl_trail'] = autopilot_trail
            elif self.df['trail_status'].iloc[0] == 0 and trail_update: # update for close pos instant after update if condition have met
                self.df['trail_status'] = 1
                self.df['tp_trail'],self.df['sl_trail'] = autopilot_trail
                self.df["sl"] = self.df['tp'].iloc[0]-self.df['sl_trail'].iloc[0] 
            if self.df["sl"].iloc[0] < 0 or self.df['trail_status'].iloc[0] == 1: # 'not trail_update" do work with first cycle, and if we wanna update sl with already -pnl% will wait until sl triggered
                self.df["sl"] *= -1 
            if self.pnl_percentage < self.df["sl"].iloc[0]*-1:
                #whatever with status, we have closed position
                self.df['trail_status'] = 0
                self.close_possition(calculate=False)
                return True
            elif self.pnl_percentage >= self.df["tp"].iloc[0] and self.df['trail_status'].iloc[0] == 0:
                self.df['trail_status'] = 1
                self.df["sl"] = self.pnl_percentage-self.df['sl_trail'].iloc[0]
                self.df['tp'] = self.pnl_percentage
            elif self.pnl_percentage >= self.df['tp'].iloc[0]:
                self.df["sl"] = self.pnl_percentage-self.df['sl_trail'].iloc[0]
                self.df['tp'] = self.pnl_percentage
            self.df["sl"] = abs(self.df["sl"].iloc[0])
            ########################################
        
        

        self.execute(self.query_update_trade, tuple(self.df.values[0]))
        if show_df:
            return self.df
        
        
        return self.df['pnl_percentage'].iloc[0]

    def calculate_pnl_part(self, df:pd.DataFrame):
        self.df = df
        self.initial = self.df['average_price'].iloc[0]
        self.final = self.df['close_price'].iloc[0]
        self.df['quantity'] -= self.quantity
        # self.amount -= self.fee
        self.df['amount'] -= self.amount
        self.df['fee'] += self.fee
        
        # print(self.final == self.get_current_price(self.symbol))
        # print('self.side,self.amount, self.quantity, self.initial, self.final')
        # print(self.side,self.amount, self.quantity, self.initial, self.final, '||', self.quantity*self.initial-self.amount)
        # print('PART:',self.quantity*self.final-self.amount)
        
        
        # if self.side == 'SHORT':
        #     if self.initial < self.final: #-
        #         self.pnl_profit_part_calc = abs(self.quantity*self.initial-self.amount)
        #     else: #+
        #         self.pnl_profit_part_calc = abs(self.quantity*self.initial-self.amount)*-1
        # else: #long=== +
        #     if self.initial < self.final:
                
        #         self.pnl_profit_part_calc = abs(self.quantity*self.initial-self.amount)*-1
        #     else: #-
        #         self.pnl_profit_part_calc = abs(self.quantity*self.initial-self.amount)


        if self.side == 'SHORT':
            if self.final >= self.initial : #long v +
                self.pnl_profit_part_calc = self.amount - self.quantity*self.initial
            else: #-
                self.pnl_profit_part_calc = self.quantity*self.initial-self.amount
        else: 
            if self.final >= self.initial : #short v -
                
                self.pnl_profit_part_calc = self.quantity*self.initial-self.amount
            else: #+
                self.pnl_profit_part_calc = self.quantity*self.initial-self.amount
        
        
        self.df['pnl_profit_part'] += self.pnl_profit_part_calc
        self.update_balace(self.get_balance() + self.amount-self.fee)
        self.df['balance'] = self.balance
        query = f"update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,average_price=?,close_price=?,\
            quantity=?,amount=?,side=?,balance=?,\
            pnl_percentage=?,pnl_profit_part=?,pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=? where eventTime={self.df['eventTime'].iloc[0]}"
        self.execute(self.query_update_trade, tuple(self.df.values[0]))

    def get_pnl_all(self, active=None):
        with self.db as conn:
            if active == 'active':
                self.df = pd.read_sql(f'select pnl_profit from {self.trades_table} where inPossition=1',conn)
                print(self.df.sum().values[0])
                return self.df.sum().values[0]
            elif active == 'closed':
                self.df = pd.read_sql(f'select pnl_profit from {self.trades_table} where inPossition=0',conn)
                print(self.df.sum().values[0])
                return self.df.sum().values[0]
            else:
                self.df = pd.read_sql(f'select pnl_profit from {self.trades_table}',conn)
                print(self.df.sum().values[0])
                return self.df.sum().values[0]
        
    def get_pnl(self):
        #XXX
        self.df = pd.read_sql(f'select pnl_profit from {self.trades_table} where symbol="{self.symbol}"',self.db)
        print(self.df.sum().values[0])
        return self.df.sum().values[0]


    def place_order_market(self, symbol:str, amount, side: str, timestamp = Time.get_timestamp()):
        self.ts = timestamp
        self.symbol = symbol.upper()
        self.open_price = self.get_current_price(self.symbol)
        if self.symbol in ['BTCUSDT']:
             amount = self.open_price/1000
        self.quantity = round(amount/self.open_price,3)
        self.amount = self.quantity*self.open_price
        self.fee = self.amount*(1-self.fee_market) #TODO СДЕЛАТЬ ЧТОТО С КОМСОЙ
        self.side = side.upper()
        self.pnl_profit_part = 0
        self.pnl_percentage,self.pnl_profit = 0,0
        self.tp,self.sl,self.tp_trail,self.sl_trail = 0,0,0,0
        self.trail_status = 0
        if self.get_status() == 0:
            if self.get_balance() < self.amount+self.fee: # self.balance >>> self.get_balance()
                print(f'insufficient balance! [{self.balance:.2f}]')
                return False
            self.update_balace(self.get_balance() - self.amount-self.fee)
            self.close_price = self.open_price
            self.average_price = self.open_price
            self.update_status(1)
            self.order_count = 1
            query = f"INSERT INTO {self.trades_table} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            
            values = (self.ts, self.ts, self.symbol, self.open_price, self.average_price, self.close_price, self.quantity, self.amount, self.side, self.balance,\
                self.pnl_percentage,self.pnl_profit_part, self.pnl_profit, self.fee, self.get_status() ,self.order_count, self.tp,self.sl,self.tp_trail,self.sl_trail,self.trail_status)
            self.execute(query,values)
        else: #(eventTime,eventEnd,symbol,open_price,average_price,close_price,quantity,amount,side,balance,pnl_percentage,pnl_profit,inPossition)
            #NOTE CHANGE SELF.DF TO SELF.DF_TRADE OR SOMETHIG MORE OBVIOUS!
            self.df = self.select_last_trade()
            if type(self.df) == bool:
                return False
            self.df['eventEnd'] = self.ts
            self.df['close_price'] = self.open_price
            if self.side == self.df['side'].iloc[0]:
                if self.get_balance() < self.amount+self.fee:
                    print(f'insufficient balance! [{self.balance:.2f}]')
                    return False
                self.update_balace(self.get_balance() - self.amount-self.fee)
                self.df['balance'] = self.balance
                self.df['order_count'] += 1
                self.df['quantity'] += self.quantity
                self.df['amount'] += self.amount
                self.df['fee'] += self.fee
                if self.df['order_count'].iloc[0] == 2:
                    self.df['average_price'] = (self.quantity+self.df['quantity'].iloc[0])/(self.df['quantity'].iloc[0]/self.df['open_price'].iloc[0]+self.quantity/self.open_price)
                else:
                    self.df['average_price'] = (self.quantity+self.df['quantity'].iloc[0])/(self.df['quantity'].iloc[0]/self.df['average_price'].iloc[0]+self.quantity/self.open_price)
            else: #opposite trade
                if self.quantity < self.df['quantity'].iloc[0]:
                    self.calculate_pnl_part(self.df)
                    return True
                elif self.quantity > self.df['quantity'].iloc[0]:
                    self.close_possition()
                    return True
            # self.df['balance'] = self.get_balance() #TODO заменить на self.balance ГДЕ ЄТО БУДЕТ РАБОТАТЬ
            # self.df['pnl_percentage'],self.df['pnl_profit'] = self.calculate_pnl()

            # query = f"update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,average_price=?,close_price=?,\
            #     quantity=?,amount=?,side=?,balance=?,\
            #     pnl_percentage=?,pnl_profit_part=?,pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=? where eventTime={self.df['eventTime'].iloc[0]}"
            
            #NOTE new query for all update trades
            self.query_update_trade = f"""update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,
        average_price=?,close_price=?,quantity=?,amount=?,side=?,balance=?,pnl_percentage=?,pnl_profit_part=?,
        pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=?,trail_status=? where eventTime={self.df['eventTime'].iloc[0]}"""
            self.execute(self.query_update_trade, tuple(self.df.values[0]))
        return True
            # print('lAST TRADE after MOD:', self.df.T)
    
    def close_possition_all(self):
        for symbol in self.tickerLst:
            self.symbol = symbol.upper()
            if self.get_status() !=1:
                # print(f'No open possition for {self.symbol}')
                continue
            if not self.calculate_pnl():
                continue
            #XXX sECONG USESSLESS CALL AFTER CALC PNL WHERE ALREADY UPDATED self.DF! try to remove next time
            self.df = self.select_last_trade()
            # print(self.symbol, self.df['symbol'].iloc[0]) #XXX
            self.df['inPossition'] = 0
            self.df['eventEnd'] = Time.get_timestamp()
            last_fee = self.df['quantity'].iloc[0]*self.df['close_price'].iloc[0]*(1-self.fee_market)
            # self.df['fee'] += self.df['quantity'].iloc[0]*self.df['close_price'].iloc[0]*(1-self.fee_market)
            # self.df['pnl_profit'] -= self.df['fee'].iloc[0]
            
            self.result_balance = self.df['amount'].iloc[0]+self.df['pnl_profit'].iloc[0]+self.balance + self.df['fee'].iloc[0] - last_fee
            
            
            # self.result_balance = self.df['quantity'].iloc[0]*self.df['close_price'].iloc[0]+self.df['balance'].iloc[0]
            self.update_balace(self.result_balance)
            self.df['balance'] = self.balance
            self.df['fee'] += last_fee
            self.df['pnl_profit'] -= last_fee
            query = f"update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,average_price=?,close_price=?,\
                    quantity=?,amount=?,side=?,balance=?,\
                    pnl_percentage=?,pnl_profit_part=?,pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=? where eventTime={self.df['eventTime'].iloc[0]}"
            self.execute(self.query_update_trade, tuple(self.df.values[0]))
            print(f'*********************[Possition {self.side} {self.symbol} closed!]********************* \n\t \
            [PNL]:{self.df["pnl_profit"].iloc[0]:.2f}$ {self.pnl_percentage:.2f}%\n***************************************************************************')
            self.update_status(0)    

    def close_possition(self, symbol=None, calculate=True):
        if symbol:
            self.symbol = symbol.upper()
        ## XXX ПОХОДУ СИЛЬНО ДОХУЯ КАЛК ПНЛА, НАМУДРИЛ. НА ФИКС
        ##XXX И ПОХОДУ СИЛЬНО ДОХУЯ ОБНОВ self.df 
        if calculate:
            self.calculate_pnl()

        if self.get_status() !=1:
            # print(f'****************[No open possition for {self.symbol!r}]****************') #XXX
            return False
        
        #XXX sECONG USESSLESS CALL AFTER CALC self.select_last_trade() PNL WHERE ALREADY UPDATED self.DF! try to remove next time #XXX same thing!
        self.df = self.select_last_trade()
        # print(self.symbol, self.df['symbol'].iloc[0])
        self.df['inPossition'] = 0
        self.df['eventEnd'] = Time.get_timestamp()
        last_fee = self.df['quantity'].iloc[0]*self.df['close_price'].iloc[0]*(1-self.fee_market)
        # self.df['fee'] += self.df['quantity'].iloc[0]*self.df['close_price'].iloc[0]*(1-self.fee_market)
        # self.df['pnl_profit'] -= self.df['fee'].iloc[0]
        

        #XXX self.df['amount'].iloc[0] maybe it should be quantity * finalPrice????? for proper calc new balance///
        self.result_balance = self.df['amount'].iloc[0]+self.df['pnl_profit'].iloc[0]+self.balance + self.df['fee'].iloc[0] - last_fee
        
        
        # self.result_balance = self.df['quantity'].iloc[0]*self.df['close_price'].iloc[0]+self.df['balance'].iloc[0]
        self.update_balace(self.result_balance)
        self.update_status(0)
        self.df['balance'] = self.balance
        self.df['fee'] += last_fee
        self.df['pnl_profit'] -= last_fee
        query = f"update {self.trades_table} set eventTime=?,eventEnd=?,symbol=?,open_price=?,average_price=?,close_price=?,\
                quantity=?,amount=?,side=?,balance=?,\
                pnl_percentage=?,pnl_profit_part=?,pnl_profit=?,fee=?,inPossition=?,order_count=?,tp=?,sl=?,tp_trail=?,sl_trail=? where eventTime={self.df['eventTime'].iloc[0]}"
        ##XXX И ПОХОДУ СИЛЬНО ДОХУЯ ОБНОВ self.df vvvvvvvvvvvvvvvvvvvv А не ЭТО ФИНАЛЬНАЯ ОБНОВА ТУТ ВсЕ ОК
        self.execute(self.query_update_trade, tuple(self.df.values[0]))
        print(f'*********************[Possition {self.side} {self.symbol} closed!]********************* \n\t \
            [PNL]:{self.df["pnl_profit"].iloc[0]:.2f}$ {self.pnl_percentage:.2f}%\n***************************************************************************')
        return True
        
    def get_trades(self, limit=None,*,symbol=None,status: int = None):
        if not symbol and not limit:
            # self.trades_list = self.cursormany(f"select * from {self.trades_table}").fetchall()
            self.df = pd.read_sql(f"select * from {self.trades_table}", self.db)
            self.df['eventTime'] += 60000*60*3
            self.df['eventTime'] = pd.to_datetime(self.df['eventTime'], unit='ms')
            # self.df['eventEnd'] = pd.to_datetime(self.df['eventEnd'], unit='ms')
            # print(self.df)
            # return self.df
        if status == 0 or status == 1:
            # self.trades_list = self.cursormany(f"select * from {self.trades_table}").fetchall()
            self.df = pd.read_sql(f"select * from {self.trades_table} where inPossition={status}", self.db)
            self.df['eventTime'] += 60000*60*3
            self.df['eventTime'] = pd.to_datetime(self.df['eventTime'], unit='ms')
            self.df['eventEnd'] = pd.to_datetime(self.df['eventEnd'], unit='ms')
            # print(self.df)
            # return self.df
        if limit:
            query = f"select * from {self.trades_table} order by rowid desc limit {limit}"
            # self.trades_list = self.cursormany(query).fetchall()
            self.df = pd.read_sql(query, self.db)
            self.df['eventTime'] += 60000*60*3
            self.df['eventTime'] = pd.to_datetime(self.df['eventTime'], unit='ms')
            self.df['eventEnd'] = pd.to_datetime(self.df['eventEnd'], unit='ms')
            # print(self.df)
            # return self.df
        return self.df
        # self.trades_list = self.cursormany(f"select * from {self.trades_table} where symbol='{self.symbol}'").fetchall()
        # self.df = pd.read_sql(f"select * from {self.trades_table} where symbol='{self.symbol}'", self.db)
        # print(self.df.T)
        # return self.df.T

