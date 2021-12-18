from flask import Flask, redirect, render_template, request, url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from forex_python.converter import CurrencyRates

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template('index.html')
    
    else:

        c = CurrencyRates()

        # Ensure salary was submitted
        if not request.form.get("salary"):
            return 1

        try:
            whatever = float(request.form.get("salary"))
        except:
            return 1

        if int(request.form.get("salary")) < 1:
            return 1

        salary = float(request.form.get("salary"))

        currency = request.form.get("currency")

        entries = []

        def UK(salary):
            #convert currency
            salary = c.convert(currency, 'GBP', salary)

            #income tax

            #personal allowance

            if salary <= 100000:
                persallowance = 12570

            else:
                persallowance = 12570 - (salary - 100000)/2    

            if persallowance < 0:
                persallowance = 0

            if salary <= persallowance:
                inctax = 0

            elif persallowance < salary <= 50270:
                inctax = (salary - persallowance) * 0.2

            elif 50270 < salary <= 150000:
                inctax = (50270 - persallowance) * 0.2 + (salary - 50270) * 0.4

            else:
                inctax = (50270 - persallowance) * 0.2 + (150000 - 50270) * 0.4 + (salary - 150000) * 0.45

            #national insurance

            if salary <= (12 * 797):
                natins = 0

            elif (12 * 797) < salary <= (12 * 4189):
                natins = 0.12 * (salary - (12 * 797))

            else:
                natins = 0.12 * ((12 * 4189) - (12 * 797)) + 0.02 * (salary - (12 * 4189))

            #total tax

            tax = inctax + natins
            netpay = salary - tax
            taxrate = tax / salary

            #print('UK Tax Rate: ', taxrate)
            #print('UK Net Pay: ', c.convert('GBP', 'USD', netpay))

            UK = {
                "country": "United Kingdom",
                "netpay": c.convert('GBP', currency, netpay),
                "taxrate": taxrate
            }

            entries.append(UK)

            return 0

        def France(salary):
            #convert currency

            salary = c.convert(currency, 'EUR', salary)

            #LA DÉDUCTION FORFAITAIRE (a 10% deduction, or maximum eur12,652)

            ded = salary * 0.1

            if ded > 12652:
                ded = 12652
            

            #social contributions

            contr = 0

            #securite sociale (assurance vieillesse)

            contr = contr + salary * 0.004

            if salary > 12 * 3428:
                contr = contr + (12 * 3428) * 0.069
            
            else:
                contr = contr + salary * 0.069

            #CSG/CRDS

            if 0.9825 * salary > 164544:
                csg = 0.9825 * salary * 0.092 + (salary - 164544) * 0.092

            else:
                csg = 0.9825 * salary * 0.092

            if 0.9825 * salary > 164544:
                crds = 0.9825 * salary * 0.005 + (salary - 164544) * 0.005

            else:
                crds = 0.9825 * salary * 0.005

            contr = contr + crds + csg

            #retraite complementaire

            if salary > 12 * 27424:
                contr = contr + 12 * (27424 - 3428) * 0.0986 + 12 * 3428 * 0.0401

            elif 12 * 27424 >= salary > 12 * 3428:
                contr = contr + 12 * ((salary/12) - 3428) * 0.0986 + 12 * 3428 * 0.0401    

            else:
                contr = contr + salary * 0.0401 

            #deducted salary from which income tax is calculated

            dedsalary = salary - ded - (contr - crds - (2.4/9.2) * csg)

            #income tax

            if dedsalary <= 10084:
                inctax = 0

            elif 10084 < dedsalary <= 25710:
                inctax = (dedsalary - 10084) * 0.11

            elif 25710 < dedsalary <= 73516:
                inctax = (25710 - 10085) * 0.11 + (dedsalary - 25711) * 0.3

            elif 73517 < dedsalary <= 158122:
                inctax = (25710 - 10085) * 0.11 + (73516 - 25711) * 0.3 + (dedsalary - 73517) * 0.41

            else:
                inctax = (25710 - 10085) * 0.11 + (73516 - 25711) * 0.3 + (158122 - 73517) * 0.41 + (dedsalary - 158122) * 0.45



            taxrate = (inctax + contr) / salary
            netpay = salary - (inctax + contr)

            #print('France Tax Rate: ', taxrate)
            #print('France Net Pay: ', c.convert('EUR', 'USD', netpay))

            france = {
                "country": "France",
                "netpay": c.convert('EUR', currency, netpay),
                "taxrate": taxrate
            }

            entries.append(france)

            return 0

        def USA(salary, state, city):

            #convert currency

            salary = c.convert(currency, 'USD', salary)

            #federal taxes (assuming standard deduction!)

            federal = 0

            #salary minus standard deduction

            dedsalary = salary - 12950

            if dedsalary < 0:
                federal = 0

            elif dedsalary < 10275:
                federal = 0.1 * dedsalary

            elif 10275 <= dedsalary < 41775:
                federal = 1027.5 + 0.12 * (dedsalary - 10275)

            elif 41775 <= dedsalary < 89075:
                federal = 4807.5 + 0.22 * (dedsalary - 41775)

            elif 89075 <= dedsalary < 170050:
                federal = 15213.5 + 0.24 * (dedsalary - 89075)

            elif 170050 <= dedsalary < 215950:
                federal = 34647.5 + 0.32 * (dedsalary - 170050) 

            elif 215950 <= dedsalary < 539900:
                federal = 49335.5 + 0.35 * (dedsalary - 215950)  

            elif dedsalary >= 539900:
                federal = 162718 + 0.37 * (dedsalary - 539900)  

            #fica

            if salary <= 147000:
                fica = 0.0765 * salary

            elif 147000 < salary <= 200000:
                fica = 0.062 * 147000 + 0.0145 * salary

            elif salary > 200000:
                fica = 0.062 * 147000 + 0.0145 * 200000 + 0.0235 * (salary - 200000)       

            #state taxes

            def NY(city):

                #standard deduction

                dedsalary = salary - 8000

                if dedsalary < 0:
                    state = 0

                elif dedsalary < 8500:
                    state = 0.04 * dedsalary

                elif 8500 <= dedsalary < 11700:
                    state = 340 + 0.045 * (dedsalary - 8500)

                elif 11700 <= dedsalary < 13900:
                    state = 484 + 0.0525 * (dedsalary - 11700)            

                elif 13900 <= dedsalary < 21400:
                    state = 600 + 0.059 * (dedsalary - 13900)  

                elif 21400 <= dedsalary < 80650:
                    state = 1042 + 0.0609 * (dedsalary - 21400)            

                elif 80650 <= dedsalary < 215400:
                    state = 4650 + 0.0641 * (dedsalary - 80650)  

                elif 215400 <= dedsalary < 1077550:
                    state = 13288 + 0.0685 * (dedsalary - 215400)            

                elif dedsalary >= 1077550:
                    state = 72345 + 0.0882 * (dedsalary - 1077550)

                #local tax

                def NYC():

                    if salary < 12000:
                        local = 0.03078 * salary

                    elif 12000 <= salary < 25000:
                        local = 369 + 0.03762 * (salary - 12000)   

                    elif 25000 <= salary < 50000:
                        local = 858 + 0.03819 * (salary - 25000)                         

                    elif salary >= 50000:
                        local = 1813 + 0.03876 * (salary - 50000)

                    return local

                #total state + local

                if city == 'NYC':
                    total = state + NYC()

                else:
                    print('ERROR')
                    return 1

                return total

            def CA(city):

                #standard deduction

                dedsalary = salary - 4601

                if dedsalary < 0:
                    state = 0

                elif dedsalary < 8932:
                    state = 0.01 * dedsalary

                elif 8932 <= dedsalary < 21175:
                    state = 89.32 + 0.02 * (dedsalary - 8932)

                elif 21175 <= dedsalary < 33421:
                    state = 334.18 + 0.04 * (dedsalary - 21175)            

                elif 33421 <= dedsalary < 46394:
                    state = 824.02 + 0.06 * (dedsalary - 33421)  

                elif 46394 <= dedsalary < 58634:
                    state = 1602.4 + 0.08 * (dedsalary - 46394)            

                elif 58634 <= dedsalary < 299508:
                    state = 2581.6 + 0.093 * (dedsalary - 59634)  

                elif 299508 <= dedsalary < 359407:
                    state = 24982.88 + 0.103 * (dedsalary - 299508)            

                elif 359407 <= dedsalary < 599012:
                    state = 31152.48 + 0.113 * (dedsalary - 359407)

                elif dedsalary >= 599012:
                    state = 58227.85 + 0.123 * (dedsalary - 599012)

                return state     


            #federal + state + local

            if state == 'NY' and city == 'NYC':
                inctax = federal + NY(city)
                statename = 'New York'

            elif state == 'CA':
                inctax = federal + CA(city)
                statename = 'California'

            elif state == 'TX':
                inctax = federal
                statename = 'Texas'          
        

            else:
                print('ERROR')
                return 1    


            taxrate = (inctax + fica) / salary
            netpay = salary - (inctax + fica)

            USA = {
                "country": "United States (" + statename + ")",
                "netpay": c.convert('USD', currency, netpay),
                "taxrate": taxrate
            }

            entries.append(USA)    

            return 0  

        def Canada(salary, state):

            #convert currency

            salary = c.convert(currency, 'CAD', salary)

            #federal taxes

            federal = 0

            if salary < 49020:
                federal = 0.15 * salary

            elif 49020 <= salary < 98040:
                federal = 7353 + 0.205 * (salary - 49020)

            elif 98040 <= salary < 151978:
                federal = 17402.1 + 0.26 * (salary - 98040)

            elif 151978 <= salary < 216511:
                federal = 31425.98 + 0.29 * (salary - 151978) 

            elif salary >= 216511:
                federal = 50140.55 + 0.33 * (salary - 216511)

            #federal basic personal tax credit

            if salary <= 150473:
                credit = 0.15 * 13229

            elif salary >= 214368:
                credit = 0.15 * 12298

            else:
                base = 12298
                additional = 931 - (((salary - 150473) / 63895) * 931)
                credit = 0.15 * (base + additional)

            federal = federal - credit  

            #CPP

            if salary < 3500:
                cpp = 0

            elif 3500 <= salary < 64900:
                cpp = 0.0545 * (salary - 3500) 

            elif salary >= 64900:
                cpp = 0.0545 * (64900 - 3500)

            #EI

            if salary < 56300:
                ei = 0.0158 * salary

            else:
                ei = 0.0158 * 56300    


            #provincial taxes

            def Ontario():

                if salary < 45142:
                    provincial = 0.0505 * salary

                elif 45142 <= salary < 90287:
                    provincial = 0.0505 * 45142 + 0.0915 * (salary - 45142)        

                elif 90287 <= salary < 150000:
                    provincial = 0.0505 * 45142 + 0.0915 * (90287 - 45142) + 0.1116 * (salary - 90287)

                elif 150000 <= salary < 220000:
                    provincial = 0.0505 * 45142 + 0.0915 * (90287 - 45142) + 0.1116 * (150000 - 90287) + 0.1216 * (salary - 150000)

                elif 220000 <= salary:
                    provincial = 0.0505 * 45142 + 0.0915 * (90287 - 45142) + 0.1116 * (150000 - 90287) + 0.1216 * (220000 - 150000) + 0.1316 * (salary - 220000)

                #Ontario tax credit

                credit = 0.0505 * 10783

                provincial = provincial - credit

                return provincial

            def BC():

                if salary < 43070:
                    provincial = 0.0506 * salary

                elif 43070 <= salary < 86141:
                    provincial = 0.0506 * 43070 + 0.0770 * (salary - 43070)        

                elif 86141 <= salary < 98901:
                    provincial = 0.0505 * 43070 + 0.0770 * (86141 - 43070) + 0.1050 * (salary - 86141)

                elif 98901 <= salary < 120094:
                    provincial = 0.0505 * 43070 + 0.0770 * (86141 - 43070) + 0.1050 * (98901 - 86141) + 0.1229 * (salary - 98901)

                elif 120094 <= salary < 162832:
                    provincial = 0.0505 * 43070 + 0.0770 * (86141 - 43070) + 0.1050 * (98901 - 86141) + 0.1229 * (120094 - 98901) + 0.147 * (salary - 120094)

                elif 162832 <= salary < 227091:
                    provincial = 0.0505 * 43070 + 0.0770 * (86141 - 43070) + 0.1050 * (98901 - 86141) + 0.1229 * (120094 - 98901) + 0.147 * (162832 - 120094) + 0.168 * (salary - 162832)

                elif 227091 <= salary:
                    provincial = 0.0505 * 43070 + 0.0770 * (86141 - 43070) + 0.1050 * (98901 - 86141) + 0.1229 * (120094 - 98901) + 0.147 * (162832 - 120094) + 0.168 * (227091 - 162832) + 0.205 * (salary - 227091)

                #British Columbia tax credit

                credit = 0.0506 * 11302

                provincial = provincial - credit

                return provincial

            #total

            if state == 'ON':
                inctax = federal + Ontario()
                statename = 'Ontario'

            elif state == 'BC':
                inctax = federal + BC()
                statename = 'British Columbia'

            else:
                print('ERROR')
                return 1    

            taxrate = (inctax + cpp + ei) / salary
            netpay = salary - (inctax + cpp + ei)

            canada = {
                "country": "Canada (" + statename + ")",
                "netpay": c.convert('CAD', currency, netpay),
                "taxrate": taxrate
            }

            entries.append(canada) 
            
            return 0 

        def Finland(salary):

            #convert currency
            salary = c.convert(currency, 'EUR', salary)

            #Työttömyysvakuutusmaksu (unemployment insurance)

            tyva = 0.014 * salary

            # tyontekijan elakemaksu (pension insurance)

            tyoel = 0.0715 * salary

            # sairausvakuutusmaksu (medical insurance)

            if salary > 14766:
                med = salary * 0.0136

            else:
                med = 0    

            # tulonhankkimisvahennys (standard deduction)

            ded = 750

            #state income tax

            dedsalary = salary - ded - med - tyoel - tyva

            if salary <= 19200:
                state = 0

            elif 19200 < salary <= 28700:
                state = 8 + 0.06 * (salary - 19200)

            elif 28700 < salary <= 47300:
                state = 578 + 0.1725 * (salary - 28700)

            elif 47300 < salary <= 82900:
                state = 3786.5 + 0.2125 * (salary - 47300)

            elif salary > 82900:
                state = 11351.5 + 0.3125 * (salary - 82900)

            #tyotulovahennys (tax credit)

            credit = 0.122 * (salary - 3500)

            if credit > 1840:
                credit = 1840

            if (salary - ded) > 33000:
                credit = credit - ((salary - ded) - 33000) * 0.0189

            state = state - credit

            # Yle tax

            yle = 0.025 * ((salary - ded) - 14000)

            if yle > 163:
                yle = 163

            # municipal tax (assuming Helsinki)

            #municipal tax deductions

            if 7230 >= salary > 2500:
                ded1 = 0.51 * (salary - 2500)

            elif salary > 7230:
                ded1 = 0.51 * (7230 - 2500) + 0.28 * (salary - 7230)

            if ded1 > 3570:
                ded1 = 3570

            if salary > 14000:
                ded1 = ded1 - (salary - 14000) * 0.045

            if ded1 < 0:
                ded1 = 0

            if (salary - ded - ded1 - tyoel - tyva - med) <= 3305:
                ded2 = (salary - ded1)

            else:
                ded2 = 3305 - 0.18 * (salary - ded - ded1 - tyoel - tyva - med)

            if ded2 < 0:
                ded2 = 0

            municipal = (salary - tyoel - tyva - med - ded1 - ded2) * 0.18    

            #total tax

            tax = state + tyoel + med + tyva + yle + municipal
            netpay = salary - tax
            taxrate = tax / salary

            finland = {
                "country": "Finland",
                "netpay": c.convert('EUR', currency, netpay),
                "taxrate": taxrate
            }

            entries.append(finland)

            return 0     

        UK(salary)
        France(salary)
        Finland(salary)
        USA(salary,'NY','NYC')
        USA(salary,'CA','SF')
        USA(salary,'TX','AU')  
        Canada(salary,'ON')
        Canada(salary,'BC')

        # convert pay to selected currency format
        if currency == "USD":
            salary = "US${:,.2f}".format(salary)
            for entry in entries:
                entry["netpay"] = "US${:,.2f}".format(entry["netpay"])

        elif currency == "GBP":
            salary = "£{:,.2f}".format(salary)
            for entry in entries:
                entry["netpay"] = "£{:,.2f}".format(entry["netpay"])

        elif currency == "CAD":
            salary = "CA${:,.2f}".format(salary)
            for entry in entries:
                entry["netpay"] = "CA${:,.2f}".format(entry["netpay"]) 

        elif currency == "EUR":
            salary = "€{:,.2f}".format(salary)
            for entry in entries:
                entry["netpay"] = "€{:,.2f}".format(entry["netpay"]) 

        # convert Tax Rate to % format

        for entry in entries:
            entry["taxrate"] = "{:.0%}".format(entry["taxrate"])         

        return render_template("output.html", entries = entries, salary=salary)          

if __name__ == '__main__':
    app.run(debug = True)   