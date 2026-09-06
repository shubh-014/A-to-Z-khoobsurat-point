let total = parseFloat(localStorage.getItem("total") || 0.0);
let totalExpense = parseFloat(localStorage.getItem("expenses") || 0.0);
let totalIncome = parseFloat(localStorage.getItem("income") || 0.0);
let totalSaving = parseFloat(localStorage.getItem("saving") || 0.0);


document.getElementById("total-balance").innerHTML = "Rs " + total.toFixed(2);
document.getElementById("total-expenses").innerHTML = "Rs " + totalExpense.toFixed(2);
document.getElementById("total-income").innerHTML = "Rs " + totalIncome.toFixed(2);
document.getElementById("total-savings").innerHTML = "Rs " + totalSaving.toFixed(2);


document.getElementById("add-transaction").addEventListener("click", function () {
    let transactionName = document.getElementById("description").value;
    let transactionAmount = parseFloat(document.getElementById("amount").value);
    let transactionType = document.getElementById("transaction-type").value;
    if (transactionAmount < 0) { alert("Amount can't be negative"); return; }
    if (isNaN(transactionAmount)) {
        alert("Enter amount");
        return;
    }
    if (transactionType === "select") { alert("Enter Transaction Type") }
    else if (transactionType === "Expense") { expense(transactionAmount) }
    else if (transactionType === "Income") { income(transactionAmount) }
    else saving(transactionAmount);

});
document.getElementById("reset").addEventListener("click", function () {
    total = 0.0;
    totalIncome = 0.0;
    totalExpense = 0.0;
    totalSaving = 0.0;
    update();
});

let expense = function (transactionAmount) {
    if (transactionAmount > total) {
        let balance = transactionAmount - total
        if (confirm("Not sufficient balance, do you want to retrieve the remaining Rs" + balance + " from your savings?")) {
            if (totalSaving >= balance) {
                total = 0;
                totalExpense += transactionAmount;
                totalSaving -= balance;
            }
            else alert("You do not have enough balance")
        }

    } else {
        total = total - transactionAmount;
        totalExpense += transactionAmount;
    }

    update();
};

let income = function (transactionAmount) {
    total = total + transactionAmount;
    totalIncome += transactionAmount;
    update();
}

let saving = function (transactionAmount) {
    if (transactionAmount > total) { alert("You do not have enough savings") } else {
        total = total - transactionAmount;
        totalSaving += transactionAmount;
        update();
    }
}



let update = function () {
    localStorage.setItem("total", total);
    localStorage.setItem("expenses", totalExpense);
    localStorage.setItem("income", totalIncome);
    localStorage.setItem("saving", totalSaving);
    document.getElementById("total-balance").innerHTML = "Rs " + total.toFixed(2);
    document.getElementById("total-expenses").innerHTML = "Rs " + totalExpense.toFixed(2);
    document.getElementById("total-income").innerHTML = "Rs " + totalIncome.toFixed(2);
    document.getElementById("total-savings").innerHTML = "Rs " + totalSaving.toFixed(2);
    document.getElementById("description").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("transaction-type").value = "";
    myChart.data.datasets[0].data = [

        totalExpense,

        totalIncome,

        totalSaving

    ];

    myChart.update();
    let chartTotal =  parseFloat(localStorage.getItem("total"));

document.querySelector("#chart-center strong").innerHTML =
    "Rs " + chartTotal.toFixed(2);
}
let ctx = document.getElementById("chart");
let myChart = new Chart(ctx, {
    type: "doughnut",

    data: {
        labels: ["Expenses", "Income", "Savings"],

        datasets: [{
            data: [totalExpense, totalIncome, totalSaving]
        }]
    },

    options: {
        maintainAspectRatio: false,

        cutout: "65%",

        plugins: {
            legend: {
                position: "right"
            }
        }
    }
});
window.onload = function () {
    let x = localStorage.getItem("username");
    if (x == null) {
        let username = prompt("Whats your good name?")
        localStorage.setItem("username", username)
    }
    x = localStorage.getItem("username");
    document.getElementById("Username").innerHTML = x.toUpperCase();
}
document.getElementById("Signout").onclick = function () {
    if (confirm("Are you sure you wish to sign out?")) {
        localStorage.removeItem("username");
        total = 0.0;
        totalIncome = 0.0;
        totalExpense = 0.0;
        totalSaving = 0.0;
        document.getElementById("Username").innerHTML = " ";
        update();
        let username = prompt("Whats your good name?")
        localStorage.setItem("username", username)
        x = localStorage.getItem("username");
        document.getElementById("Username").innerHTML = x.toUpperCase();
    }
}

const navitems = document.querySelectorAll(".nav-item");

navitems.forEach(function (item) {

    item.addEventListener("click", function () {

        navitems.forEach(function (nav) {

            nav.classList.remove("active");

        });
        item.classList.add("active");

    });

});


