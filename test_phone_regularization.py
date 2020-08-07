#!/usr/bin/env python
# coding: utf-8

__author__ = "Cindy Lee"
__email__ = "cindyl.intern@fubon.com"
__date__ = "20200805"

import re
#STEP1 全形轉半形
def UP1(ustring): 
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全形空格直接轉換
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全形字元（除空格）根據關係轉化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

#STEP2 去掉首+尾/首/尾都是符號(可能不只一碼)
def UP2(ustring):
    s = ustring
    for j in ustring[0:]:
        if j.isdigit() == False:  #首
            s = s.lstrip(j)
        else: break        
    for i in s[::-1]:
        if i.isdigit() == False:
            s = s.rstrip(i)
        else: break
    return s

#STEP3 判斷分機欄位
def UP3(ustring):
    count_sym = 0
    sym_list = []
    str_split = []
    check_ext = False
    junk_sym = ''
    
    def delete_junk(str_list, junk_sym):
        for a in str_list:
            if a == junk_sym:
                str_split.remove(junk_sym)

    for i in ustring:
        if i.isdigit() == False:
            count_sym+=1
            sym_list.append(i) #存下符號
    #符號數量=1
    if count_sym == 1: 
        str_split = ustring.split(sym_list[0])
        if (len(str_split[1]) < len(str_split[0])):
            check_ext = True #確認是否有分機
            delete_junk(str_split, junk_sym)
            return str_split, check_ext
        else: return ustring, check_ext
    #符號數量=2
    elif count_sym == 2 and sym_list[1] != '-':
        #str_split = ustring.split(sym_list[0])
        str_split = re.split(r'[\W]',ustring)  
        if  ((len(str_split[2]) < (len(str_split[0]) + len(str_split[1])))):
            check_ext = True #確認是否有分機
            delete_junk(str_split, junk_sym)
            return str_split, check_ext
        else: return ustring, check_ext
    #符號數量=3
    elif count_sym == 3:
        str_split = re.split(r'[\W]',ustring)
        if  ((len(str_split[3]) < (len(str_split[0]) +  len(str_split[1]) +  len(str_split[2])))):
            check_ext = True #確認是否有分機
            delete_junk(str_split, junk_sym)
            return str_split, check_ext
    else: return ustring, check_ext

#STEP3_1 判斷有無分機 / 整理號碼
def UP3_1(phone_num_list, check_ext): 
   # phone_num_list, check_ext = UP3(test3)
    phone_num = ''
    phone_len = 0
    first = ''
    if (len(phone_num_list[0]) == 5 or len(phone_num_list[0]) == 6 or len(phone_num_list[0]) == 7 or len(phone_num_list[0]) == 8): #沒有區碼有分機
        phone_num = phone_num_list[0]
    elif (len(phone_num_list[0]) == 9 or len(phone_num_list[0])) == 10: #有區碼有分機（區碼與電話無間隔）
        phone_num = phone_num_list[0]
    #改這
    elif len(phone_num_list[1]) == 5 or len(phone_num_list[1]) == 6 or len(phone_num_list[1]) == 7 or len(phone_num_list[1]) == 8: #有區碼有分機（區碼與電話有間隔）
        for i in range(0,2):
            phone_num += phone_num_list[i]
    elif ((len(phone_num_list[1]) == 4 and len(phone_num_list[2]) == 4) or (len(phone_num_list[1]) == 3 and len(phone_num_list[2])) == 4): #有區碼有分機（多間隔）
        for i in range(0,3):
            phone_num += phone_num_list[i]
    else:
        first = str(phone_num_list[0])
        if first[:2] == '09':
            for i in phone_num_list:
                phone_len += len(i)
                if phone_len == 10:
                    for i in range(len(phone_num_list)):
                        phone_num += phone_num_list[i]
    return phone_num

#STEP4 判斷手機-完整長度10碼
def UP4(ustring):
    phone_num = ""
    phone_num = "".join(filter(str.isdigit, ustring))
    if (phone_num[0]+phone_num[1] == "09") and (len(phone_num) == 10):
        return phone_num
    elif (phone_num[0]+phone_num[1] == "09") and (len(phone_num) != 10):
        return None
    else: return ustring

#STEP5 判斷手機-補0
def UP5(ustring):
    phone_num = ""
    if ustring != None:
        phone_num = "".join(filter(str.isdigit, ustring))
        if phone_num[0] == '9':
            phone_num = '0' + phone_num
        elif phone_num[0:4] == '8869':
            phone_num = '0' + phone_num[3:]
        elif phone_num[0:5] == '88609':
            phone_num = phone_num[3:]
        if phone_num[:2] == '09' and len(phone_num) != 10:
            phone_num = None
        return phone_num
    else: return None
 
#STEP6+7 判斷空值
def UP6_7(ustring):
    if ustring != None: return ustring
    elif ustring == None: return None           #輸入空值
    else:
        for i in ustring:
            if i.isdigit() == False: return None #輸入全為非數字

#STEP8 判斷長度不足
def UP8(ustring):
    phone_num = ""
    if ustring != None:
        phone_num = "".join(filter(str.isdigit, ustring))
        if len(phone_num) < 6:
            return None
        else: return ustring
    else: return None

#STEP9 判斷市無分機 / 區碼並回傳正規後號碼
def UP9(ustring):
    if ustring != None:
        result = ''
        sym_list = []
        index_list = []
        count_sym = 0
        count_digit = 0
        count_index = -1
        phone_num = ustring
        temp_phone=[]

        #補符號/刪符號
        def add_str(count_sym, sym_list, temp_phone, phone_num, index_list):
            temp = ''
            if count_sym == 2 and sym_list[1] == '-':
                temp_phone =  phone_num.split('-')
                phone_num = temp_phone[0] + '-' + temp_phone[1] + temp_phone[2]
            elif count_sym == 1 and (sym_list[0] == '~' or sym_list[0] == ')'):
                i = index_list[0]
                temp = phone_num.replace(phone_num[i], '-')
                phone_num = temp
            elif (count_sym == 1 and sym_list[0] == '-') or count_sym == 0:
                phone_num = phone_num
            return phone_num
        for i in phone_num:
            count_index += 1
            if i.isdigit() == False:
                index_list.append(count_index)
                count_sym += 1
                sym_list.append(i)
            else: count_digit += 1
        #台北02
        if phone_num[:2] == '02':
            if count_digit == 10:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:2] + '-' + result[2:]
                elif  index_list[0] == 3:
                    temp = result.replace(result[3], '')
                    result = temp
                    result = result[:2] + '-' + result[2:]
            else: return None
        #苗栗/037
        elif phone_num[:3] == '037':
            if count_digit == 9:
            #print("yeee")
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:3] + '-' + result[3:]
            else: return None
        #桃園/新竹/花蓮/宜蘭/03
        elif phone_num[:2] == '03':
            if count_digit == 9:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:2] + '-' + result[2:]
            else: return None
        #南投/049
        elif phone_num[:3] == '049':
            if count_digit == 10:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:3] + '-' + result[3:]
            else: return None
        #彰化/04(9碼) #台中/04(10碼)
        elif phone_num[:2] == '04':
            if count_digit == 9 or count_digit == 10:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:2] + '-' + result[2:]
            else: return None
        #嘉義雲林/05
        elif phone_num[:2] == '05':
            if count_digit == 9:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:2] + '-' + result[2:]
            else: return None
        #台南澎湖/06
        elif phone_num[:2] == '06':
                if count_digit == 9:
                    result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                    if count_sym == 0:
                        result = result[:2] + '-' + result[2:]
                else: return None
        #高雄/07
        elif phone_num[:2] == '07':
            if count_digit == 9:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:2] + '-' + result[2:]
            else: return None
        #馬祖/0836
        elif phone_num[:4] == '0836':
            if count_digit == 9:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:4] + '-' + result[4:]
            else: return None
         #金門/082
        elif phone_num[:3] == '082':
            if count_digit == 9:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:3] + '-' + result[3:]
            else: return None
        #台東/089
        elif phone_num[:3] == '089':
            if count_digit == 9:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:3] + '-' + result[3:]
            else: return None
        #屏東/08
        elif phone_num[:2] == '08':
            if count_digit == 9:
                result = add_str(count_sym, sym_list, temp_phone, phone_num, index_list)
                if count_sym == 0:
                    result = result[:2] + '-' + result[2:]
            else: return None
        elif phone_num[:2] == '09' and count_digit == 10:
            result = phone_num
        elif len(phone_num) > 8:
            return None
        else:  result = phone_num
        return result
    else: return None

#執行所有函式
def run(ustring):
    final =''
    a = UP2(ustring)
    x, y = UP3(a)
    if y == True:
        b = UP3_1(x, y)
        c = UP4(b)
        d = UP5(c)
        e = UP6_7(d)
        f = UP8(e)
        g = UP9(f)
        if g[:2] != '09':
            final = g + '~' + x[-1]
        else: final = g
    else:
        c = UP4(x)
        d = UP5(c)
        e = UP6_7(d)
        f = UP8(e)
        g = UP9(f)
        final = g 
    return final

#main
if __name__=='__main__':
#test cases
    """
    test = '0222692266'
    test1 = '0978-005-517'
    test2 = '087664582'
    test3 = '08-7334582#123'
    test4 = '04-2481-1518-205'
    test5 = '-3734916'
    test6 = '037-622848'
    test7 = '0392170476'#None
    test8 = '0972--006-602'
    test9 = '0935-97-87-47'
    test10 = '023-3667352'
    test11 = '0926-4565' #None
    test12 = '090-524-231' #None
    test13 = '093739269' #None
    test14 = '5713410'#沒區碼的
    test15 = '3316-6047'#沒區碼的
    test16 = '410'
    test17 = '0836760186' #None
    test18 = '0836-23855'
    test19 = '5713410#123'
    test20 = '0-0-'
    test21 = '0836-26078#125'
    test22 = '082-333274*610'
    test23 = '57134 10'
    test24= '07-8118198*101'
    test25 = '03-5163276*55606'
    test26 = '604-303-0595'
    test27 = '+886978005517'
    test28 = '033750496'
    test29 = '12345467.0978005517'
    test30 = '07-020001#4836'
    """

    while(1):
        try:
            test_input = input('input a phone number:')
            if test_input == 'end':
                break
            else:
                #test_input = raw_input('input a phone number:')
                #test_input = '0222692266'
                print(run(test_input))
        except:
            print("None")
        #test_input = "0222692266"
        #print(run(test_input))'
