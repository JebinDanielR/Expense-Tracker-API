const expenseForm = document.getElementById("expense-form");
const categorySelect = document.getElementById("category");
const expenseTableBody = document.getElementById("expense-table-body");
const summaryDiv = document.getElementById("summary");

document.addEventListener("DOMContentLoaded", () => {
    loadCategories();
    loadExpenses();
    loadSummary();
});

// GraphQL - Load Categories
async function loadCategories() {
    const query = `
        query {
            categories {
                id
                name
            }
        }
    `;

    const response = await fetch("/graphql", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            query: query
        })
    });

    const result = await response.json();

    categorySelect.innerHTML = "";

    result.data.categories.forEach(category => {
        const option = document.createElement("option");

        option.value = category.id;
        option.textContent = category.name;

        categorySelect.appendChild(option);
    });
}

// REST - Load Expenses
async function loadExpenses() {
    const response = await fetch("/expenses");

    const expenses = await response.json();

    expenseTableBody.innerHTML = "";

    expenses.forEach(expense => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${expense.amount}</td>
            <td>${expense.description}</td>
            <td>${expense.spent_on}</td>
            <td>${expense.category_name}</td>
        `;

        expenseTableBody.appendChild(row);
    });
}

// REST - Add Expense
expenseForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const expense = {
        amount: Number(
            document.getElementById("amount").value
        ),

        description:
            document.getElementById("description").value,

        spent_on:
            document.getElementById("spent_on").value,

        category_id:
            Number(categorySelect.value)
    };

    const response = await fetch("/expenses", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(expense)
    });

    if (response.ok) {

        expenseForm.reset();

        await loadExpenses();
        await loadSummary();

    } else {

        const error = await response.json();

        alert(error.detail);
    }
});

// REST - Monthly Summary
async function loadSummary() {

    const today = new Date();

    const month =
        `${today.getFullYear()}-${String(
            today.getMonth() + 1
        ).padStart(2, "0")}`;

    const response =await fetch(`/summary?month=${month}`);

    const summary =await response.json();

    let html = `
        <div class="total">
            Total Spend: ${summary.total_spend}
        </div>
    `;

    summary.breakdown.forEach(item => {

        html += `
            <div class="summary-item">

                <span>
                    ${item.category_name}
                </span>

                <span>
                    ${item.total}
                    (${item.percentage}%)
                </span>

            </div>
        `;

    });

    summaryDiv.innerHTML = html;
}