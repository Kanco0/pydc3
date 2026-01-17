<p align="center"><b>2026/01/17</b></p>

<h1 align="center">📊 Dataset:
  E-Commerce
</h1>
<h2 align="center">📌 Project Summary: Retail Data Audit & Cleanup</h2>

The Problem: Over 500k rows of raw e-commerce data were unusable due to encoding errors, negative quantities (up to -80k), missing prices, and "Guest" transactions without IDs.

The Fix: I restored missing info using StockCode mapping, filtered out impossible outliers (negative values), and standardized product descriptions. I also converted timestamps into actionable Time/Day/Month columns.

The Result: A 100% clean, analysis-ready dataset with a new Total_Sales column, allowing the business to accurately track revenue and peak shopping hours.
<hr>
<h3 align="center">Encoding Fix</h3>

First thing is to change the encoding to <code>ISO-8859-1</code> because the data is so old, therefore it’s not gonna work for us.  
(I tried without this and it showed some weird errors).

<hr>
<h3 align="center">Inspecting Columns & Initial Statistics</h3>

Next is to see the columns to know what I am working with.  
After that, I used <code>.info()</code> to get non-null counts and the column data storing type.  
I saw 2 columns where a lot of values were supposed to be numbers, but the app stored them as <code>float</code> or <code>object</code> due to empty cells.  

After that, I used <code>.describe()</code> on <code>Quantity</code> and <code>UnitPrice</code> as both are connected.  

I saw the quantity reached <code>-80.995</code>.  
This could mean an error in entering data or a huge cancellation.  

Same for <code>UnitPrice</code>, it reached <code>-11.062.06</code>.  
There is no product that is minus in trade logic, which means wrong changes or calculation mistakes.  

For now, I am still confused, so I used <code>df['Quantity'] &lt; 0</code>, which means look and print any value that's under 0.  
Pipe line means "or".  
Same thing done for <code>UnitPrice</code>.
<hr>
<h3 align="center">Removing Outliers for Net Sales Calculation</h3>

As now depends on the task type, but for me I want to calculate Net Sales, so I need to get rid of these outliers.  
I’d make a new line, but unlike the last one, I will call it <code>clean</code> and instead of <code>&gt;0</code> I will also use <code>&gt;0</code> for safety.  

After that, I used <code>df.shape</code> and <code>clean.shape</code> so I could know how many lines we got read off.  
It shows that the number changed from 514k to 530k, which means 11k rows were containing some type of outliers.  

Now thanks to the <code>.describe()</code> method, I can better understand the distribution of the cleaned data.
<hr>
<h3 align="center">Inspecting Minimum Values and Very Cheap Items</h3>

I can see that the min is now 1 instead of minus, which makes kinda some sense,  
but I’m still suspicious about <code>UnitPrice</code> min. It says 0.001, which is weird.  

Is it some low prices that get shipped for free as small samples, or gifts?  
Probably the system doesn’t allow a price of "0", or the low price is due to some big sales.  

To make sure, I used <code>very_cheap</code> and made sure to print anything below <0.1.  
Checking made sense since I found this:  

<code>91772   ESSENTIAL BALM 3.5g TIN IN ENVELOPE      2400      0.060</code>.
<hr>
<h3 align="center">Fixing <code>InvoiceDate</code> and Creating Time-Based Columns</h3>

For the <code>InvoiceDate</code>, I noticed it was an object, not a datetime.
By using <code>pd.to_datetime()</code>, I converted it from object to date type,
and it’s now visible in a beautiful universal format (year/month/day).

Next, I created 3 new columns:

The first one is <code>Month</code> to know which month had the highest sales.

The second is <code>Day_Name</code> to see if people shop more on weekends.

The third is <code>Hour</code> to identify what time customers buy most — morning or evening.

This makes the dataset ready for analyzing revenues and patterns.
<hr>
<h3 align="center">Cleaning <code>Description</code> and Handling Missing Data</h3>

I cleaned the <code>Description</code> column by converting all text to uppercase and removing extra spaces using <code>.strip()</code>.
This ensures that products like 'lunch bag' and 'LUNCH BAG' are counted as the same item, which makes the 'Top 10 Products' list accurate (if it existed, of course).

Next, I tackled missing values in <code>Description</code> and <code>UnitPrice</code> using a two-step recovery process:

Filled missing values by cross-referencing their <code>StockCode</code> with the rest of the dataset.

Any remaining rows that still lacked both <code>Description</code> and <code>UnitPrice</code> were permanently removed, as they had no analytical value.

After re-checking with <code>.info()</code>, I could see that most of the cleaning work was done.

For fun, I added a new column called <code>Total_Sales</code> by multiplying <code>Quantity</code> with <code>UnitPrice</code>, giving the full price for each transaction.

As a test, I performed <code>value_counts()</code> on the new <code>Hour</code> column.
This allowed me to see the distribution of orders throughout the day and identify peak shopping hours for the store.
<hr>
<h3 align="center">Handling Missing <code>CustomerID</code> Values</h3>

While checking <code>.info()</code>, I noticed that <code>CustomerID</code> had only 397K entries, while the rest of the columns had exactly 530,104 rows.

This likely means a few things:

Some rows correspond to customers who purchased without an account.

Or there could have been a data collection issue (hopefully not).

I decided not to overthink it. The solution was simple:

Fill missing <code>CustomerID</code> values with 0, leaving a note in the code that 0 means no customer ID.

Convert the column type from <code>float64</code> to int, since customer IDs are whole numbers.

This ensures the dataset is consistent and ready for analysis without introducing false data.
