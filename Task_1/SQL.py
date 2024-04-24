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
    
    # Find all name-surname combinations that are duplicated in the customers dataset. 
    # Return `Name` and `Surname` columns

    # groups by name and surname and then returns duplicates of this combination (count > 1)
    qry = """ SELECT Name, Surname
              FROM customers
              GROUP BY Name, Surname
              HAVING COUNT(*) > 1 """
    
    return qry



def question_2():    
    
    # Return the `Name`, `Surname` and `Income` of all female customers in the dataset in descending order of income

    #returns relevant columns where gender = female, and orders by income in descending order
    qry = """ SELECT Name, Surname, Income, Gender 
              FROM customers
              WHERE customers.Gender LIKE 'Female'
              ORDER BY Income DESC """

    return qry




def question_3():    
    
    # Find the `ApprovalPercentage` of loans by `LoanTerm`

                # if approved then add 1, else add nothing -> counts the number of approved loans
                # divides by the total number of loans and then multiplies by 100 to return %
                # % calculated per loan term 

    qry = """ SELECT (COUNT(CASE WHEN ApprovalStatus = 'Approved' THEN 1 END) / COUNT(*) * 1.0) AS ApprovalPercentage
              FROM loans 
              GROUP BY LoanTerm """

    return qry




def question_4():    
    
    # Return a breakdown of the number of customers per CustomerClass in the credit data
    # Return columns `CustomerClass` and `Count`

    #counts the number of customers/customer ID's in each customer class
    qry = """ SELECT CustomerClass, COUNT(CustomerID) AS Count
              FROM credit
              GROUP BY CustomerClass """

    return qry





def question_5():    
    
    # Make use of the UPDATE function to amend/fix the following: Customers with a CreditScore between and including 600 to 650 must be classified as CustomerClass C.

    
    # sql BETWEEN is inclusive and therefore includes 600 and 650
    # specifies criteria for update to class C
    qry = """ UPDATE credit
              SET CustomerClass = 'C'
              WHERE CreditScore BETWEEN 600 AND 650 """
    
    return qry


