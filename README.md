# International-Tax-Calculator
International-Tax-Calculator

I created an International Tax Calculator app where the user can input a gross salary and the app will output net pay & tax rate for several countries. The app is created using Flask, Python, HTML, CSS and Bootstrap.

The purpose of the app is to be an easy way for people to get apples-to-apples comparisons between salaries in different countries as net pay after tax can vary significantly.

The templates folder contains a base html template as well as index.html which is the home page where the user chooses the currency and enters gross pay. output.html will then who a table with the included countries
and the net pay & tax rate for each of them by taking the user-inputted salary and feeding it into several Python functions in app.py for each country. The calculations are based on official tax brackets.

static includes a styles.css file, however most of the styling is achieved via Bootstrap. The 'other' folder contains sources used for tax calculations.

The limitaion of this app is that I had to make simplifying assumptions to account for the fact that tax codes are extremely complex. This calculator will not be applicable for married proplr, for example, although
it should still give a reasonable estimate of the relative differences between countries.

Another limitation is that the tax brackets and other numbers will have to be updated each year.

Over time, I will be expanding this with more countries, and I also plan to ad cost-of-living data.
