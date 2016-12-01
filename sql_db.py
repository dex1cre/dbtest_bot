# -*- coding: utf-8 -*-

import sqlite3 as sq

def sql_rq(sql_code, conn):             #rq - reqyest  - запрос
    cur = conn.cursor()                 #создаём объект-курсор
    if "INSERT" in sql_code or "UPDATE" in sql_code:
        cur.execute(sql_code)           #принимает только один SQL запрос
        cur.commit()
    else:
        p = cur.execute(sql_code)       #принимает только один SQL запрос
        return p
