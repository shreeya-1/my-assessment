"""
The database loan.db consists of 3 tables: 
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data
    
You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

"""


def question_1():    
    
    #Make use of a JOIN to find out the `AverageIncome` per `CustomerClass`

    #per = group by customerClass, sums income then divides by number of customers in that class

    qry = """ SELECT CustomerClass, (SUM(customers.Income)/ COUNT (*)) AS AverageIncome 
              FROM customers JOIN credit ON customers.CustomerID = credit.CustomerID
              GROUP BY credit.CustomerClass """
    
    return qry



def question_2():    
    
    #Q2: Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'. 

    # groups by province and then counts number of applications that meet the "rejected" criteria
    qry = """  SELECT  customers.Region AS Province, COUNT(*) AS RejectedApplications
               FROM loans JOIN customers ON loans.CustomerID = customers.CustomerID
               WHERE loans.ApprovalStatus LIKE 'Rejected'
               GROUP BY customers.Region """

    return qry



def question_3():    
    
    # Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
        # `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`
    # Do not return the new table

    

#creates tbl with relevant columns and then inserts data from existing tbls
#uses inner join to find customers with loans/credit scores
    qry = """ CREATE TABLE financing (
              CustomerID INT,
              Income INT,
              LoanAmount INT,
              LoanTerm INT,
              InterestRate DECIMAL(5, 2),
              ApprovalStatus VARCHAR(50),
              CreditScore INT );

              INSERT INTO financing (CustomerID, Income, LoanAmount, LoanTerm, InterestRate, ApprovalStatus, CreditScore) 
              SELECT customers.CustomerID, customers.Income, loans.LoanAmount, loans.LoanTerm, loans.InterestRate, loans.ApprovalStatus, credit.CreditScore 
              FROM customers INNER JOIN loans ON customers.CustomerID = loans.CustomerID
              INNER JOIN credit ON credit.CustomerID = customers.CustomerID; """
    
    return qry


# Question 4 and 5 are linked


def question_4():

    # Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarizes Repayments per customer per month.
    # Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    # Repayments should only occur between 6am and 6pm London Time.
    # Hint: there should be 12x CustomerID = 1.
    # Null values to be filled with 0.
    

    #makes use of cross join to ensure that there is a repayment entry for every customer, for every month
    #uses coalesce to map null repayment values to 0
    #extracts hour from date
    qry = """ 
              CREATE TABLE timeline (
              CustomerID INT,
              MonthName VARCHAR(10),
              NumberOfRepayments INT,
              AmountTotal DECIMAL(10, 2));
              

              INSERT INTO timeline (CustomerID, MonthName, NumberOfRepayments, AmountTotal)
              SELECT repayments.CustomerID, months.MonthName, COUNT(*) AS NumberOfRepayments, COALESCE(SUM(repayments.Amount), 0) AS AmountTotal
              FROM repayments CROSS JOIN months
              WHERE EXTRACT(HOUR FROM repayments.RepaymentDate) >= 6 AND EXTRACT(HOUR FROM repayments.RepaymentDate) < 18
              GROUP BY months.MonthName, repayments.CustomerID; """

    return qry



def question_5():

    # Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
        # CustomerID, JanuaryRepayments, JanuaryTotal,...,DecemberRepayments, DecemberTotal,...etc
    # MonthRepayments columns (e.g JanuaryRepayments) should be integers
    # Hint: there should be 1x CustomerID = 1

    # TODO to be implemented
    qry = """ """

    return qry





#QUESTION 6 and 7 are linked

def question_6():

    # The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    # Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    # relation to the corresponding CustomerID.

    # Utilize a window function to correct this mistake in a new `CorrectedAge` column.
    # Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender` 
    # Also return a result set for this table
    # Null values can be input manually

    #lag(age,2) references row 2 rows above given row, if there is no value -> will be mapped to null
    
    qry = """ CREATE TABLE corrected_customers AS
              SELECT CustomerID, Age, LAG(Age, 2) OVER (ORDER BY CustomerID), Age AS CorrectedAge, Gender
              FROM customers; 
              
              SELECT * FROM corrected_customers; """

    return qry


def question_7():

    # Create a column called 'AgeCategory' that categorizes customers by age 
    # Age categories should be as follows:
        # Teen: x < 20
        # Young Adult: 20 <= x < 30
        # Adult: 30 <= x < 60
        # Pensioner: x >= 60
    # Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    # The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6 
    # Customers with no repayments should be included as 0 in the result.

    # uses case statement to assign category to each age range
    # dense rank is used to ensure that numbers in sequence not skipped
    # rank orders by the greatest number of repayments (by counting repayment ID, after grouping by AgeCategory
    qry = """ SELECT customers.CustomerID, customers.Age, CASE
                            WHEN Age < 20 THEN 'Teen'
                            WHEN Age >= 20 AND Age < 30 THEN 'Young Adult'
                            WHEN Age >= 30 AND Age < 60 THEN 'Adult'
                            ELSE 'Pensioner'END AS AgeCategory,
    COALESCE(COUNT(repayments.RepaymentID), 0) AS TotalRepayments, DENSE_RANK() OVER (PARTITION BY AgeCategory ORDER BY COUNT(repayments.RepaymentID) DESC) AS Rank
        FROM  customers LEFT JOIN repayments ON customers.CustomerID = repayments.CustomerID
        GROUP BY  AgeCategory, customers.CustomerID, customers.Age
        ORDER BY AgeCategory, Rank; """

    return qry
