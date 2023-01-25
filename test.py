import pymysql


def faq_db():
    sql = 'SELECT product_name FROM product_info;'
    menu_db = exe_db_smartstore(sql)

    sql = 'CALL get_ordered_customer_db;'
    ordered_customer = exe_db_smartstore(sql)

    sql = 'CALL get_non_ordered_customer_db;'
    not_ordered_customer = exe_db_smartstore(sql)

    return menu_db, ordered_customer, not_ordered_customer

def exe_db_smartstore(sql):
    conn = pymysql.connect(host='10.10.21.106', port=3306, user='root', password='1q2w3e4r',
                           db='project7smartstore')
    c = conn.cursor()

    c.execute(sql)
    conn.commit()
    loaded = c.fetchall()

    c.close()
    conn.close()

    return loaded

a = faq_db()
print(a)
