public class EmployeeManager {

    private String companyName;
    private int employeeCount;

    public EmployeeManager(String companyName) {
        this.companyName = companyName;
        this.employeeCount = 0;
    }

    public void hireEmployee() {
        employeeCount++;
    }

    public void fireEmployee() {
        if (employeeCount > 0) {
            employeeCount--;
        }
    }

    public int getEmployeeCount() {
        return employeeCount;
    }

    public String getCompanyName() {
        return companyName;
    }

    /* operational logic */

    public void processMonthlyPayroll() {
        System.out.println("Processing payroll...");
        applyBonuses();                 // moved
        calculateSalaries();            // moved
        generatePayrollSummary();       // added
        finalizePayroll();
    }

    private void calculateSalaries() {
        System.out.println("Calculating salaries");
    }

    private void generatePayrollSummary() { // added
        System.out.println("Generating payroll summary");
    }

    private void finalizePayroll() {
        System.out.println("Finalizing payroll");
    }

    /* reporting */

    public void printReport() {
        System.out.println("Company: " + companyName);
        System.out.println("Employees: " + employeeCount);
    }

    public static void main(String[] args) {
        EmployeeManager em = new EmployeeManager("TechCorp");
        em.hireEmployee();
        em.hireEmployee();
        em.processMonthlyPayroll();
        em.printReport();
    }
}
