import sqlite3
import csv
import statistics

# Connect to the database
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Fetch data from the "employees" and "departments" tables
query = """
    SELECT employees.employee_name, employees.salary, departments.department_name
    FROM employees
    JOIN departments ON employees.department_id = departments.department_id
    WHERE departments.department_name = 'Sales' AND employees.salary >= 50000
"""
#print(query)
cursor.execute(query)
results = cursor.fetchall()
#print(results)

# Calculate average and median salary
salaries = [row[1] for row in results]
average_salary = statistics.mean(salaries)
median_salary = statistics.median(salaries)
#print(median_salary)

# Group data by department and find highest earner
department_earners = {}
for row in results:
    employee_name = row[0]
    salary = row[1]
    department = row[2]
    print(employee_name)

    if department not in department_earners or salary > department_earners[department][1]:
        department_earners[department] = (employee_name, salary)

# Find the employee with the highest salary in the entire company
highest_earner = max(results, key=lambda x: x[1])

# Save results to a CSV file
with open("salary_report.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Department", "Highest Earner", "Salary"])
    for department, (employee, salary) in department_earners.items():
        writer.writerow([department, employee, salary])

# Close the database connection
cursor.close()
conn.close()
